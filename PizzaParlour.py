from csv_parser import CsvParser
from flask import Flask, jsonify, request
from jsonschema import ValidationError, validate

import data_formats
import options
from cart import Cart
from drink import Drink
from json_parser import JsonParser
from order import Order
from pizza import Pizza

app = Flask("Assignment 2")

orders = {}
next_order_no = 1


def valid_order_no(order_no):
    """Return True iff order_no is a valid order number, ie the order number of
    an order placed in this session of the server."""
    return order_no in orders


@app.route('/pizza', methods=["GET", "POST"])
def welcome_pizza():
    """ We will put order to server or get the current order from server
    in order to modify it."""
    try:
        if request.method == "GET":  # We want to change
            print("Got GET request")
            request.args.get("name")
        elif request.method == "POST":
            print("Got POST request")
            # request.files.
    except Exception:
        pass  # fail silently for now
    return 'Welcome to Pizza Planet!'


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
    if not valid_order_no(order_no):
        return "Not a valid order number", 404
    # TODO: complete edit_order

    return "Successfully edited order {}".format(order_no)


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
            validate(order_data, data_formats.order_schema_json_tree)
            print("JSON validation success")
            for product in JsonParser().get_product_list(order_data):
                order.get_cart().add_product(product)
        elif order_data["data_format"] == "csv":
            validate(order_data, data_formats.order_schema_csv)
            for product in CsvParser().get_product_list(
                    order_data["csv_string"]):
                order.get_cart().add_product(product)
    except ValidationError as err:
        print(err)
        print("JSON validation failed")
        return "No valid JSON payload", 400
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
    Drink.set_type_to_price(options.DRINK_TYPE_TO_PRICE)
    Pizza.set_type_to_price(options.PIZZA_TYPE_TO_PRICE)
    Pizza.set_size_to_price(options.PIZZA_SIZE_TO_PRICE)
    Pizza.set_topping_to_price(options.PIZZA_TOPPING_TO_PRICE)
    app.run()
