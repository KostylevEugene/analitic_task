from db_eng import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey


''' В данном файле находится модель БД '''


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer(), primary_key=True)
    category = Column(String())

    def __init__(self, category):
        self.category = category

    def __repr__(self):
        return f'Category {self.category}'


class Good(Base):
    __tablename__ = 'goods'

    id = Column(Integer(), primary_key=True)
    good = Column(String())
    # category_id = Column(Integer(), ForeignKey(Category.id), index=True, nullable=False)
    # price = Column(Integer())
    # description = Column(String())

    def __init__(self, id):
        self.id = id
        # self.category_id = category_id
        # self.price = price
        # self.description = description

    def __repr__(self):
        return f'Good id {self.id}'


class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer(), primary_key=True)
    date = Column(String())
    time = Column(String())
    ip = Column(Integer())

    def __init__(self, date, time, ip):
        self.date = date
        self.time = time
        self.ip = ip

    def __repr__(self):
        return f'Action {self.ip}, {self.time}, {self.date}'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String)
    last_ip = Column(Integer())

    def __init__(self, id, last_ip):
        self.id = id
        # self.username = username
        self.last_ip = last_ip

    def __repr__(self):
        return f'User id {self.id} '


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer(), primary_key=True)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f'Cart {self.id}'



class GoodsInCart(Base):
    __tablename__ = 'goods_in_cart'

    id = Column(Integer(), primary_key=True)
    cart_id = Column(Integer(), ForeignKey(Cart.id), index=True, nullable=False)
    good_id = Column(Integer(), ForeignKey(Good.id), index=True, nullable=False)
    amount = Column(Integer())
    actions_id = Column(Integer(), ForeignKey(Action.id), index=True, nullable=False)

    def __init__(self, cart_id, good_id, amount, action_id):
        self.cart_id = cart_id
        self.good_id = good_id
        self.amount = amount
        self.actions_id = action_id

    def __repr__(self):
        return f'Cart {self.cart_id}, {self.good_id}, {self.amount}, {self.actions_id}'


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer(), primary_key=True)
    cart_id = Column(Integer(), ForeignKey(Cart.id), index=True, nullable=False)
    actions_id = Column(Integer(), ForeignKey(Action.id), index=True, nullable=False)
    user_id = Column(Integer(), ForeignKey(User.id), index=True, nullable=False)
    payment_status = Column(String())

    def __init__(self, cart_id, action_id, user_id, payment_status):
        self.cart_id = cart_id
        self.actions_id = action_id
        self.user_id = user_id
        self.payment_status = payment_status

    def __repr__(self):
        return f'Payment {self.cart_id}, {self.actions_id}, {self.user_id}, {self.payment_status}'


class UsersAction(Base):
    __tablename__ = 'usersactions'

    id = Column(Integer(), primary_key=True)
    action_id = Column(Integer(), ForeignKey(Action.id), index=True, nullable=False)
    category_id = Column(Integer(), ForeignKey(Category.id), index=True, nullable=False)

    def __init__(self, action_id, category_id):
        self.action_id = action_id
        self.category_id = category_id

    def __repr__(self):
        return f'UsersAction {self.action_id}, {self.category_id}'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
