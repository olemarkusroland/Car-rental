import flask.scaffold
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import Flask
from flask_restful import Api

from customers import request_customers
from cars import request_cars
from relations import request_relations

Base = declarative_base()

class Customers(Base):
    __tablename__ = 'customers'

    # Standard columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(Integer)
    address = Column(String)
    # Navigation property
    car = relationship('Cars', back_populates='customer')


class Cars(Base):
    __tablename__ = 'cars'
    # Standard columns
    id = Column(Integer, primary_key=True)
    # Price class
    prize = Column(String)

    # Size class
    size = Column(String)

    # Vehicle identification number
    vin = Column(String)

    customer_id = Column(Integer, ForeignKey('customers.id'))
    # Navigation property
    customer = relationship('Customers', back_populates='car')


def main():
    app = Flask(__name__)
    api = Api(app)

    engine = create_engine('sqlite:///rental.sqlite')

    Session = sessionmaker(bind=engine)
    session_customers = Session()
    session_cars = Session()
    session_relation1 = Session()
    session_relation2 = Session()

    request_customers(session_customers, Customers, api)
    request_cars(session_cars, Cars, api)
    request_relations(session_relation1, Cars, Customers, api)

    app.run(debug=True)


if __name__ == '__main__':
    main()
