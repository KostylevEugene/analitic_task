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


if __name__ == '__main__':
    print(is_user_exists(81270149216))