import copy
import json


def split_order(order):
    orders_result = []
    items = order.pop('items')
    for item in items:
        each_item = copy.deepcopy(order)
        each_item.update(item)
        orders_result.append(each_item)
    return orders_result


def make_list_of_orders(response):
    orders_list = []
    for item in response.get('items'):
        orders = split_order(item)
        orders_list.extend(orders)
    return orders_list