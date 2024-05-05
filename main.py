from classes import Vehicle, VehicleManager

manager = VehicleManager(url="https://test.tspb.su/test-task")

print(manager.get_vehicles())

print(manager.filter_vehicles(params={"price": 30000}))

print(manager.filter_vehicles(params={"name": "Toyota"}))

print(manager.get_vehicle(vehicle_id=4))

print(manager.add_vehicle(
    vehicle_data=Vehicle(
        id=21,
        name='Toyota',
        model='Camry',
        year=2021,
        color='red',
        price=21000,
        latitude=55.753215,
        longitude=37.620393
    )
)
)
print(manager.update_vehicle(
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
)
print(manager.delete_vehicle(vehicle_id=1))

print(manager.get_distance(4, 7))

print(manager.get_nearest_vehicle(4))
