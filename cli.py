import click
import requests
from click_shell import shell

BASE_URL = "http://127.0.0.1:5000"
TOPPINGS_OPTIONS = ("Olives",
                    "Tomatoes",
                    "Mushrooms",
                    "Jalapenos",
                    "Chicken",
                    "Beef",
                    "Pepperoni",
                    "Pineapple",
                    "Bacon",
                    "Extra cheese")
DRINK_OPTIONS = ("Coke",
                 "Diet Coke",
                 "Coke Zero",
                 "Pepsi",
                 "Diet Pepsi",
                 "Dr Pepper",
                 "Water",
                 "Juice")


def generate_base_order():
    base_order = {
        "products": [],
        "delivery_method": {
            "delivery_type": "pickup",
            "details": {}
        }
    }
    return base_order


def response_valid(response):
    if response.status_code != 200:
        click.echo("Sorry, the previous command could not be submitted, "
                   "please try again.\n"
                   "Response from server: {}".format(response.text))
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
@click.option("--toppings", "-t", required=False,
              help="Enter the toppings you would like",
              type=click.Choice(TOPPINGS_OPTIONS, case_sensitive=False),
              multiple=True
              )
def pizza(number, toppings):
    print("toppings={}, type={}".format(toppings, type(toppings)))
    for topping in toppings:
        pass
    click.secho("Message", fg="green")
    """{
        "product_category": "pizza",
        "size": "small",
        "type": "custom",
        "toppings": [
            "olive",
            "chicken"
        ]
    },"""


@order.command()
@click.option("--number", "-n", required=False,
              help="The number of this item you would like to order.",
              type=click.IntRange(min=1),
              default=1
              )
@click.argument("drink-type",
                type=click.Choice(DRINK_OPTIONS, case_sensitive=False)
                )
@click.pass_obj
def drink(globals, number, drink_type):
    print("drink_type={}, type={}".format(drink_type, type(drink_type)))
    drink = {"product_category": "drink", "type": drink_type.lower()}
    for _ in range(number):
        globals["current_order"]["products"].append(drink)
    print(globals["current_order"])  # DEBUG


@order.command()
@click.pass_obj
def submit(globals):
    print(globals["current_order"])
    try:
        response = requests.post(
            BASE_URL + "/api/orders",
            json=globals["current_order"])
    except requests.exceptions.RequestException as e:
        click.echo("Sorry, we failed to connect to the pizzeria server. "
                   "Please try again later.")
        return

    if response_valid(response):
        try:
            print(response.status_code)
            print(response.text)
            json_repsonse = response.json()
            click.secho(
                "Your order has been sucessfully submitted. The total price is "
                "{}, and your order number is {}".format(
                    json_repsonse["total_price"],
                    json_repsonse["order_no"]))
            print(response.json())
        except Exception as exception:
            print(exception)


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
