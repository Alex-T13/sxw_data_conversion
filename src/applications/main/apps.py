from decimal import Decimal, ROUND_HALF_UP
import os

from django.apps import AppConfig
from django.conf import settings

from openpyxl import load_workbook

from applications.main.d_types import DataForXML
from framework.custom_logging import logger


class MainConfig(AppConfig):
    label = "main"
    name = f"applications.{label}"


def handle_uploaded_file(file, object_id: int):
    from applications.main.models import ConstructionMaterial

    wb = load_workbook(filename=file, data_only=True)
    ws = wb.active

    checking_row_0 = next(ws.values)
    logger.debug(f"row_0:{checking_row_0}")
    if checking_row_0 != ('NAIM', 'ED_IZM', 'KOL_VO', 'PRICE', 'COST'):
        raise IndexError

    count_obj_db = int(ConstructionMaterial.objects.filter(building_object__id=object_id).count())
    logger.debug(f"count_obj_db: {count_obj_db}")

    materials = []

    for n, row in enumerate(ws.values, start=count_obj_db):
        logger.debug(f"iteration: {n}")
        if row[0] is None:
            raise TypeError
        if row[2] is None:
            raise TypeError
        if row[4] is None:
            raise TypeError

        material = ConstructionMaterial(
            id_instance=n,
            name=row[0],
            unit=row[1] if row[1] is not None else 'ШТ',
            quantity=row[2],
            price=row[3] if row[3] is not None else Decimal('{:f}'.format(
                (Decimal(row[4]) / Decimal(row[2])).quantize(Decimal('1.00000'), ROUND_HALF_UP).normalize())),
            total_cost=row[4],
            building_object_id=object_id,
        )
        materials.append(material)

    ConstructionMaterial.objects.bulk_create(materials[1:])
    return True


def create_xml(object_id: int, object_name: str, user_id: int):
    from xml.dom import minidom
    data = get_data_for_xml(object_id)

    doc = minidom.Document()
    root = doc.createElement('root')
    doc.appendChild(root)

    building = doc.createElement('stroyka')
    building.setAttribute('version', '1.2')
    building.setAttribute('prg', 'SXW')
    building.setAttribute('ver_prg', '')
    building.setAttribute('baza', '2017')
    building.setAttribute('idobekt', '')
    building.setAttribute('naim', '')
    building.setAttribute('nachalo', '')
    root.appendChild(building)

    obj_estimate = doc.createElement('ob_smeta')
    obj_estimate.setAttribute('nomer', '1')
    obj_estimate.setAttribute('naim', object_name)
    building.appendChild(obj_estimate)

    loc_estimate = doc.createElement('loc_smeta')
    loc_estimate.setAttribute('nomer', '1')
    loc_estimate.setAttribute('naim', '')
    obj_estimate.appendChild(loc_estimate)

    initial_data = doc.createElement('ishodnye_dannye')
    initial_data.setAttribute('zona', '3')
    initial_data.setAttribute('region', '7')
    initial_data.setAttribute('mesyac_cen', '7')
    initial_data.setAttribute('snds', '0')
    initial_data.setAttribute('vid_ohr_pp', '11')
    initial_data.setAttribute('stavka4', '6.94')
    initial_data.setAttribute('kf_zu', '0.93')
    initial_data.setAttribute('kf_vrem', '0.93')
    initial_data.setAttribute('num_post', '0.93')
    initial_data.setAttribute('kf_p4_ohr', '1')
    initial_data.setAttribute('kf_p4_pp', '1')
    loc_estimate.appendChild(initial_data)

    while True:
        try:
            next_data = next(data)
        except StopIteration:
            logger.debug('StopIteration!')
            break
        else:
            # logger.debug(f"iteration: {next_data.id_instance}")
            valuation = doc.createElement('rascenka')
            valuation.setAttribute('npp', next_data.id_instance)
            valuation.setAttribute('obosn', next_data.basis)
            valuation.setAttribute('naim', next_data.name)
            valuation.setAttribute('klv', str(next_data.quantity))
            valuation.setAttribute('ed_izm', next_data.unit)
            valuation.setAttribute('vid_ohr_pp', '11')  # the parameter will be fixed after import
            valuation.setAttribute('uniq_lab_ohr_pp', '1.1')  # the parameter will be fixed after import
            valuation.setAttribute('tip', '101')
            valuation.setAttribute('cena_0', str(next_data.unit_cost))
            loc_estimate.appendChild(valuation)

            price = doc.createElement('cena')
            price.setAttribute('mat', str(next_data.price))
            price.setAttribute('tr', str(next_data.unit_tr))  # the parameter will be fixed after import
            price.setAttribute('pryam', str(next_data.unit_cost))
            price.setAttribute('prc_ohr', '')  # the parameter will be fixed after import
            price.setAttribute('prc_pp', '')  # the parameter will be fixed after import
            valuation.appendChild(price)

            cost = doc.createElement('stoimost')
            cost.setAttribute('mat', str(next_data.total_cost))
            cost.setAttribute('tr', str(next_data.total_tr))  # the parameter will be fixed after import
            cost.setAttribute('pryam', str(next_data.total_cost_total_tr))
            cost.setAttribute('ohr', '0')
            cost.setAttribute('pp', '0')
            valuation.appendChild(cost)

            # materialy
            materials = doc.createElement('materialy')
            valuation.appendChild(materials)

            resources = doc.createElement('resurs')
            resources.setAttribute('obosn', next_data.basis)
            resources.setAttribute('kodcic', '')
            resources.setAttribute('naim', next_data.name)
            resources.setAttribute('ed_izm', next_data.unit)
            resources.setAttribute('norma', '1')
            resources.setAttribute('klv', str(next_data.quantity))
            resources.setAttribute('cena_0', str(next_data.price))
            resources.setAttribute('stm_0', str(next_data.total_cost))
            resources.setAttribute('tr', str(next_data.unit_tr))
            resources.setAttribute('tr_rub', '0')
            resources.setAttribute('cena_tr', '2')  # the parameter will be fixed after import
            materials.appendChild(resources)

    xml_str = doc.toprettyxml(indent=" ")
    xml_str = xml_str[:-8]

    path = f"{settings.MEDIA_ROOT}/{user_id}/xml/"
    file_path_xml = f"{settings.MEDIA_ROOT}/{user_id}/xml/Materials.xml"
    file_path_ref_part = f"{settings.MEDIA_ROOT}/_ref_part.txt"
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{file_path_xml}", "w") as f_xml, open(f"{file_path_ref_part}", "r") as f_ref_part:
        f_xml.write(xml_str)
        ref_part = f_ref_part.read()
        f_xml.write(ref_part)


def get_data_for_xml(object_id: int,) -> DataForXML:
    from applications.main.models import ConstructionMaterial
    data_from_base = ConstructionMaterial.objects.filter(building_object__id=object_id)

    for value in data_from_base:
        quantity = Decimal('{:f}'.format(Decimal(str(value.quantity)).normalize()))
        price = Decimal('{:f}'.format(Decimal(str(value.price)).normalize()))
        unit_tr = Decimal('{:f}'.format((price * Decimal('0.02')).quantize(Decimal('1.00'), ROUND_HALF_UP).normalize()))  # not '{:f}'
        total_tr = Decimal('{:f}'.format((unit_tr * quantity).quantize(Decimal('1.00'), ROUND_HALF_UP).normalize()))  # not '{:f}'
        unit_cost = Decimal('{:f}'.format((price + unit_tr).quantize(Decimal('1.00'), ROUND_HALF_UP).normalize()))  # not '{:f}'
        total_cost = Decimal('{:f}'.format(Decimal(str(value.total_cost)).normalize()))
        total_cost_total_tr = Decimal(
            '{:f}'.format((total_tr + total_cost).quantize(Decimal('1.00'), ROUND_HALF_UP).normalize())
        )  # not '{:f}'

        data_modified = DataForXML(
            id_instance=str(value.id_instance),
            basis=f"СЦЕН-МТ-00{value.id_instance}" if value.id_instance <= 9 else f"СЦЕН-МТ-0{value.id_instance}"
            if value.id_instance <= 99 else f"СЦЕН-МТ-{value.id_instance}",
            name=value.name,
            unit=value.unit,
            quantity=quantity,
            price=price,
            unit_tr=unit_tr,
            total_tr=total_tr,
            unit_cost=unit_cost,
            total_cost=total_cost,
            total_cost_total_tr=total_cost_total_tr
        )
        yield data_modified
