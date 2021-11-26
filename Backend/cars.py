import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import *

def json_cars(session, Cars):
    cars = session.query(Cars).all()

    cars_array = []

    for car in cars:
        car_json_formatted = dict(id=car.id, prize=car.prize, size=car.size, vin=car.vin, customer_id=car.customer_id)

        cars_array.append(car_json_formatted)

    session.close()
    return cars_array

def request_cars(session, Cars, api):
    json_cars(session, Cars)

    class CarList(Resource):
        def get(self):
            session.close()
            return json_cars(session, Cars), 200

        def post(self):
            car_input = request.get_json()

            if car_input['prize'] == "" or car_input['size'] == "" or car_input['vin'] == "":
                raise NotAcceptable("Input can not be empty")

            car = Cars(prize=car_input['prize'], size=car_input['size'], vin=car_input['vin'])

            session.add(car)

            session.commit()
            session.close()
            return 201

    class Car(Resource):
        def get(self, id):
            car = session.query(Cars).filter(Cars.id == id).first()
            if car is None:
                raise NotFound("Car not found")

            car_json_formatted = dict(id=car.id, prize=car.prize, size=car.size, vin=car.vin,
                                      customer_id=car.customer_id)

            session.close()
            return car_json_formatted, 200

        def put(self, id):
            car = session.query(Cars).filter(Cars.id == id).first()
            if car is None:
                raise NotFound("Car not found")

            car_input = request.get_json()

            if car_input['id'] != "":
                car.id = car_input['id']
            if car_input['prize'] != "":
                car.prize = car_input['prize']
            if car_input['size'] != "":
                car.size = car_input['size']
            if car_input['vin'] != "":
                car.vin = car_input['vin']
            if car_input['customer_id'] != "":
                car.customer_id = car_input['customer_id']

            session.commit()
            session.close()
            return 201

        def delete(self, id):
            car = session.query(Cars).filter(Cars.id == id).first()
            if car is None:
                raise NotFound("Car not found")

            session.delete(car)

            session.commit()
            session.close()
            return 204

    api.add_resource(CarList, '/cars/')
    api.add_resource(Car, '/cars/<id>')
