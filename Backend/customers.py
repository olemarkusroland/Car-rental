import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import *

def json_customers(session, Customers):
    customers = session.query(Customers).all()

    customers_array = []

    for customer in customers:
        customer_json_formatted = dict(id=customer.id, name=customer.name, phone=customer.phone,
                                       address=customer.address)

        customers_array.append(customer_json_formatted)

    session.close()
    return customers_array

def request_customers(session, Customers, api):
    json_customers(session, Customers)

    class CustomerList(Resource):
        def get(self):
            session.close()
            return json_customers(session, Customers), 200

        def post(self):
            customer_input = request.get_json()

            if customer_input['name'] == "" or customer_input['phone'] == "" or customer_input['address'] == "":
                raise NotAcceptable("Input can not be empty")

            customer = Customers(name=customer_input['name'], phone=customer_input['phone'],
                                 address=customer_input['address'])

            session.add(customer)

            session.commit()
            session.close()
            return 201

    class Customer(Resource):
        def get(self, id):
            customer = session.query(Customers).filter(Customers.id == id).first()
            if customer is None:
                raise NotFound("Customer not found")

            customer_json_formatted = dict(id=customer.id, name=customer.name, phone=customer.phone,
                                          address=customer.address)

            session.close()
            return customer_json_formatted, 200

        def put(self, id):
            customer = session.query(Customers).filter(Customers.id == id).first()
            if customer is None:
                raise NotFound("Customer not found")

            customer_input = request.get_json()

            if customer_input['name'] != "":
                customer.name = customer_input['name']
            if customer_input['phone'] != "":
                customer.phone = customer_input['phone']
            if customer_input['address'] != "":
                customer.address = customer_input['address']

            session.commit()
            session.close()
            return 201

        def delete(self, id):
            customer = session.query(Customers).filter(Customers.id == id).first()
            if customer is None:
                raise NotFound("Customer not found")

            session.delete(customer)

            session.commit()
            session.close()
            return 204

    api.add_resource(CustomerList, '/customers/')
    api.add_resource(Customer, '/customers/<id>')
