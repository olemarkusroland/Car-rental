import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import *


def request_relations(session, Cars, Customers, api):
    class RelationList(Resource):
        def get(self):
            cars = session.query(Cars).all()
            if cars is None:
                raise NotFound("Car not found")

            relations = []

            for car in cars:
                if car.customer_id is not None:
                    relations_json_format = dict(car_id=car.id, customer_id=car.customer_id)

                    relations.append(relations_json_format)

            session.close()
            return relations, 200

    class Relation(Resource):
        def get(self, id):
            car = session.query(Cars).filter(Cars.id == id).first()
            if car is None:
                raise NotFound("Car not found")

            relation_json_formatted = dict(car_id=car.id, customer_id=car.customer_id)

            session.close()
            return relation_json_formatted, 200

        def put(self, id):
            customer = session.query(Customers).filter(Customers.id == id).first()
            if customer is None:
                raise NotFound("Car with specified id not found")
            session.close()

            car = session.query(Cars).filter(Cars.id == id).one()
            if car is None:
                raise NotFound("Car with specified id not found")

            car_input = request.get_json()

            car.customer_id = car_input['customer_id']

            session.commit()
            session.close()
            return 201

        def delete(self, id):
            car = session.query(Cars).filter(Cars.id == id).first()
            if car is None:
                raise NotFound("Car not found")

            car.customer_id = None

            session.commit()
            session.close()
            return 204

    api.add_resource(RelationList, '/relations/')
    api.add_resource(Relation, '/relations/<id>')
