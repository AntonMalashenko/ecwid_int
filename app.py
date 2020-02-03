import json

from settings import app_settings
from src.utils import make_list_of_orders
from src.client.ecwid_client import EcwidClient
from src.processors.xls_processor import XlsProcessor


def app():
    client = EcwidClient(
        app_settings.API_PRIVATE_TOKEN,
        app_settings.STORE_ID
    )
    # orders = client.search_orders()
    # orders = make_list_of_orders(orders)
    orders = json.load(open('data.json', 'rb'))
    processor = XlsProcessor(orders)
    processor.make_table()



if __name__ == '__main__':
    app()
