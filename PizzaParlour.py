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
    """Receive an order made by a client."""
    global next_order_no
    current_order_no = next_order_no
    next_order_no += 1
    new_cart = Cart()

    try:
        order_data = request.get_json(silent=True)
        if order_data is None or order_data.get(
                "data_format") not in ("json_tree", "csv"):
            raise ValidationError("No valid JSON received")
        # Otherwise, we got a JSON object we can try to call validate() on
        if order_data["data_format"] == "json_tree":
            validate(order_data, data_formats.order_schema_json_tree)
            print("JSON validation success")
            parser = JsonParser()
            for product in parser.get_product_list(order_data):
                new_cart.add_product(product)
        elif order_data["data_format"] == "csv":
            validate(order_data, data_formats.order_schema_csv)
            # TODO: use CSV parser to add the products in
            # order_data["products"] to the cart
    except ValidationError as err:
        print(err)
        print("JSON validation failed")
        return "No valid JSON payload", 400
    except Exception as err:
        print(err)
        return "An error occurred on the server", 500

    orders[current_order_no] = Order(current_order_no, new_cart)
    response = {"order_no": current_order_no,
                "total_price": new_cart.get_total_price()}
    return jsonify(response)


@app.route('/api/orders/<int:order_no>', methods=['GET'])
def get_order(order_no):
    current_order = orders[order_no]
    return jsonify(current_order)


@app.route('/api/orders/<int:order_no>', methods=['PATCH'])
def edit_order(order_no):
    orders[order_no]
    return order_no


@app.route('/api/menu')
def get_full_menu():
    full_menu = {
        "pizza types": options.PIZZA_TYPE_TO_PRICE,
        "pizza sizes": options.PIZZA_SIZE_TO_PRICE,
        "pizza toppings": options.PIZZA_TOPPING_TO_PRICE,
        "drink types": options.DRINK_TYPE_TO_PRICE}
    return jsonify(full_menu)


@app.route('/api/menu/<str:item>', methods=['GET'])
def get_menu_item_price(item):
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
