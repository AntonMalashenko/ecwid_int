from urllib.parse import urljoin

import requests

from settings import app_settings


class EcwidClient:
    def __init__(self, token, store_id):
        self.token = token
        self.store_id = store_id

    def get_order(self, order_id):
        order_url = app_settings.ORDER_DETAIL_URL_TEMPLATE.format(
            store_id=self.store_id, order_id=order_id
        )
        response = requests.get(
            url=urljoin(app_settings.BASE_ECWID_URL, order_url),
            params=dict(
                token=self.token
            )
        )
        return response

    def search_orders(self, order_ids=None):
        if order_ids:
            qery_str = '?orderNumber={}'.format(','.join([str(order) for order in set(order_ids)]))
            order_url = app_settings.ORDER_SEARCH_URL_TEMPLATE.format(
                store_id=self.store_id) + qery_str
        else:
            order_url = app_settings.ORDER_SEARCH_URL_TEMPLATE.format(
                store_id=self.store_id)
        response = requests.get(
            url=urljoin(app_settings.BASE_ECWID_URL, order_url),
            params=dict(
                token=self.token
            )
        )
        if response.status_code == 200:
            return response.json()
        raise requests.HTTPError(response.status_code, response.reason)

    def store_profile(self):
        order_url = app_settings.STORE_PROFILE_URL_TEMPLATE.format(
            store_id=self.store_id,
        )
        response = requests.get(
            url=urljoin(app_settings.BASE_ECWID_URL, order_url),
            params=dict(
                token=self.token
            )
        )
        return response

    def get_products(self, product_ids):
        order_url = app_settings.PRODUCT_SEARCH_URL_TEMPLATE.format(
            self.store_id, ','.join(product_ids))
        response = requests.get(
            url=urljoin(app_settings.BASE_ECWID_URL, order_url),
            params=dict(
                token=self.token
            )
        )
        if response.status_code == 200:
            return response.json()
        print(response.status_code, response.reason)
