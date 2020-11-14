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
    """Return the order dictionary for an empty order."""
    base_order = {
        "products": [],
        "delivery_method": {
            "type": "pickup",
            "details": {}
        }
    }
    return base_order


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


def pretty_print_dictionary(dic):
    """Print a dictionary nicely to the terminal."""
    for key, value in dic.items():
        click.echo("{:13}:  ${}".format(key.title(), value))
    click.echo()


def echo_item(position, product):
    """Output the given product to the terminal as part of a list of items. The
    first item in the list has position 1."""
    click.secho(f"{position}.", nl=False, bold=True, fg="blue", bg="white")
    if product["product_category"] == "drink":
        click.secho(" {}".format(product["type"].title()))
    elif product["product_category"] == "pizza":
        click.secho(
            " {} {} pizza".format(
                product["size"].title(),
                product["type"].title(),
            ), nl=False)
        if len(product["toppings"]) > 0:
            click.secho(" with additional {}".format(", ".join(
                product["toppings"]).title()), nl=False)
        click.secho()


def valid_response(response, error_handler=None, expect_json=False):
    """Return True iff response is valid under the given conditions. If response
    has an invalid status code, call error_handler. If expect_json is True, also
    check if the response has a JSON payload."""
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
    """Entry point to the CLI."""
    # Global variables:
    # current_order: the dictionary of the current order in progress
    context.obj = {"current_order": generate_base_order()}


@main.command()
@click.argument("item-name", type=click.STRING, nargs=-1, required=False)
def menu(item_name):
    """Request the full menu or part of the menu from the server, and output the
    results. If item_name is not given, output the whole menu; otherwise output
    just the given item."""
    try:
        if len(item_name) == 0:
            # Print the full menu
            response = requests.get(BASE_URL + "/api/menu")
            if valid_response(response, expect_json=True):
                json_response = response.json()
                for category, sublist in json_response.items():
                    click.secho("{}:".format(category.title()),
                                fg="blue", bold=True)
                    pretty_print_dictionary(sublist)
        else:
            # Get price of one item
            item_str = "_".join(item_name).lower()
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
    # Don't need to do anything for this function, since it's a command to group
    # the other subcommands related to ordering
    pass


@order.command()
@click.pass_obj
def new(globals):
    """Create a new order and discard the previous one from memory; prompt the
    user on whether to proceed if there is a previous incomplete order in
    progress."""
    if len(globals["current_order"]["products"]) > 0 and not click.confirm(
        "Creating a new order will discard the previous order in progress, "
            "do you wish to proceed?"):
        return  # Don't override the previous order in progress
    globals["current_order"] = generate_base_order()


@order.command()
@click.option("--number", "-n", required=False,
              help="The number of pizzas of this type to order.",
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
              help="The topping(s) you would like (one topping per -t option)",
              type=click.Choice(PIZZA_TOPPINGS_OPTIONS, case_sensitive=False),
              multiple=True
              )
@click.pass_obj
def pizza(globals, number, pizza_size, pizza_type, toppings):
    """Order a pizza with the given pizza_size, pizza_type, and toppings."""
    pizza = {
        "product_category": "pizza",
        "size": pizza_size.lower(),
        "type": pizza_type.lower(),
        "toppings": [name.lower() for name in toppings]}
    for _ in range(number):
        globals["current_order"]["products"].append(pizza)


@order.command()
@click.option("--number", "-n", required=False,
              help="The number of drinks of this type to order.",
              type=click.IntRange(min=1),
              default=1
              )
@click.argument("drink-type",
                type=click.Choice(DRINK_TYPE_OPTIONS, case_sensitive=False)
                )
@click.pass_obj
def drink(globals, number, drink_type):
    """Order a drink with the given drink_type."""
    drink = {"product_category": "drink", "type": drink_type.lower()}
    for _ in range(number):
        globals["current_order"]["products"].append(drink)


@order.command()
@click.pass_obj
def submit(globals):
    """Submit the current order in progress, prompting the user for a
    pickup/delivery method."""
    # Don't allow empty orders to be submitted
    if len(globals["current_order"]["products"]) == 0:
        click.echo("Please add items to your order before submitting.")
        return

    # Request an order number from server
    try:
        response = requests.post(BASE_URL + "/api/orders")
    except requests.exceptions.RequestException:
        click.echo("Sorry, we failed to connect to the pizzeria server. "
                   "Please try again later.")
        return
    if not valid_response(response):
        return
    order_no = int(response.text)

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
            globals["current_order"].clear()
            globals["current_order"]["data_format"] = "csv"
            globals["current_order"]["csv_string"] = csv_string

    # Send order information to server
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
        # Reset the order variable after submitting the order
        globals["current_order"] = generate_base_order()


def edit_pizza(selected_pizza, cart_item_id, changes):
    """Interactively edit selected_pizza at item_no by prompting the user with
    possible options, and record the new edits in changes."""
    edit_type = click.prompt(
        "Select an option to edit",
        type=click.Choice(("type", "size", "add_topping", "remove_topping"),
                          case_sensitive=False)).lower()
    if cart_item_id not in changes:
        changes[cart_item_id] = {"cart_item_id": cart_item_id}
    if edit_type == "type":
        new_type = click.prompt("Select a new pizza type",
                                type=click.Choice(
                                    PIZZA_TYPE_OPTIONS,
                                    case_sensitive=False)).lower()
        selected_pizza["type"] = new_type
        changes[cart_item_id]["type"] = new_type
    elif edit_type == "size":
        new_size = click.prompt("Select a new pizza size",
                                type=click.Choice(
                                    PIZZA_SIZE_OPTIONS,
                                    case_sensitive=False)).lower()
        selected_pizza["size"] = new_size
        changes[cart_item_id]["size"] = new_size
    elif edit_type == "add_topping":
        new_topping = click.prompt("Add a topping",
                                   type=click.Choice(
                                       PIZZA_TOPPINGS_OPTIONS,
                                       case_sensitive=False)).lower()
        selected_pizza["toppings"].append(new_topping)
        changes[cart_item_id]["toppings"] = selected_pizza["toppings"]
    else:  # edit_type == "remove_topping"
        topping_to_delete = click.prompt(
            "Remove a topping",
            type=click.Choice(
                [name.title() for name in selected_pizza["toppings"]],
                case_sensitive=False)).lower()
        for topping in selected_pizza["toppings"]:
            if topping.lower() == topping_to_delete:
                selected_pizza["toppings"].remove(topping)
                break
        changes[cart_item_id]["toppings"] = selected_pizza["toppings"]


def interactive_edit_order(globals, changes):
    """Interactively print the current order and give the user options to edit
    it, adding any changes made to changes. Return True iff the user has not
    finished editing the order yet."""
    # Print the current order
    click.echo("Current order:")
    for index, product in enumerate(globals["current_order"]["products"]):
        # Number the products in the order starting from 1
        echo_item(index + 1, product)

    # Get the item in the order the user would like to edit
    item_no = click.prompt(
        "Select the number of an item to edit (enter 0 to exit)",
        type=click.IntRange(
            min=0,
            max=len(
                globals["current_order"]["products"])))
    if item_no == 0:
        return False  # User is done editing the order
    selected_product = globals["current_order"]["products"][item_no - 1]
    cart_item_id = selected_product.get("cart_item_id")

    # Determine which operation the user wishes to do
    operation = click.prompt(
        "Select an operation",
        type=click.Choice(("delete", "edit"), case_sensitive=False))
    if operation.lower() == "delete":
        globals["current_order"]["products"].pop(item_no - 1)
        changes[cart_item_id] = {"cart_item_id": cart_item_id,
                                 "remove": "remove"}
    else:  # the operation is 'edit'
        echo_item(item_no, selected_product)
        if selected_product["product_category"] == "drink":
            new_type = click.prompt(
                "Select a new drink type",
                type=click.Choice(
                    DRINK_TYPE_OPTIONS,
                    case_sensitive=False)).lower()
            selected_product["type"] = new_type
            if cart_item_id not in changes:
                changes[cart_item_id] = {"cart_item_id": cart_item_id}
            changes[cart_item_id]["type"] = new_type
        elif selected_product["product_category"] == "pizza":
            edit_pizza(selected_product, cart_item_id, changes)

    return True  # User is not yet done editing the order


@order.command()
@click.argument("order-number",
                type=click.IntRange(min=0),
                required=False)
@click.pass_obj
def edit(globals, order_number):
    """If order_number is given, edit the submitted order with the given
    order_number. Otherwise, edit the current order in progress."""
    if order_number is not None:
        if len(
            globals["current_order"]["products"]) > 0 and not click.confirm(
            "Loading a past order will discard the previous order in progress, "
                "do you wish to proceed?"):
            return  # Don't override the previous order in progress
        globals["current_order"] = generate_base_order()
        # Get this order from the server
        try:
            response = requests.get(
                BASE_URL + "/api/orders/" + str(order_number))
            if not valid_response(
                    response,
                    lambda res: click.echo(
                        "Error: {} is not a valid order number".format(order_number)),
                    expect_json=True):
                return
            globals["current_order"]["products"] = response.json()["products"]
        except requests.exceptions.RequestException as exception:
            print(exception)
            return
    else:
        # Set temporary item id's to keep track of items between edits
        for index, product in enumerate(globals["current_order"]["products"]):
            product["cart_item_id"] = index + 1

    changes = {}
    while interactive_edit_order(globals, changes):
        pass  # repeatedly call interactive_edit_order until the user exits it

    if order_number is not None:
        # Editing order on the server, send the changes to the server
        print(changes)  # TODO: remove debug
        try:
            response = requests.patch(
                BASE_URL +
                "/api/orders/" +
                str(order_number),
                json=list(
                    changes.values()))
            if not valid_response(response):
                return
            click.echo(f"The price of the new order is ${response.text}")
        except requests.exceptions.RequestException as exception:
            print(exception)
            return
        # Reset the order variable since it was retrieved from the server
        globals["current_order"] = generate_base_order()
    else:
        # Remove temporary id's added earlier
        for product in globals["current_order"]["products"]:
            product.pop("cart_item_id", None)


@order.command()
@click.argument("order-number", type=click.IntRange(min=0))
def cancel(order_number):
    """Cancel a submitted order with the given order_number."""
    # Get this order from the server
    try:
        response = requests.delete(
            BASE_URL + "/api/orders/" + str(order_number))
        if response.status_code == 200:
            click.echo("Successfully cancelled order {}".format(order_number))
        else:
            click.echo(
                "Error: {} is not a valid order number".format(order_number))
    except requests.exceptions.RequestException as exception:
        print(exception)
        return


if __name__ == "__main__":
    main()
