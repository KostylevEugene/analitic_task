from db import db_session
from models import *



def get_category_id(cat):
    result = db_session.query(Category.id).filter(Category.category == cat).scalar()
    return result


# print(get_category_id('canned_food'))
