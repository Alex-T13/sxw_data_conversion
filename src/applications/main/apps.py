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

    logger.debug(f"materials:{materials[0]}")
    #
    # for row in enumerate(ws.values):
    #     for value in enumerate(row):
    #         if value[0] % 3:
    #             print(f"value: {value[1]}")
    # нужна проверка первой строки

    try:
        ConstructionMaterial.objects.bulk_create(materials[1:])
        # ConstructionMaterial.objects.create(**data)
    except Exception:
        logger.info('Something went wrong')
    else:
        logger.info('The transaction was successful')
