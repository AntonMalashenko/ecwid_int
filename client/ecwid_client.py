from urllib.parse import urljoin

import requests

from settings import app_settings


class EcwidClient:
    def __init__(self, token):
        self.token = token

    def get_order(self, order_id):
        order_url = app_settings.ORDER_DETAIL_URL_TEMPLATE.format(
            store_id='4870020', order_id=order_id
        )
        response = requests.get(
            url=urljoin(app_settings.BASE_ECWID_URL, order_url),
            params=dict(
                token=self.token
            )
        )
        return response

    def search_orders(self, order_ids: list):
        order_url = app_settings.ORDER_SEARCH_URL_TEMPLATE.format(
            store_id='4870020',
            order_ids=','.join([str(order) for order in set(order_ids)])
        )
        response = requests.get(
            url=urljoin(app_settings.BASE_ECWID_URL, order_url),
            params=dict(
                token=self.token
            )
        )
        return response

    def store_profile(self, store_id):
            order_url = app_settings.STORE_PROFILE_URL_TEMPLATE.format(
                store_id=store_id,
            )
            response = requests.get(
                url=urljoin(app_settings.BASE_ECWID_URL, order_url),
                params=dict(
                    token=self.token
                )
            )
            return response

if __name__ == '__main__':
    client = EcwidClient(app_settings.API_TOKEN)
    # order = client.search_orders([3,5,6,98,23, 23])
    order = client.store_profile(4870020)
