from db import db_session
from models import *
from queries import *
import re


f = open('logs.txt')

lines = f.readlines()

for line in lines:

    date = re.findall(r'\d{4}-\d{2}-\d{2}', line)[0]
    time = re.findall(r'\d{2}:\d{2}:\d{2}', line)[0]
    ip = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line)[0]


    if re.search(r'cart\?', line):
        goods_id = re.findall(r'goods_id=(\d+)', line)[0]
        amount = re.findall(r'amount=(\d+)', line)[0]
        cart_id = re.findall(r'cart_id=(\d+)', line)[0]

        new_action = Action(ip, time, date)
        db_session.add(new_action)

        if is_cart_exists(cart_id) == None:
            cart = Cart(cart_id)
            db_session.add(cart)

        if is_good_exists(goods_id) == None:
            goods = Good(goods_id)
            db_session.add(goods)

        db_session.commit()

        last_action_id = get_last_action_id()

        goods_in_cart = GoodsInCart(cart_id, goods_id, amount, last_action_id)
        db_session.add(goods_in_cart)
        db_session.commit()


    elif re.search(r'pay\?', line):
        user_id = re.findall(r'user_id=(\d+)', line)[0]
        cart_id = re.findall(r'cart_id=(\d+)', line)[0]

        new_action = Action(ip, time, date)
        db_session.add(new_action)

        if is_user_exists(user_id) == None:
            user = User(user_id, ip)
            db_session.add(user)
            db_session.commit()

        else:
            db_session.query(User).filter(User.id == user_id).update({'last_ip': ip})

        last_action_id = get_last_action_id()

        payment = Payment(cart_id, last_action_id, user_id, None)
        db_session.add(payment)
        db_session.commit()

    elif re.search(r'success', line):
        paid_cart = re.findall(r'pay_(\d+)', line)[0]

        db_session.query(Payment).filter(Payment.cart_id == paid_cart).update({'payment_status': 'paid'})
        db_session.commit()


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


