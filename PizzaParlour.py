import json

from flask import Flask, jsonify, request
from jsonschema import ValidationError, validate

import options
from cart import Cart
from csv_parser import CsvParser
from drink import Drink
from invalid_option_error import InvalidOptionError
from json_parser import JsonParser
from order import Order
from pizza import Pizza

app = Flask("Assignment 2")

# orders is a dictionary that will hold all the orders received in this
# session
orders = {}
# next_order_no keeps track of the next order number to assign for a new order
next_order_no = 1

# Load json schemas
with open("edit_order_schema.json") as schema:
    edit_order_schema = json.load(schema)
with open("order_schema_json.json") as schema:
    order_schema_json_tree = json.load(schema)
with open("order_schema_csv.json") as schema:
    order_schema_csv = json.load(schema)


def valid_order_no(order_no):
    """Return True iff order_no is a valid order number, ie the order number of
    an order placed in this session of the server."""
    return order_no in orders

@app.route('/api/orders', methods=["POST"])
def create_order():
    """Receive an order made by a client, and return the assigned order
    number."""
    global next_order_no
    # Create an Order object for this order.
    current_order_no = next_order_no
    next_order_no += 1
    orders[current_order_no] = Order(current_order_no, Cart())
    return str(current_order_no)


@app.route('/api/orders/<int:order_no>', methods=['GET'])
def get_order(order_no):
    """Return the products in the order given by order_no. Returns a 404 status
    code if order_no is not a valid order number."""
    if not valid_order_no(order_no):
        return "Not a valid order number", 404
    parser = JsonParser()
    return parser.get_json(orders[order_no].get_cart().get_products())


@app.route('/api/orders/<int:order_no>', methods=['PATCH'])
def edit_order(order_no):
    """Edit the order at order_no with the received data, where the data only
    specifies the attributes that need to be changed. Return the new total price
    of the order."""
    if not valid_order_no(order_no):
        return "Not a valid order number", 404
    order = orders[order_no]
    try:
        edit_data = request.get_json(silent=True)
        if edit_data is None:
            raise ValidationError("No valid JSON received")
        # Otherwise, we got a JSON object we can try to call validate() on
        print(edit_data)
        validate(edit_data, edit_order_schema)
        print("JSON validation success")
        cart = order.get_cart()
        for change in edit_data:
            cart_item_id = change.pop("cart_item_id")
            if change.pop("remove", None) is None:
                cart.edit_product(cart_item_id, change)
            else:
                cart.remove_product(cart_item_id)
    except ValidationError as err:
        # JSON payload not valid according to our JSON schema
        print(err)
        return "No valid JSON payload", 400
    except InvalidOptionError as err:
        # JSON payload contained an invalid product option
        print(err)
        return "JSON payload contained invalid option for a product", 400
    except Exception as err:
        print(err)
        return "An error occurred on the server", 500
    return str(order.get_cart().get_total_price())


@app.route('/api/orders/<int:order_no>', methods=['PUT'])
def replace_order(order_no):
    """Replace the order at order_no with the received data. Returns a 404
    status code if order_no is not a valid order number."""
    if not valid_order_no(order_no):
        return "Not a valid order number", 404
    order = orders[order_no]
    try:
        order_data = request.get_json(silent=True)
        if order_data is None or order_data.get(
                "data_format") not in ("json_tree", "csv"):
            raise ValidationError("No valid JSON received")
        # Otherwise, we got a JSON object we can try to call validate() on
        if order_data["data_format"] == "json_tree":
            validate(order_data, order_schema_json_tree)
            for product in JsonParser().get_product_list(order_data):
                order.get_cart().add_product(product)
        elif order_data["data_format"] == "csv":
            validate(order_data, order_schema_csv)
            for product in CsvParser().get_product_list(
                    order_data["csv_string"]):
                order.get_cart().add_product(product)
    except ValidationError as err:
        # JSON payload not valid according to our JSON schema
        print(err)
        return "No valid JSON payload", 400
    except InvalidOptionError as err:
        # JSON payload contained an invalid product option
        print(err)
        return "JSON payload contained invalid option for a product", 400
    except Exception as err:
        print(err)
        return "An error occurred on the server", 500
    return jsonify({"total_price": order.get_cart().get_total_price()})


@app.route('/api/orders/<int:order_no>', methods=['DELETE'])
def cancel_order(order_no):
    """Cancel the order given by order_no. Returns a 404 status code if order_no
    is not a valid order number."""
    if not valid_order_no(order_no):
        return "Not a valid order number", 404
    # Remove the order from memory
    del orders[order_no]
    return "Successfully deleted order {}".format(order_no)


@app.route('/api/menu')
def get_full_menu():
    full_menu = {
        "pizza types": options.PIZZA_TYPE_TO_PRICE,
        "pizza sizes": options.PIZZA_SIZE_TO_PRICE,
        "pizza toppings": options.PIZZA_TOPPING_TO_PRICE,
        "drink types": options.DRINK_TYPE_TO_PRICE}
    return jsonify(full_menu)


@app.route('/api/menu/<string:item>', methods=['GET'])
def get_menu_item_price(item):
    item = item.upper()  # Dictionaries here use uppercase keys
    price = options.DRINK_TYPE_TO_PRICE.get(item)
    if price is not None:
        return jsonify(price)
    price = options.PIZZA_TYPE_TO_PRICE.get(item)
    if price is not None:
        return jsonify(price)
    price = options.PIZZA_TOPPING_TO_PRICE.get(item)
    if price is not None:
        return jsonify(price)
    return "Not a valid menu item", 400


if __name__ == "__main__":
    # Set options
    Drink.set_type_to_price(options.DRINK_TYPE_TO_PRICE)
    Pizza.set_type_to_price(options.PIZZA_TYPE_TO_PRICE)
    Pizza.set_size_to_price(options.PIZZA_SIZE_TO_PRICE)
    Pizza.set_topping_to_price(options.PIZZA_TOPPING_TO_PRICE)

    app.run()
