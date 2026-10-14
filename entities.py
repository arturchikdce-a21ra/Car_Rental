from abc import ABC, abstractmethod
from datetime import datetime


class Entity(ABC):

    @abstractmethod
    def info(self):
        pass


class Car(Entity):
    _id_counter = 0

    def __init__(self, brand, model, year, plate, price_per_day):
        Car._id_counter += 1
        self.__id = Car._id_counter
        self.__brand = brand
        self.__model = model
        self.__year = year
        self.__plate = plate
        self.__price_per_day = price_per_day
        self.__is_rented = False

    def get_id(self):
        return self.__id

    def get_brand(self):
        return self.__brand

    def set_brand(self, brand):
        self.__brand = brand

    def get_model(self):
        return self.__model

    def set_model(self, model):
        self.__model = model

    def get_year(self):
        return self.__year

    def set_year(self, year):
        self.__year = year

    def get_plate(self):
        return self.__plate

    def set_plate(self, plate):
        self.__plate = plate

    def get_price_per_day(self):
        return self.__price_per_day

    def set_price_per_day(self, price):
        self.__price_per_day = price

    def is_rented(self):
        return self.__is_rented

    def set_rented(self, value):
        self.__is_rented = value

    def get_full_name(self):
        return f"{self.__brand} {self.__model}"

    def info(self):
        return f"{self.get_full_name()} ({self.__plate}, {self.__year} г.)"

    def __eq__(self, other):
        return isinstance(other, Car) and self.__plate == other.__plate

    def __lt__(self, other):
        return self.__brand < other.__brand

    def __str__(self):
        return self.info()

    def __repr__(self):
        return f"Car({self.__brand} {self.__model}, {self.__plate})"

    def __len__(self):
        return len(self.get_full_name())


class Client(Entity):
    _id_counter = 0

    def __init__(self, name, phone, license_number):
        Client._id_counter += 1
        self.__id = Client._id_counter
        self.__name = name
        self.__phone = phone
        self.__license_number = license_number

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_phone(self):
        return self.__phone

    def set_phone(self, phone):
        self.__phone = phone

    def get_license_number(self):
        return self.__license_number

    def set_license_number(self, number):
        self.__license_number = number

    def info(self):
        return f"{self.__name} (тел: {self.__phone}, ВУ: {self.__license_number})"

    def __eq__(self, other):
        return isinstance(other, Client) and self.__license_number == other.__license_number

    def __lt__(self, other):
        return self.__name < other.__name

    def __str__(self):
        return self.info()

    def __repr__(self):
        return f"Client({self.__name})"

    def __len__(self):
        return len(self.__name)


class Rental(Entity):

    def __init__(self, client, car, start_time=None, end_time=None):
        self.__client = client
        self.__car = car
        self.__start_time = start_time or datetime.now()
        self.__end_time = end_time

    def get_client(self):
        return self.__client

    def get_car(self):
        return self.__car

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def set_end_time(self, time):
        self.__end_time = time

    def get_client_name(self):
        return self.__client.get_name()

    def get_car_name(self):
        return self.__car.get_full_name()

    def get_car_plate(self):
        return self.__car.get_plate()

    def get_duration_days(self):
        if self.__end_time:
            delta = self.__end_time - self.__start_time
            return max(1, delta.days)
        return 1

    def get_total_price(self):
        return self.get_duration_days() * self.__car.get_price_per_day()

    def is_active(self):
        return self.__end_time is None

    def info(self):
        return f"{self.__client.get_name()} -> {self.__car.get_full_name()}"

    def __eq__(self, other):
        return isinstance(other, Rental) and self.__client == other.__client and self.__car == other.__car

    def __lt__(self, other):
        return self.__start_time < other.__start_time

    def __str__(self):
        return self.info()

    def __repr__(self):
        return f"Rental({self.__client.get_name()}, {self.__car.get_full_name()})"

    def __len__(self):
        return self.get_duration_days()
