from db_eng import db_session
from models import *
from sqlalchemy.sql import func


''' В данном файле находится функции-запросы, необходимые для работы с БД при парсинге данных. '''


# Проверяет существует ли категория в БД
def is_category_exists(cat):
    result = db_session.query(Category.category).filter(Category.category == cat).scalar()
    return result


# Получает category_id из таблицы categories 
def get_category_id(cat):
    result = db_session.query(Category.id).filter(Category.category == cat).scalar()
    return result


# Проверяет последний созданный id в таблице actions
def get_last_action_id():
    result = db_session.query(func.max(Action.id)).scalar()
    return result


# Проверяет последний созданный id в таблице categories
def get_last_category_id():
    result = db_session.query(func.max(Category.id)).scalar()
    return result


# Проверяет существование корзины в таблице carts
def is_cart_exists(cart):
    result = db_session.query(Cart).filter(Cart.id == cart).scalar()
    return result


# Проверяет существование товара в таблице goods
def is_good_exists(good):
    result = db_session.query(Good).filter(Good.id == good).scalar()
    return result


# Проверяет существование пользователя в таблице users
def is_user_exists(user):
    result = db_session.query(User).filter(User.id == user).scalar()
    return result


# Возвращает ip страны, пользователи которой чаще всего посещают сайт
def get_freq_country():
    result = db_session.query(Action.ip).group_by(Action.ip).order_by(func.count(Action.ip).desc()).limit(1).scalar()
    return result


# Возвращает ip страны, пользователи которой чаще всего интересуются товарами из категории fresh_fish
def get_freq_country_fresh_fish():
    result = db_session.query(Action.ip).join(UsersAction, UsersAction.action_id == Action.id).filter(
        UsersAction.category_id == 1).group_by(Action.ip).order_by(func.count(Action.ip).desc()).limit(1).scalar()
    return result


# Возвращает количество не оплаченных корзин
def count_not_paid_carts():
    carts = db_session.query(func.count(Cart.id)).scalar()
    paid_carts = db_session.query(func.count(Payment.payment_status)).scalar()
    result = carts - paid_carts
    return result


# Возвращает количество пользователей совершавших повторные покупки
def get_amount_freq_users():
    result = db_session.query(func.count(Payment.user_id)).group_by(Payment.user_id).\
        having(func.count(Payment.user_id) > 1).all()
    return len(result)


if __name__ == '__main__':
    print(count_not_paid_carts())
