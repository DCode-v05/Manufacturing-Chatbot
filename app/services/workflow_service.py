import json

machines = json.load(open("app/data/machines.json"))
orders = json.load(open("app/data/orders.json"))

def get_machine_status(machine_id):
    return machines.get(machine_id, {"error": "Machine not found"})

def get_order_status(order_id):
    return orders.get(order_id, {"error": "Order not found"})
