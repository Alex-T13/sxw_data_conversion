from decimal import Decimal
from typing import NamedTuple


class DataForXML(NamedTuple):
    id_instance: str
    basis: str
    name: str
    unit: str
    quantity: Decimal
    price: Decimal
    unit_tr: Decimal
    total_tr: Decimal
    unit_cost: Decimal
    total_cost: Decimal
    total_cost_total_tr: Decimal
