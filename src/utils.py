import argparse


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
            nested_res = [item, ]
    return result


def get_cmd_args():
    parser = argparse.ArgumentParser(description='Videos to images')
    parser.add_argument(
        '--dtype',
        type=int,
        help='Delivery type: 1 or 2\ndefault=2',
        default=2,
        required=False
    )
    parser.add_argument(
        '--country_code',
        type=int,
        help='Country Code\ndefault=643(Russia)',
        default=643,
        required=False
    )
    parser.add_argument(
        '--mult',
        type=float,
        help='Multiplier for all orders. 1 for raw price\ndefault=1. Example: --mult 0.9 (10% discount)',
        default=1,
        required=False
    )
    parser.add_argument(
        '--dimconv',
        type=int,
        help='Dimension conversion from cm to mm. 1 for YES or 0 for NO.\ndefault=1',
        default=1,
        required=False
    )
    parser.add_argument(
        '--dim',
        type=str,
        help='Default dimension in mm. Format: "length*width*height" Example: 10*15*20.\ndefault="1*1*1"',
        default="1*1*1",
        required=False
    )
    args = parser.parse_args()

    # delivery type validation
    if args.dtype not in [1, 2]:
        raise ValueError('Delivery type: 1 or 2')

    # dimconv validation
    if args.dimconv not in [1, 0]:
        raise ValueError('dimconv: 1 for YES or 0 for NO')
    args.dimconv = bool(args.dimconv)

    # dimensions string validation and conversion to list for future usage
    try:
        dimensions = [int(d) for d in args.dim.split("*")]
        if len(dimensions) != 3:
            raise
        args.dim = dimensions
    except:
        raise ValueError(f'Wrong dimension format {args.dim}. Format "length*width*height" Example: 10*15*20')

    print(args)
    return args
