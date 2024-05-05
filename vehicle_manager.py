import requests
import math


class Vehicle:
    def __init__(self, name: str, model: str, year: int, color: str, price: int, latitude: float,
                 longitude: float, id: int = 1):
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

        return vehicles

    def filter_vehicles(self, params: dict):
        response = requests.get(self.url + "/vehicles", params=params)
        vehicles = []
        data = response.json()
        for vehicle in data:
            match = True

            for key, value in params.items():
                if key not in vehicle or vehicle[key] != value:
                    match = False
                    break
            if match:
                vehicles.append(
                    Vehicle(
                        id=vehicle['id'],
                        name=vehicle['name'],
                        model=vehicle['model'],
                        year=vehicle['year'],
                        color=vehicle['color'],
                        price=vehicle['price'],
                        latitude=vehicle['latitude'],
                        longitude=vehicle['longitude']
                    )
                )

        return vehicles

    def get_vehicle(self, vehicle_id: int):
        response = requests.get(self.url + f"/vehicles/{vehicle_id}")
        data = response.json()

        if 'error' in data:
            raise Exception("Ошибка при получении данных о транспортном средстве")

        return Vehicle(
            id=data['id'],
            name=data['name'],
            model=data['model'],
            year=data['year'],
            color=data['color'],
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )

    def add_vehicle(self, vehicle_data: Vehicle):
        response = requests.post(f"{self.url}/vehicles", json=vehicle_data.__dict__())
        return response.status_code == 201

    def update_vehicle(self, vehicle_data: Vehicle):
        response = requests.put(self.url + f"/vehicles/{vehicle_data.id}", json=vehicle_data.__dict__())
        return response.status_code == 200

    def delete_vehicle(self, vehicle_id: int):
        response = requests.delete(self.url + f"/vehicles/{vehicle_id}")
        return response.status_code == 204

    def get_distance(self, id1: int, id2: int):
        earth_radius = 6371000

        vehicle1 = self.get_vehicle(vehicle_id=id1)
        vehicle2 = self.get_vehicle(vehicle_id=id2)

        delta_lat = math.radians(vehicle1.latitude - vehicle2.latitude)
        delta_lon = math.radians(vehicle1.longitude - vehicle2.longitude)

        a = (math.sin(delta_lat / 2) ** 2 + math.cos(math.radians(vehicle1.latitude)) *
             math.cos(math.radians(vehicle2.latitude)) * math.sin(delta_lon / 2) ** 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = earth_radius * c

        return round(distance,3)

    def get_nearest_vehicle(self, vehicle_id: int):
        vehicles = self.get_vehicles()
        min_distance: float = 40075000
        nearest_vehicle: Vehicle = self.get_vehicle(vehicle_id)
        vehicles.pop(vehicle_id - 1)

        for vehicle in vehicles:
            if str(vehicle.id) == str(vehicle_id):
                continue

            distance = self.get_distance(vehicle_id, vehicle.id)

            if distance < min_distance:
                min_distance = distance
                nearest_vehicle = vehicle

        return nearest_vehicle
