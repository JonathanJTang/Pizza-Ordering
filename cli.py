import click
import requests
from click_shell import shell

BASE_URL = "http://127.0.0.1:5000"
PIZZA_TYPE_OPTIONS = ("Pepperoni",
                      "Margherita",
                      "Vegetarian",
                      "Neapolitan",
                      "Custom")
PIZZA_SIZE_OPTIONS = ("Small",
                      "Medium",
                      "Large",
                      "Extra_large")
PIZZA_TOPPINGS_OPTIONS = ("Olive",
                          "Tomato",
                          "Mushroom",
                          "Jalapeno",
                          "Chicken",
                          "Beef",
                          "Pepperoni",
                          "Pineapple",
                          "Bacon",
                          "Extra_cheese")
DRINK_TYPE_OPTIONS = ("Coke",
                      "Diet_Coke",
                      "Coke_Zero",
                      "Pepsi",
                      "Diet_Pepsi",
                      "Dr_Pepper",
                      "Water",
                      "Juice")
DELIVERY_OPTIONS = ("Pickup",
                    "Pizzeria",
                    "Uber_Eats",
                    "Foodora")


def generate_base_order():
    base_order = {
        "products": [],
        "delivery_method": {
            "type": "pickup",
            "details": {}
        }
    }
    return base_order


def valid_response(response, expect_json=False):
    if response.status_code != 200:
        click.echo(
            "Sorry, the previous command could not be submitted, "
            "please try again.\n"
            "Response from server: ({}) {}".format(
                response.status_code,
                response.text))
        return False
    if expect_json:
        try:
            response.json()
        except Exception as exception:
            print(exception)
            return False
    return True


@shell(intro="Pizzeria Command Line Ordering Interface", prompt="> ")
@click.pass_context
def main(context):
    # Global variables:
    # current_order: the dictionary of the current order in progress
    # current_order_no: the order number of the current order in progress
    # (populated only after the order has been submitted)
    context.obj = {"current_order": generate_base_order(),
                   "current_order_no": -1}


@main.group()
@click.argument("item", type=click.STRING, nargs=-1)
def menu(item):
    if item is None:
        # Output full menu
        pass
    else:
        try:
            response = requests.get(BASE_URL + "/api/menu/" + item.replace(" ", "_"))
            if response.status_code == 200:
                click.echo("{}: ${}".format(item, response.text))
            else:
                click.echo("{} is not a valid menu item".format(item))
        except Exception as exception:
            print(exception)
            return


@main.group()
@click.pass_obj
def order(globals):
    print("Previous globals: ", globals)


@order.command()
@click.pass_obj
def new(globals):
    if len(globals["current_order"]["products"]) > 0 and not click.confirm(
        "Creating a new order will discard the previous order in progress, "
            "do you wish to proceed?"):
        return  # Don't override the previous order in progress
    globals["current_order"] = generate_base_order()


@order.command()
@click.option("--number", "-n", required=False,
              help="The number of this item you would like to order.",
              type=click.IntRange(min=1),
              default=1
              )
@click.argument("pizza-size",
                type=click.Choice(PIZZA_SIZE_OPTIONS, case_sensitive=False)
                )
@click.argument("pizza-type",
                type=click.Choice(PIZZA_TYPE_OPTIONS, case_sensitive=False)
                )
@click.option("--toppings", "-t", required=False,
              help="Enter the toppings you would like",
              type=click.Choice(PIZZA_TOPPINGS_OPTIONS, case_sensitive=False),
              multiple=True
              )
@click.pass_obj
def pizza(globals, number, pizza_size, pizza_type, toppings):
    print("pizza_size={}, pizza_type={}".format(pizza_size, pizza_type))
    print("toppings={}, type={}".format(toppings, type(toppings)))
    pizza = {
        "product_category": "pizza",
        "size": pizza_size,
        "type": pizza_type,
        "toppings": list(toppings)}
    for _ in range(number):
        globals["current_order"]["products"].append(pizza)
    print(globals["current_order"])  # TODO: remove DEBUG


@order.command()
@click.option("--number", "-n", required=False,
              help="The number of this item you would like to order.",
              type=click.IntRange(min=1),
              default=1
              )
@click.argument("drink-type",
                type=click.Choice(DRINK_TYPE_OPTIONS, case_sensitive=False)
                )
@click.pass_obj
def drink(globals, number, drink_type):
    print("drink_type={}, type={}".format(drink_type, type(drink_type)))
    drink = {"product_category": "drink", "type": drink_type.lower()}
    for _ in range(number):
        globals["current_order"]["products"].append(drink)
    print(globals["current_order"])  # TODO: remove DEBUG


def echo_order(current_order):
    for index, product in enumerate(current_order["products"]):
        # Number the products in the order starting from 1
        click.echo(index + 1, nl=False, color="blue")
        if product["product_category"] == "drink":
            click.echo()
        elif product["product_category"] == "pizza":
            click.echo(
                "{} {} pizza with additional {}".format(
                    product["size"],
                    product["type"],
                    ",".join(
                        product["toppings"])))


@order.command()
@click.pass_obj
def submit(globals):
    print(globals["current_order"])
    delivery_option = click.prompt(
        "Please select a pickup/delivery method: "
        "('Pickup' for in-store pickup, 'Pizzeria' for in-house delivery, "
        "or one of 'Uber_Eats', 'Foodora')", type=click.Choice(
            DELIVERY_OPTIONS, case_sensitive=False), show_choices=False)
    print(delivery_option, type(delivery_option))
    delivery_option = delivery_option.lower()
    globals["current_order"]["delivery_method"]["type"] = delivery_option
    globals["current_order"]["data_format"] = "json_tree"
    if (delivery_option != "pickup"):
        address = click.prompt("Please enter your address", type=str)
        globals["current_order"]["delivery_method"]["details"] = {
            "address": address}

    try:
        response = requests.post(
            BASE_URL + "/api/orders",
            json=globals["current_order"])
    except requests.exceptions.RequestException as e:
        click.echo("Sorry, we failed to connect to the pizzeria server. "
                   "Please try again later.")
        return

    if valid_response(response, expect_json=True):
        json_repsonse = response.json()
        click.secho(
            "Your order has been sucessfully submitted. The total price is "
            "${}, and your order number is {}".format(
                json_repsonse["total_price"],
                json_repsonse["order_no"]))

    # TODO: reset globals["current_order"] to generate_base_order() ??


@order.command()
@click.argument("order-number", type=click.IntRange(min=0))
def edit(order_number):
    # Get this order from the server
    try:
        response = requests.get(BASE_URL + "/api/orders/" + order_number)
        if valid_response(response, expect_json=True):
            selected_order = response.json()
            echo_order(selected_order)
    except Exception as exception:
        print(exception)
        return


@order.command()
@click.argument("order-number", type=click.IntRange(min=0))
def cancel(order_number):
    # Get this order from the server
    try:
        response = requests.get(BASE_URL + "/api/orders/" + order_number)
        if valid_response(response, expect_json=True):
            selected_order = response.json()
            echo_order(selected_order)
    except Exception as exception:
        print(exception)
        return


@main.command()
def test():
    # # click.clear()  # Run clear in terminal
    # click.prompt("Please enter a valid integer", type=click.IntRange(min=1))
    response = requests.get(BASE_URL + "/pizza")
    # response = requests.get(BASE_URL + "/api/orders/create")
    # response = requests.post('https://httpbin.org/post', data = {'key':'value'})
    print(response.status_code)
    print(response.text)
    print(response.json())


if __name__ == "__main__":
    main()
