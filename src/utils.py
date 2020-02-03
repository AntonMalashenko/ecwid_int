def clean_phone(phone):
    clear_phone = ''.join(x for x in phone if x.isdigit())
    if clear_phone.startswith('8'):
        clear_phone = '+7' + clear_phone[1:]
    else:
        clear_phone =  '+' + clear_phone
    if len(clear_phone) == 12:
        clear_phone = "{}-{}-{}-{}".format(clear_phone[:2], clear_phone[2:5],
                                           clear_phone[5:8], clear_phone[8:])
    return clear_phone
