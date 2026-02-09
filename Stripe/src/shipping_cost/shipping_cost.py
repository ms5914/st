##part 1
from email.policy import default
from collections import defaultdict

order_us = {
    "country": "US",
    "items": [
        {"product": "mouse", "quantity": 20},
        {"product": "laptop", "quantity": 5}
    ]
}

order_ca = {
    "country": "CA",
    "items": [
        {"product": "mouse", "quantity": 20},
        {"product": "laptop", "quantity": 5}
    ]
}

shipping_cost = {
    "US": [
        {"product": "mouse", "cost": 550},
        {"product": "laptop", "cost": 1000}
    ],
    "CA": [
        {"product": "mouse", "cost": 750},
        {"product": "laptop", "cost": 1100}
    ]
}


def calculate_shipping_cost(order, shipping_cost):
    product_costs = defaultdict(int)
    for product_cost in shipping_cost[ order["country"]]:
        product_costs[product_cost["product"]] = product_cost["cost"]

    total_cost = 0
    for item in order["items"]:
        product = item["product"]
        quantity = item["quantity"]
        total_cost+=product_costs[product]*quantity

    return total_cost
print(calculate_shipping_cost(order_us, shipping_cost))

#Part 2: Tiered pricing

shipping_cost = {
    "US": [
        {
            "product": "mouse",
            "costs": [
                {"minQuantity": 0, "maxQuantity": None, "cost": 550}
            ]
        },
        {
            "product": "laptop",
            "costs": [
                {"minQuantity": 0, "maxQuantity": 2, "cost": 1000},
                {"minQuantity": 3, "maxQuantity": None, "cost": 900}
            ]
        }
    ],
    "CA": [
        {
            "product": "mouse",
            "costs": [
                {"minQuantity": 0, "maxQuantity": None, "cost": 750}
            ]
        },
        {
            "product": "laptop",
            "costs": [
                {"minQuantity": 0, "maxQuantity": 2, "cost": 1100},
                {"minQuantity": 3, "maxQuantity": None, "cost": 1000}
            ]
        }
    ]
}



def calculate_shipping_cost(order, shipping_cost):
    product_costs = defaultdict(list)
    for product_cost in shipping_cost[order["country"]]:
        product_costs[product_cost["product"]] = product_cost["costs"]

    total_cost = 0
    for item in order["items"]:
        product = item["product"]
        quantity = item["quantity"]
        per_product_cost = 0
        for cost_tier in product_costs[product]:
            min_quantity, max_quantity, cost = cost_tier["minQuantity"], cost_tier["maxQuantity"], cost_tier["cost"]
            if max_quantity is None:
                purchased = quantity
            else:
                capacity = max_quantity - min_quantity
                purchased = min(capacity, quantity)
            quantity-=purchased
            per_product_cost+=purchased*cost
            if quantity == 0:
                break
        total_cost+=per_product_cost
    return total_cost


print(calculate_shipping_cost(order_us, shipping_cost))
print(calculate_shipping_cost(order_ca, shipping_cost))



#Part 3: Mixed Pricing Types

shipping_cost = {
    "US": [
        {
            "product": "mouse",
            "costs": [
                {
                    "type": "incremental",
                    "minQuantity": 0,
                    "maxQuantity": None,
                    "cost": 550
                }
            ]
        },
        {
            "product": "laptop",
            "costs": [
                {
                    "type": "fixed",
                    "minQuantity": 0,
                    "maxQuantity": 2,
                    "cost": 1000
                },
                {
                    "type": "incremental",
                    "minQuantity": 3,
                    "maxQuantity": None,
                    "cost": 900
                }
            ]
        }
    ],
    "CA": [
        {
            "product": "mouse",
            "costs": [
                {
                    "type": "incremental",
                    "minQuantity": 0,
                    "maxQuantity": None,
                    "cost": 750
                }
            ]
        },
        {
            "product": "laptop",
            "costs": [
                {
                    "type": "fixed",
                    "minQuantity": 0,
                    "maxQuantity": 2,
                    "cost": 1100
                },
                {
                    "type": "incremental",
                    "minQuantity": 3,
                    "maxQuantity": None,
                    "cost": 1000
                }
            ]
        }
    ]
}
def calculate_shipping_cost(order, shipping_cost):
    product_costs = defaultdict(list)
    for product_cost in shipping_cost[order["country"]]:
        product_costs[product_cost["product"]] = product_cost["costs"]

    total_cost = 0
    for item in order["items"]:
        product = item["product"]
        quantity = item["quantity"]
        per_product_cost = 0
        for cost_tier in product_costs[product]:
            min_quantity, max_quantity, cost, type = cost_tier["minQuantity"], cost_tier["maxQuantity"], cost_tier["cost"], cost_tier["type"]
            if max_quantity is None:
                purchased = quantity
            else:
                capacity = max_quantity - min_quantity
                purchased = min(capacity, quantity)
            quantity-=purchased
            if purchased:
                per_product_cost+=purchased*cost if type == "incremental" else cost
        total_cost+=per_product_cost
    return total_cost


print(calculate_shipping_cost(order_us, shipping_cost))
print(calculate_shipping_cost(order_ca, shipping_cost))




