from db import db_session
from models import *
import re


def is_category_exists(cat):
    result = db_session.query(Category.category).filter(Category.category == cat).scalar()
    return result


f = open('newlogs.txt')

lines = f.readlines()

for line in lines:
    # list_line = line.split()[2:]
    # list_line[5] = list_line[5].split('/')[3:]

    # if list_line[5][0] == '':
        # list_line[5][0] = list_line[5][0].replace('', 'main_page')

    # print(list_line)

    # if 'cart?' in list_line[5][0]:
    #     result = re.split(r'[?&=]', list_line[5][0])
    #     result.pop(0)
    #     print(dict(result))
    date = re.findall(r'\d{4}-\d{2}-\d{2}', line)
    time = re.findall(r'\d{2}:\d{2}:\d{2}', line)
    ip = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line)

    if re.search(r'cart\?', line):
        goods_id = re.findall(r'goods_id=(\d+)', line)
        amount = re.findall(r'amount=(\d+)', line)
        cart_id = re.findall(r'cart_id=(\d+)', line)

        # print(goods_id[0], amount[0], cart_id[0])

    if re.search(r'pay\?', line):
        user_id = re.findall(r'user_id=(\d+)', line)
        cart_id = re.findall(r'cart_id=(\d+)', line)

        # print(user_id[0], cart_id[0])

    if re.search(r'success', line):
        paid_cart = re.findall(r'pay_(\d+)', line)

        # print(paid_cart[0])

    else:
        category = re.findall(r'\.com/(\w+)', line)
        # print(category)





    # print(date[0], time[0], ip[0], user_id)