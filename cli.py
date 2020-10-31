import click
import requests

BASE_URL = "http://127.0.0.1:5000/api"
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

@click.group()
def main():
    pass

@main.group()
@click.option("--number", "-n", required=False,
    help="The number of items you would like to order.",
    type=click.IntRange(min=1),
    default=1
)
def order(number):
    print("order={}".format(number))

@order.command()
@click.option("--toppings", "-t", required=False,
    help="Enter the toppings you would like",
    type=click.Choice(TOPPINGS_OPTIONS, case_sensitive=False),
    multiple=True
)
def pizza(toppings):
    print("toppings={}, type={}".format(toppings, type(toppings)))
    for topping in toppings:
        pass
    click.secho("Message", fg="green")

@order.command()
@click.argument("drink-type",
                type=click.Choice(DRINK_OPTIONS, case_sensitive=False)
)
def drink(drink_type):
    print("drink_type={}, type={}".format(drink_type, type(drink_type)))


@click.command()
def test():
    # # click.clear()  # Run clear in terminal
    # click.prompt("Please enter a valid integer", type=click.IntRange(min=1))
    response = requests.get(BASE_URL + "/api/orders/create")
    # response = requests.post('https://httpbin.org/post', data = {'key':'value'})
    print(response.status_code)
    print(response.text)
    print(response.json())
    # print(response)

if __name__ == "__main__":
    main()