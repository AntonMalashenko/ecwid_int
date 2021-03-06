import argparse
import copy

from settings.app_settings import MAX_PRODUCT_LENGTH
from src.processors.xls_processor import make_table
from src.utils import split_array


class OrderProcessor:
    response = None
    products = dict()

    def __init__(self, client, extra_args: argparse.Namespace):
        self.client = client
        self.extra_args = extra_args

    def start(self):
        self.response = self.client.search_orders()
        orders = self.make_list_of_orders()
        product_ids = self.prepare_product_request(orders)
        product_ids = split_array(product_ids, MAX_PRODUCT_LENGTH)
        products = []
        for array in product_ids:
            response = self.client.get_products(array).get('items')
            products.extend(response)
        products = self.create_products_dict(products)
        make_table(
            orders,
            products,
            self.extra_args.mult,
            self.extra_args.dim,
            self.extra_args.dtype,
            self.extra_args.dimconv,
            self.extra_args.country_code,
        )

    def create_products_dict(self, products):
        return {
            item.get('id'): item
            for item in products
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
            orders = self.split_order(item)
            orders_list.extend(orders)
        return orders_list
