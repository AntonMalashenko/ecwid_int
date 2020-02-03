import copy
import json

from settings.app_settings import PROJECT_ROOT
from src.processors.xls_processor import XlsProcessor


class OrderProcessor:
    response = None
    products = dict()

    def __init__(self, client):
        self.client = client

    def start(self):
        self.response = self.client.search_orders()
        orders = self.make_list_of_orders()
        product_ids = self.prepare_product_request(orders)
        products = self.client.get_products(product_ids)
        products = self.create_products_dict(products)
        XlsProcessor(orders, products).make_table()

    def create_products_dict(self, products):
        return {
            item.get('id'): item
            for item in products.get('items')
            if item.get('id')
        }

    def prepare_product_request(self, orders):
        ids = {str(o.get('productId')) for o in orders}
        return ids

    def split_order(self, order):
        orders_result = []
        items = order.pop('items')
        for item in items:
            each_item = copy.deepcopy(order)
            each_item.update(item)
            orders_result.append(each_item)
        return orders_result

    def make_list_of_orders(self):
        orders_list = []
        for item in self.response.get('items'):
            # if item.get('orderNumber') == 79:
            #     json.dump(item, open(PROJECT_ROOT+'/order_79.json', 'w'), indent=2)
            orders = self.split_order(item)
            orders_list.extend(orders)
        return orders_list


