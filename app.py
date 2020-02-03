import os

from settings import app_settings
from settings.app_settings import PROJECT_ROOT, FILES_DIR_NAME, FILES_PATH
from src.processors.order_processor import OrderProcessor
from src.client.ecwid_client import EcwidClient


def create_file_dir():
    if not FILES_DIR_NAME in os.listdir(PROJECT_ROOT):
        os.mkdir(FILES_PATH)


def app():
    create_file_dir()
    client = EcwidClient(
        app_settings.API_PRIVATE_TOKEN,
        app_settings.STORE_ID
    )
    order_processor = OrderProcessor(client)
    order_processor.start()


if __name__ == '__main__':
    app()
