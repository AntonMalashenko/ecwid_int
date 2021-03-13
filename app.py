import os
import argparse

from settings import app_settings
from settings.app_settings import PROJECT_ROOT, FILES_DIR_NAME, FILES_PATH
from src.processors.order_processor import OrderProcessor
from src.client.ecwid_client import EcwidClient
from src.utils import get_cmd_args


def create_file_dir():
    if not FILES_DIR_NAME in os.listdir(PROJECT_ROOT):
        os.mkdir(FILES_PATH)


def app(
    cmd_args: argparse.Namespace,
    token: str = None,
    store_id: str = None
):
    create_file_dir()
    client = EcwidClient(
        token=token or app_settings.API_PRIVATE_TOKEN,
        store_id=store_id or app_settings.STORE_ID,
    )
    order_processor = OrderProcessor(client, cmd_args)
    order_processor.start()


if __name__ == '__main__':
    args = get_cmd_args()
    app(cmd_args=args)
