from db import db_session
from models import *
from sqlalchemy.sql import func
import re


def is_category_exists(cat):
    result = db_session.query(Category.category).filter(Category.category == cat).scalar()
    return result

def get_category_id(cat):
    result = db_session.query(Category.id).filter(Category.category == cat).scalar()
    return result

def get_last_action_id():
    result = db_session.query(func.max(Action.id)).scalar()
    return result

def get_last_category_id():
    result = db_session.query(func.max(Category.id)).scalar()
    return result

f = open('newlogs.txt')

lines = f.readlines()

for line in lines:

    date = re.findall(r'\d{4}-\d{2}-\d{2}', line)[0]
    time = re.findall(r'\d{2}:\d{2}:\d{2}', line)[0]
    ip = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line)[0]


    if re.search(r'cart\?', line):
        goods_id = re.findall(r'goods_id=(\d+)', line)[0]
        amount = re.findall(r'amount=(\d+)', line)[0]
        cart_id = re.findall(r'cart_id=(\d+)', line)[0]

        # print(goods_id, amount, cart_id)

    if re.search(r'pay\?', line):
        user_id = re.findall(r'user_id=(\d+)', line)[0]
        cart_id = re.findall(r'cart_id=(\d+)', line)[0]

        # print(user_id, cart_id)

    if re.search(r'success', line):
        paid_cart = re.findall(r'pay_(\d+)', line)[0]

        # print(paid_cart)

    else:
        category = re.findall(r'\.com/(\w+)', line)

        # Если категория новая
        if category and is_category_exists(category[0]) == None:
            new_category = Category(category[0])

            new_action = Action(ip, time, date)

            db_session.add(new_category, new_action)
            db_session.commit()


        # Если категория уже существует
        if category and is_category_exists(category[0]) != None:
            new_action = Action(ip, time, date)
            db_session.add(new_action)
            db_session.commit()

            last_action_id = get_last_action_id()

            category_id = get_category_id(category[0])

            new_user_action = UsersAction(last_action_id, category_id)
            db_session.add(new_user_action)
            db_session.commit()

        # Если категория отсутствует
        else:

            new_action = Action(ip, time, date)
            db_session.add(new_action)
            db_session.commit()


    # print(date[0], time[0], ip[0], user_id)