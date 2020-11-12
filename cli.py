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


def valid_response(response, error_handler=None, expect_json=False):
    if response.status_code != 200:
        if error_handler is None:
            # Default error handler
            click.echo(
                "Sorry, the previous command failed.\n"
                "Response from server: ({}) {}".format(
                    response.status_code,
                    response.text))
        else:
            error_handler(response)
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


@main.command()
@click.argument("item-name", type=click.STRING, nargs=-1, required=False)
def menu(item_name):
    try:
        if len(item_name) == 0:
            # Print the full menu
            response = requests.get(BASE_URL + "/api/menu")
            if valid_response(response, expect_json=True):
                json_response = response.json()
                for category, sublist in json_response.items():
                    click.echo("{}:".format(category.title()))
                    click.echo(sublist)
        else:
            # Get price of one item
            item_str = "_".join(item_name)
            response = requests.get(
                BASE_URL +
                "/api/menu/" +
                item_str)
            if valid_response(response, error_handler=lambda res: click.echo(
                    "Error: {} is not a valid menu item".format(item_str))):
                click.echo("{}: ${}".format(item_str, response.text.strip()))

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
        click.secho(
            f"{index + 1}.",
            nl=False,
            bold=True,
            fg="blue",
            bg="white")
        if product["product_category"] == "drink":
            click.secho(" {}".format(product["type"]))
        elif product["product_category"] == "pizza":
            click.secho(
                " {} {} pizza with additional {}".format(
                    product["size"],
                    product["type"],
                    ",".join(
                        product["toppings"])))


def convert_to_csv(order_data):
    """Convert order_data (in JSON) to a CSV string in the format accepted by
    PizzaParlour."""
    product_strings = []
    for item in order_data["products"]:
        if item["product_category"] == "pizza":
            product_strings.append(
                ",".join(("pizza", item["type"], item["size"],
                         "|".join(item["toppings"]))))
        elif item["product_category"] == "drink":
            product_strings.append(",".join(("drink", item["type"], "")))
    delivery_string = ",".join(
        (order_data["delivery_method"]["type"],
         order_data["delivery_method"]["details"]["address"],
         str(order_data["delivery_method"]["details"]["order_no"])))
    return "\n".join(product_strings + [delivery_string])


@order.command()
@click.pass_obj
def submit(globals):
    print(globals["current_order"])  # TODO: remove DEBUG
    try:
        response = requests.post(BASE_URL + "/api/orders")
    except requests.exceptions.RequestException:
        click.echo("Sorry, we failed to connect to the pizzeria server. "
                   "Please try again later.")
        return

    if not valid_response(response):
        return
    order_no = int(response.text)
    print("Got order_no of {}".format(order_no))  # TODO: remove DEBUG

    # Get the delivery type
    delivery_option = click.prompt(
        "Please select a pickup/delivery method: "
        "('Pickup' for in-store pickup, 'Pizzeria' for in-house delivery, "
        "or one of 'Uber_Eats', 'Foodora')", type=click.Choice(
            DELIVERY_OPTIONS, case_sensitive=False), show_choices=False)
    delivery_option = delivery_option.lower()
    globals["current_order"]["delivery_method"]["type"] = delivery_option
    globals["current_order"]["data_format"] = "json_tree"
    if (delivery_option != "pickup"):
        address = click.prompt("Please enter your address", type=str)
        globals["current_order"]["delivery_method"]["details"] = {
            "address": address, "order_no": order_no}
        if (delivery_option == "foodora"):
            csv_string = convert_to_csv(globals["current_order"])
            print(repr(csv_string))  # TODO: remove DEBUG
            globals["current_order"].clear()
            globals["current_order"]["data_format"] = "csv"
            globals["current_order"]["csv_string"] = csv_string

    try:
        response = requests.put(
            BASE_URL + "/api/orders/" + str(order_no),
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
                order_no))

    # Reset the order variable (can get it in the future through 'order edit')
    globals["current_order"] = generate_base_order()


@order.command()
@click.argument("order-number", type=click.IntRange(min=0))
def edit(order_number):
    # Get this order from the server
    try:
        response = requests.get(BASE_URL + "/api/orders/" + str(order_number))
        if not valid_response(
                response,
                lambda res: click.echo(
                    "Error: {} is not a valid order number".format(order_number)),
                expect_json=True):
            return
        selected_order = response.json()
        click.echo("Current order:")
        echo_order(selected_order)
    except requests.exceptions.RequestException as exception:
        print(exception)
        return
    item_no = click.prompt(
        "Select an item to edit",
        type=click.IntRange(
            min=1,
            max=len(
                selected_order["products"])))


@order.command()
@click.argument("order-number", type=click.IntRange(min=0))
def cancel(order_number):
    # Get this order from the server
    try:
        response = requests.get(BASE_URL + "/api/orders/" + str(order_number))
        if response.status_code == 200:
            click.echo("Successfully cancelled order {}".format(order_number))
        else:
            click.echo(
                "Error: {} is not a valid order number".format(order_number))
    except requests.exceptions.RequestException as exception:
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
