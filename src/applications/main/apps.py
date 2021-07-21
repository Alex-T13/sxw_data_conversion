from django.apps import AppConfig

from openpyxl import load_workbook
from framework.custom_logging import logger


class MainConfig(AppConfig):
    label = "main"
    name = f"applications.{label}"


def handle_uploaded_file(file, object_id: str):
    from applications.main.models import ConstructionMaterial

    wb = load_workbook(filename=file, data_only=True)
    ws = wb.active

    checking_row_0 = next(ws.values)
    logger.debug(f"row_0:{checking_row_0}")
    if checking_row_0 != ('NAIM', 'ED_IZM', 'KOL_VO', 'PRICE', 'COST'):
        raise IndexError

    materials = [
        ConstructionMaterial(
            name=row[0],
            unit=row[1] if row[1] is not None else 'ШТ',
            quantity=row[2],
            price=row[3] if row[3] is not None else None,
            total_cost=row[4],
            building_object_id=object_id,
        )
        for row in ws.values
    ]

    ConstructionMaterial.objects.bulk_create(materials[1:])
