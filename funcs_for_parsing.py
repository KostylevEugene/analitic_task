from queries import *
from db_eng import db_session
import re

''' В данном файле содержатся функции необходимые для парсинга данных из логов. '''


# Создаёт модель события и записывает её в БД
def create_new_user(date, time, ip):
    new_action = Action(date, time, ip)
    db_session.add(new_action)


# Ищет дату, время и IP в строке
def parse_date_ip(line):
    return (re.findall(r'\d{4}-\d{2}-\d{2}', line)[0],      # regex пример: 2014-02-24
            re.findall(r'\d{2}:\d{2}:\d{2}', line)[0],      # regex пример: 00:01:35
            re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line)[0])     # regex пример: 217.89.121.82


# Записывает данные в БД
def add_commit_to_db(*data):
    db_session.add(*data)
    db_session.commit()


# Ищет id товара, количество товара и id корзины в строке
def parse_goods_info(line):
    return (re.findall(r'goods_id=(\d+)', line)[0],     # regex пример:  8
            re.findall(r'amount=(\d+)', line)[0],       # regex пример:  13
            re.findall(r'cart_id=(\d+)', line)[0])       # regex пример:  8642


# Записывает данные корзины в БД
def send_cart_info_to_db(line):
    goods_id, amount, cart_id = parse_goods_info(line)

    date, time, ip = parse_date_ip(line)

    create_new_user(date, time, ip)

    if is_cart_exists(cart_id) is None:
        cart = Cart(cart_id)
        db_session.add(cart)

    if is_good_exists(goods_id) is None:
        goods = Good(goods_id)
        db_session.add(goods)

    db_session.commit()

    last_action_id = get_last_action_id()
    goods_in_cart = GoodsInCart(cart_id, goods_id, amount, last_action_id)
    add_commit_to_db(goods_in_cart)


# Ищет id пользователя и id корзины в строке
def parse_pay_info(line):
    return (re.findall(r'user_id=(\d+)', line)[0],         # regex пример:  81270149216
            re.findall(r'cart_id=(\d+)', line)[0])        # regex пример:  8642


# Записывает данные платежа в БД
def send_pay_info(line):
    date, time, ip = parse_date_ip(line)

    create_new_user(date, time, ip)

    user_id, cart_id = parse_pay_info(line)

    if is_user_exists(user_id) is None:
        user = User(user_id, ip)
        add_commit_to_db(user)
    else:
        db_session.query(User).filter(User.id == user_id).update({'last_ip': ip})

    last_action_id = get_last_action_id()

    payment = Payment(cart_id, last_action_id, user_id, None)
    add_commit_to_db(payment)


# Записывает подтверждение платежа в БД
def confirm_payment(line):
    paid_cart = re.findall(r'pay_(\d+)', line)[0]       # regex пример:  success

    db_session.query(Payment).filter(Payment.cart_id == paid_cart).update({'payment_status': 'paid'})
    db_session.commit()


# Ищет пользовательскую активность в категориях товара и записывает её в БД
def parse_category(line):
    category = re.findall(r'\.com/(\w+)', line)         # regex пример:  semi_manufactures

    date, time, ip = parse_date_ip(line)

    # Если категория новая
    if category and is_category_exists(category[0]) is None:
        new_category = Category(category[0])

        create_new_user(date, time, ip)

        add_commit_to_db(new_category)

        category_id = get_category_id(category[0])
        last_action_id = get_last_action_id()

        new_user_action = UsersAction(last_action_id, category_id)
        add_commit_to_db(new_user_action)

    # Если категория уже существует
    elif category and is_category_exists(category[0]) is not None:
        create_new_user(date, time, ip)
        db_session.commit()

        last_action_id = get_last_action_id()
        category_id = get_category_id(category[0])

        new_user_action = UsersAction(last_action_id, category_id)
        add_commit_to_db(new_user_action)

    # Если категория отсутствует
    else:
        create_new_user(date, time, ip)
        db_session.commit()
