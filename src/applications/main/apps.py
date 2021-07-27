from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_HALF_DOWN
import os

from django.apps import AppConfig
from django.conf import settings

from openpyxl import load_workbook

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
        material = ConstructionMaterial(
            id_instance=n,
            name=row[0],
            unit=row[1] if row[1] is not None else 'ШТ',
            quantity=row[2],
            price=row[3] if row[3] is not None else round(row[4] / row[2], 5),
            total_cost=row[4],
            building_object_id=object_id,
        )
        materials.append(material)

    ConstructionMaterial.objects.bulk_create(materials[1:])


def create_xml(object_id: int, user_id: int):
    from xml.dom import minidom
    from applications.main.models import ConstructionMaterial

    doc = minidom.Document()

    root = doc.createElement('root')
    doc.appendChild(root)

    root1 = doc.createElement('root1')
    root.appendChild(root1)

    root2 = doc.createElement('root2')
    root1.appendChild(root2)

    data = ConstructionMaterial.objects.filter(building_object__id=object_id)

    for key, value in enumerate(data, start=1):
        if key <= 9:
            basis = f"СЦЕН-МТ-00{str(key)}"
        elif key <= 99:
            basis = f"СЦЕН-МТ-0{str(key)}"
        else:
            basis = f"СЦЕН-МТ-{str(key)}"

        quantity = Decimal(str(value.quantity)).normalize()

        price = Decimal(str(value.price)).normalize()

        unit_tr = (price * Decimal('0.02'))  # the parameter will be fixed after import
        unit_tr = unit_tr.quantize(Decimal('1.00'), ROUND_HALF_UP)

        total_tr = (unit_tr * quantity).quantize(Decimal('1.00'), ROUND_HALF_UP)

        unit_cost = (price + unit_tr).quantize(Decimal('1.00'), ROUND_HALF_UP)

        total_cost = Decimal(str(value.total_cost)).normalize()

        total_cost_total_tr = (total_tr + total_cost).quantize(Decimal('1.00'), ROUND_HALF_UP)

        rascenka = doc.createElement('rascenka')
        rascenka.setAttribute('npp', str(key))
        rascenka.setAttribute('obosn', basis)
        rascenka.setAttribute('naim', value.name)
        rascenka.setAttribute('idGrw', '1')
        rascenka.setAttribute('klv', str(quantity))
        rascenka.setAttribute('ed_izm', value.unit)
        rascenka.setAttribute('vid_ohr_pp', '11')  # the parameter will be fixed after import
        rascenka.setAttribute('uniq_lab_ohr_pp', '1.1')  # the parameter will be fixed after import
        rascenka.setAttribute('tip', '101')
        rascenka.setAttribute('cena_0', str(unit_cost))

        # nabor_kf
        nabor_kf = doc.createElement('nabor_kf')
        rascenka.appendChild(nabor_kf)

        koef_1 = doc.createElement('koef_1')
        koef_1.setAttribute('naim', '1-й коэффициент к расценке (справочно)')
        koef_1.setAttribute('mat', '1')
        koef_1.setAttribute('tr', '1')
        nabor_kf.appendChild(koef_1)

        koef_2 = doc.createElement('koef_2')
        koef_2.setAttribute('naim', '2-й коэффициент к расценке (справочно)')
        koef_2.setAttribute('mat', '1')
        koef_2.setAttribute('tr', '1')
        nabor_kf.appendChild(koef_2)

        koef_3 = doc.createElement('koef_3')
        koef_3.setAttribute('naim', '1-й коэффициент к расценке (справочно)')
        koef_3.setAttribute('mat', '1')
        koef_3.setAttribute('tr', '1')
        nabor_kf.appendChild(koef_3)

        cena = doc.createElement('cena')
        cena.setAttribute('mat', str(price))
        cena.setAttribute('tr', str(unit_tr))
        cena.setAttribute('pryam', str(unit_cost))
        cena.setAttribute('prc_ohr', '')  # the parameter will be fixed after import
        cena.setAttribute('prc_pp', '')  # the parameter will be fixed after import
        rascenka.appendChild(cena)

        stoimost = doc.createElement('stoimost')
        stoimost.setAttribute('mat', str(total_cost))
        stoimost.setAttribute('tr', str(total_tr))
        stoimost.setAttribute('pryam', str(total_cost_total_tr))
        stoimost.setAttribute('ohr', '0')
        stoimost.setAttribute('pp', '0')
        rascenka.appendChild(stoimost)

        # materialy
        materialy = doc.createElement('materialy')
        rascenka.appendChild(materialy)

        resurs = doc.createElement('resurs')
        resurs.setAttribute('obosn', basis)
        resurs.setAttribute('kodcic', '')
        resurs.setAttribute('naim', value.name)
        resurs.setAttribute('ed_izm', value.unit)
        resurs.setAttribute('norma', '1')
        resurs.setAttribute('klv', str(quantity))
        resurs.setAttribute('cena_0', str(price))
        resurs.setAttribute('stm_0', str(total_cost))  # str(round(price * quantity, 2)))
        resurs.setAttribute('tr', str(unit_tr))
        resurs.setAttribute('tr_rub', '0')
        resurs.setAttribute('cena_tr', '2')  # the parameter will be fixed after import
        materialy.appendChild(resurs)

        root2.appendChild(rascenka)

    xml_str = doc.toprettyxml(indent="  ")

    path = f"{settings.MEDIA_ROOT}/{user_id}/xml/"
    file_name = f"Materials_obj{object_id}.xml"
    file_path = f"{settings.MEDIA_ROOT}/{user_id}/xml/{file_name}"
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{file_path}", "w") as f:
        f.write(xml_str)


def get_data_for_xml(object_id: int,):
    from applications.main.models import ConstructionMaterial

    data = ConstructionMaterial.objects.filter(building_object__id=object_id)

    for key, value in enumerate(data, start=1):
        if key <= 9:
            basis = f"СЦЕН-МТ-00{str(key)}"
        elif key <= 99:
            basis = f"СЦЕН-МТ-0{str(key)}"
        else:
            basis = f"СЦЕН-МТ-{str(key)}"

        # if int(str(value.quantity).split('.')[1]):
        #     quantity = value.quantity
        #     quantity.normalize()
        # else:
        #     quantity = int(str(value.quantity).split('.')[0])

        quantity = Decimal(str(value.quantity)).normalize()
        # logger.debug(f"quantity: {quantity}")  # delete

        price = Decimal(str(value.price)).normalize()
        # logger.debug(f"price: {price}")  # delete

        unit_tr = (price * Decimal('0.02'))  # the parameter will be fixed after import
        unit_tr = unit_tr.quantize(Decimal('1.00'), ROUND_HALF_UP)

        total_tr = (unit_tr * quantity).quantize(Decimal('1.00'), ROUND_HALF_UP)

        unit_cost = (price + unit_tr).quantize(Decimal('1.00'), ROUND_HALF_UP)

        total_cost = Decimal(str(value.total_cost)).normalize()

        total_cost_total_tr = (total_tr + total_cost).quantize(Decimal('1.00'), ROUND_HALF_UP)
        # tr * quantity + value.total_cost

        # cena_0 = round(value.price + tr_unit, 2)
    pass
