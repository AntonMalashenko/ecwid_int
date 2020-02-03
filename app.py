import os

from settings import app_settings
from settings.app_settings import PROJECT_ROOT, FILES_DIR_NAME, FILES_PATH
from src.utils import make_list_of_orders
from src.client.ecwid_client import EcwidClient
from src.processors.xls_processor import XlsProcessor


def create_file_dir():
    if not FILES_DIR_NAME in os.listdir(PROJECT_ROOT):
        os.mkdir(FILES_PATH)


def app():
    create_file_dir()
    client = EcwidClient(
        app_settings.API_PRIVATE_TOKEN,
        app_settings.STORE_ID
    )
    orders = client.search_orders()
    orders = make_list_of_orders(orders)
    processor = XlsProcessor(orders)
    processor.make_table()


if __name__ == '__main__':
    app()
