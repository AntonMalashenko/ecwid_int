

def clean_phone(phone):
    clear_phone = ''.join(x for x in phone if x.isdigit())
    if clear_phone.startswith('8'):
        clear_phone = '+7' + clear_phone[1:]
    else:
        clear_phone = '+' + clear_phone
    if len(clear_phone) == 12:
        clear_phone = "{}-{}-{}-{}".format(clear_phone[:2], clear_phone[2:5],
                                           clear_phone[5:8], clear_phone[8:])
    return clear_phone


def split_array(lst, count):
    if not isinstance(lst, list):
        lst = list(lst)
    result = []
    nested_res = []
    for item in lst:
        if len(nested_res) < count:
            nested_res.append(item)
            if lst[-1] == item:
                result.append(nested_res)
        else:
            result.append(nested_res)
            nested_res = [item,]
    return result




if __name__ == '__main__':
    test_list = list(range(30))

    print(split_array(test_list, 9))