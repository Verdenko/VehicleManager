import requests


class Vehicle:
    def __init__(self, name: str, model: str, year: int, color: str, price: int, latitude: float,
                 longitude: float, id=None, ):
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def __repr__(self):
        return f" <Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"


class VehicleManager:
    def __init__(self, url: str):
        self.url = url

    def get_vehicles(self):
        response = requests.get(self.url + "/vehicles")
        data = response.json()
        vehicles = []
        for item in data:
            vehicle = Vehicle(
                id=item['id'],
                name=item['name'],
                model=item['model'],
                year=item['year'],
                color=item['color'],
                price=item['price'],
                latitude=item['latitude'],
                longitude=item['longitude']
            )
            vehicles.append(vehicle)

        return print(vehicles)

    def filter_vehicles(self, params):
        response = requests.get(self.url + "/vehicles", params=params)
        vehicles = []

        for data in response.json():
            vehicles.append(
                Vehicle(
                    id=data['id'],
                    name=data['name'],
                    model=data['model'],
                    year=data['year'],
                    color=data['color'],
                    price=data['price'],
                    latitude=data['latitude'],
                    longitude=data['longitude']
                )
            )

        return print(vehicles)

    def get_vehicle_by_id(self, id: int):
        response = requests.get(self.url + f"/vehicles/{id}")
        data = response.json()
        return print(Vehicle(
            id=data['id'],
            name=data['name'],
            model=data['model'],
            year=data['year'],
            color=data['color'],
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        )

    def add_vehicle(self, vehicle_data: Vehicle):
        response = requests.post(f"{self.url}/vehicles", json=vehicle_data.__dict__())
        return response.status_code == 200

    def update_vehicle(self, vehicle_data: Vehicle):
        response = requests.put(self.url + f"/vehicles/{vehicle_data.id}", json=vehicle_data.__dict__())
        return response.status_code == 200

    def delete_vehicle(self, id: int):
        response = requests.delete(self.url + f"/vehicles/{id}")
        return response.status_code == 204


manager = VehicleManager(url="https://test.tspb.su/test-task")

manager.get_vehicles()

manager.filter_vehicles(params={"name": "Toyota"})

manager.get_vehicle_by_id(4)

manager.add_vehicle(
    vehicle_data=Vehicle(
        id=1,
        name='Toyota',
        model='Camry',
        year=2021,
        color='red',
        price=21000,
        latitude=55.753215,
        longitude=37.620393
    )
)
manager.update_vehicle(
    vehicle_data=Vehicle(
        id=1,
        name='Toyota',
        model='Camry',
        year=2021,
        color='red',
        price=21000,
        latitude=55.753215,
        longitude=37.620393
    )
)
manager.delete_vehicle(id=1)


