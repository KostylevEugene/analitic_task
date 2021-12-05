from db import db_session
from models import *
from sqlalchemy.sql import func


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


def is_cart_exists(cart):
    result = db_session.query(Cart).filter(Cart.id == cart).scalar()
    return result


def is_good_exists(good):
    result = db_session.query(Good).filter(Good.id == good).scalar()
    return result


def is_user_exists(user):
    result = db_session.query(User).filter(User.id == user).scalar()
    return result


def get_freq_country():
    result = db_session.query(Action.ip).group_by(Action.ip).order_by(func.count(Action.ip).desc()).limit(1).scalar()
    return result


def get_freq_country_fresh_fish():
    result = db_session.query(Action.ip).join(UsersAction, UsersAction.action_id == Action.id).filter(
        UsersAction.category_id == 1).group_by(Action.ip).order_by(func.count(Action.ip).desc()).limit(1).scalar()
    return result


def count_not_paid_carts():
    result = db_session.query(func.count(Cart.id)).scalar() - db_session.query(func.count(Payment.payment_status)).\
        scalar()
    return result


def get_amount_freq_users():
    result = len(db_session.query(func.count(Payment.user_id)).group_by(Payment.user_id).\
        having(func.count(Payment.user_id) > 1).all())
    return result


if __name__ == '__main__':
    print(is_user_exists(81270149216))