from tkinter import *
import requests


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()

        self.main_menu()

    def main_menu(self):
        menubar = Menu(self.master)

        customer_menu = Menu(menubar, tearoff=0)
        car_menu = Menu(menubar, tearoff=0)
        relation_menu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label="Customers", menu=customer_menu)
        menubar.add_cascade(label="Cars", menu=car_menu)
        menubar.add_cascade(label="Relations", menu=relation_menu)

        customer_menu.add_command(label='View all', command=self.view_customers)
        customer_menu.add_command(label='Add', command=self.add_customer)
        customer_menu.add_command(label='Edit', command=self.edit_customer)
        customer_menu.add_command(label='Remove', command=self.remove_customer)

        car_menu.add_command(label='View all', command=self.view_cars)
        car_menu.add_command(label='Add', command=self.add_car)
        car_menu.add_command(label='Edit', command=self.edit_car)
        car_menu.add_command(label='Remove', command=self.remove_car)

        relation_menu.add_command(label='View all', command=self.view_relations)
        relation_menu.add_command(label='Assign car', command=self.assign)
        relation_menu.add_command(label='Unassign car', command=self.unassign)

        self.master.config(menu=menubar)

    def response_window(self, response):
        response_window = Tk()
        response_window.title("HTTP response")
        response_window.geometry('+400+360')

        Label(response_window, text=f"HTTP response: {response.status_code}").grid(row=0, column=0, columnspan=2,
                                                                                   sticky="ew")
        response_window.btn_submit = Button(response_window, text='OK', command=response_window.destroy)
        response_window.btn_submit.grid(row=1, column=0, columnspan=2, sticky="ew")

    def error_window(self, error):
        error_window = Tk()
        error_window.title("ERROR")
        error_window.geometry('+400+360')

        Label(error_window, text=error).grid(row=0, column=0, columnspan=2, sticky="ew")
        error_window.btn_submit = Button(error_window, text='OK', command=error_window.destroy)
        error_window.btn_submit.grid(row=1, column=0, columnspan=2, sticky="ew")

    def view_customers(self):
        window = Tk()
        window.title("Customers")
        window.geometry('+400+330')

        response = requests.get('http://localhost:5000/customers/')
        if response.status_code != 200:
            self.response_window(response)
        else:

            customers = response.json()

            Label(window, text='id     ').grid(row=0, column=0, sticky='w')
            Label(window, text='Name   ').grid(row=0, column=1, sticky='w')
            Label(window, text='Phone  ').grid(row=0, column=2, sticky='w')
            Label(window, text='Address').grid(row=0, column=3, sticky='w')

            i = 1
            for customer in customers:
                Label(window, text=customer['id']).grid(row=i, column=0, sticky='w')
                Label(window, text=customer['name']).grid(row=i, column=1, sticky='w')
                Label(window, text=customer['phone']).grid(row=i, column=2, sticky='w')
                Label(window, text=customer['address']).grid(row=i, column=3, sticky='w')
                i += 1

    def add_customer(self):
        window = Tk()
        window.title("Add customer")
        window.geometry('+400+330')

        Label(window, text='Name:').grid(row=0, column=0)
        Label(window, text='Phone:').grid(row=1, column=0)
        Label(window, text='Address:').grid(row=2, column=0)

        self.name_entry = Entry(window)
        self.phone_entry = Entry(window)
        self.address_entry = Entry(window)

        self.name_entry.grid(row=0, column=1)
        self.phone_entry.grid(row=1, column=1)
        self.address_entry.grid(row=2, column=1)

        window.btn_submit = Button(window, text='Submit', command=self.submit_add_customer)
        window.btn_submit.grid(row=3, column=0, columnspan=2, sticky="ew")

    def submit_add_customer(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()

        if name == "" or phone == "" or address == "" or name.isspace() or phone.isspace() or address.isspace():
            self.error_window("Inputs can not be empty")
        else:

            json_formatted = dict(name=name, phone=phone, address=address)

            response = requests.post('http://localhost:5000/customers/', json=json_formatted)
            if response.status_code != 200:
                self.response_window(response)

    def edit_customer(self):
        window = Tk()
        window.title("Edit customer")
        window.geometry('+400+330')

        Label(window, text='id:').grid(row=0, column=0)
        Label(window, text='Name:').grid(row=1, column=0)
        Label(window, text='Phone:').grid(row=2, column=0)
        Label(window, text='Address:').grid(row=3, column=0)

        self.id_entry = Entry(window)
        self.name_entry = Entry(window)
        self.phone_entry = Entry(window)
        self.address_entry = Entry(window)

        self.id_entry.grid(row=0, column=1)
        self.name_entry.grid(row=1, column=1)
        self.phone_entry.grid(row=2, column=1)
        self.address_entry.grid(row=3, column=1)

        window.btn_submit = Button(window, text='Submit', command=self.submit_edit_customer)
        window.btn_submit.grid(row=4, column=0, columnspan=2, sticky="ew")

    def submit_edit_customer(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()

        if id == "" or id.isspace():
            self.error_window("id field can not be empty")
        else:

            json_formatted = dict(name=name, phone=phone, address=address)

            response = requests.put('http://localhost:5000/customers/' + str(id), json=json_formatted)
            if response.status_code != 200:
                self.response_window(response)

    def remove_customer(self):
        window = Tk()
        window.title("Remove customer")
        window.geometry('+400+330')

        Label(window, text='Customer id:').grid(row=0, column=0)

        self.id_entry = Entry(window)

        self.id_entry.grid(row=0, column=1)

        window.btn_submit = Button(window, text='Submit', command=self.submit_remove_customer)
        window.btn_submit.grid(row=1, column=0, columnspan=2, sticky="ew")

    def submit_remove_customer(self):
        id = self.id_entry.get()

        if id == "" or id.isspace():
            self.error_window("Input can not be empty")
        else:

            response = requests.delete('http://localhost:5000/customers/' + str(id))
            if response.status_code != 200:
                self.response_window(response)

    def view_cars(self):
        window = Tk()
        window.title("Cars")
        window.geometry('+400+330')

        response = requests.get('http://localhost:5000/cars/')
        if response.status_code != 200:
            self.response_window(response)
        else:

            cars = response.json()

            Label(window, text='id         ').grid(row=0, column=0, sticky='w')
            Label(window, text='Prize      ').grid(row=0, column=1, sticky='w')
            Label(window, text='Size       ').grid(row=0, column=2, sticky='w')
            Label(window, text='VIN        ').grid(row=0, column=3, sticky='w')
            Label(window, text='Customer id').grid(row=0, column=4, sticky='w')

            i = 1
            for car in cars:
                Label(window, text=car['id']).grid(row=i, column=0, sticky='w')
                Label(window, text=car['prize']).grid(row=i, column=1, sticky='w')
                Label(window, text=car['size']).grid(row=i, column=2, sticky='w')
                Label(window, text=car['vin']).grid(row=i, column=3, sticky='w')
                Label(window, text=car['customer_id']).grid(row=i, column=4, sticky='w')
                i += 1

    def add_car(self):
        window = Tk()
        window.title("Add car")
        window.geometry('+400+330')

        Label(window, text='Prize:').grid(row=0, column=0)
        Label(window, text='Size:').grid(row=1, column=0)
        Label(window, text='VIN:').grid(row=2, column=0)

        self.prize_entry = Entry(window)
        self.size_entry = Entry(window)
        self.vin_entry = Entry(window)

        self.prize_entry.grid(row=0, column=1)
        self.size_entry.grid(row=1, column=1)
        self.vin_entry.grid(row=2, column=1)

        window.btn_submit = Button(window, text='Submit', command=self.submit_add_car)
        window.btn_submit.grid(row=3, column=0, columnspan=2, sticky="ew")

    def submit_add_car(self):
        prize = self.prize_entry.get()
        size = self.size_entry.get()
        vin = self.vin_entry.get()

        if prize == "" or size == "" or vin == "" or prize.isspace() or size.isspace() or vin.isspace():
            self.error_window("Input can not be empty")
        else:

            json_formatted = dict(prize=prize, size=size, vin=vin)

            response = requests.post('http://localhost:5000/cars/', json=json_formatted)
            if response.status_code != 200:
                self.response_window(response)

    def edit_car(self):
        window = Tk()
        window.title("Edit car")
        window.geometry('+400+330')

        Label(window, text='id:').grid(row=0, column=0)
        Label(window, text='Price class:').grid(row=1, column=0)
        Label(window, text='Size class:').grid(row=2, column=0)
        Label(window, text='VIN:').grid(row=3, column=0)

        self.id_entry = Entry(window)
        self.prize_entry = Entry(window)
        self.size_entry = Entry(window)
        self.vin_entry = Entry(window)

        self.id_entry.grid(row=0, column=1)
        self.prize_entry.grid(row=1, column=1)
        self.size_entry.grid(row=2, column=1)
        self.vin_entry.grid(row=3, column=1)

        window.btn_submit = Button(window, text='Submit', command=self.submit_edit_car)
        window.btn_submit.grid(row=4, column=0, columnspan=2, sticky="ew")

    def submit_edit_car(self):
        id = self.id_entry.get()
        size = self.size_entry.get()
        prize = self.prize_entry.get()
        vin = self.vin_entry.get()

        if id == "" or id.isspace():
            self.error_window("id field can not be empty")
        else:

            get_response = requests.get('http://localhost:5000/cars/' + str(id))
            if get_response.status_code != 200:
                self.response_window(get_response)
            else:
                car = get_response.json()

                json_formatted = dict(id=car['id'], size=size, prize=prize, vin=vin, customer_id=car['customer_id'])

                response = requests.put('http://localhost:5000/cars/' + str(id), json=json_formatted)
                if response.status_code != 200:
                    self.response_window(response)

    def remove_car(self):
        window = Tk()
        window.title("Remove car")
        window.geometry('+400+330')

        Label(window, text='Car id:').grid(row=0, column=0)

        self.id_entry = Entry(window)

        self.id_entry.grid(row=0, column=1)

        window.btn_submit = Button(window, text='Submit', command=self.submit_remove_car)
        window.btn_submit.grid(row=1, column=0, columnspan=2, sticky="ew")

    def submit_remove_car(self):
        id = self.id_entry.get()

        if id == "" or id.isspace():
            self.error_window("Input can not be empty")
        else:

            response = requests.delete('http://localhost:5000/cars/' + str(id))
            if response.status_code != 200:
                self.response_window(response)

    def view_relations(self):
        window = Tk()
        window.title("Relations")
        window.geometry('+400+330')

        response = requests.get('http://localhost:5000/relations/')
        if response.status_code != 200:
            self.response_window(response)
        else:

            relations = response.json()

            Label(window, text='Car id     ').grid(row=0, column=0, sticky='w')
            Label(window, text='Customer id').grid(row=0, column=1, sticky='w')

            i = 1
            for relation in relations:
                Label(window, text=relation['car_id']).grid(row=i, column=0, sticky='w')
                Label(window, text=relation['customer_id']).grid(row=i, column=1, sticky='w')
                i += 1

    def assign(self):
        window = Tk()
        window.title("Assign")
        window.geometry('+400+330')

        Label(window, text='Car id:').grid(row=0, column=0)
        Label(window, text='Customer id:').grid(row=1, column=0)

        self.car_id_entry = Entry(window)
        self.customer_id_entry = Entry(window)

        self.car_id_entry.grid(row=0, column=1)
        self.customer_id_entry.grid(row=1, column=1)

        window.btn_submit = Button(window, text='Submit', command=self.submit_assign)
        window.btn_submit.grid(row=2, column=0, columnspan=2, sticky="ew")

    def submit_assign(self):
        car_id = self.car_id_entry.get()
        customer_id = self.customer_id_entry.get()

        if car_id == "" or customer_id == "" or car_id.isspace() or customer_id.isspace():
            self.error_window("Inputs can not be empty")
        else:

            get_customer_response = requests.get('http://localhost:5000/customers/' + str(customer_id))
            if get_customer_response.status_code != 200:
                self.response_window(get_customer_response)
            else:

                get_car_response = requests.get('http://localhost:5000/cars/' + str(car_id))
                if get_car_response.status_code != 200:
                    self.response_window(get_car_response)
                else:

                    car = get_car_response.json()

                    car_json_formatted = dict(id=car["id"], prize=car["prize"], size=car["size"], vin=car["vin"],
                                              customer_id=customer_id)

                    response = requests.put('http://localhost:5000/cars/' + str(car_id), json=car_json_formatted)
                    if response.status_code != 200:
                        self.response_window(response)

    def unassign(self):
        window = Tk()
        window.title("Unassign")
        window.geometry('+400+330')

        Label(window, text='Car id:').grid(row=0, column=0)

        self.id_entry = Entry(window)

        self.id_entry.grid(row=0, column=1)

        window.btn_submit = Button(window, text='Submit', command=self.submit_unassign)
        window.btn_submit.grid(row=1, column=0, columnspan=2, sticky="ew")

    def submit_unassign(self):
        id = self.id_entry.get()

        if id == "" or id.isspace():
            self.error_window("Input can not be empty")
        else:

            get_car_response = requests.get('http://localhost:5000/cars/' + str(id))
            if get_car_response.status_code != 200:
                self.response_window(get_car_response)
            else:

                car = get_car_response.json()

                car_json_formatted = dict(id=car["id"], prize=car["prize"], size=car["size"], vin=car["vin"],
                                          customer_id=None)

                response = requests.put('http://localhost:5000/cars/' + str(id), json=car_json_formatted)
                if response.status_code != 200:
                    self.response_window(response)


def main():
    root = Tk()
    root.title("Database")
    root.geometry('177x0+400+330')
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
