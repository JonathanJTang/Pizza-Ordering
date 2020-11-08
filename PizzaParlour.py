from flask import Flask, request

from cart import Cart
from order import Order

app = Flask("Assignment 2")

orders = {}
next_order_no = 1

@app.route('/pizza', methods=["GET","POST"])
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

def pizza_printer(pizza):
    print("{}".format(pizza))

@app.route('/api/orders', methods=["POST"])
def create_order():
    current_order_no = next_order_no
    next_order_no += 1

    try:
        order_data = request.get_json()
        print(order_data)
    except:
        pass  # just create an empty order?

    new_cart = Cart()
    orders[current_order_no] = Order(current_order_no, new_cart, None)
    return current_order_no

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def edit_order(order_id):
    return order_id

if __name__ == "__main__":
    app.run()
