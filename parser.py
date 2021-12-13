from funcs_for_parsing import *

''' В данном файле находится парсер логов. '''

f = open('logs.txt')
lines = f.readlines()

for line in lines:

    if re.search(r'cart\?', line):
        send_cart_info_to_db(line)

    elif re.search(r'pay\?', line):
        send_pay_info(line)

    elif re.search(r'success', line):
        confirm_payment(line)

    else:
        parse_category(line)
