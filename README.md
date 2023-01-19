# Pizza Ordering CLI + Backend

Command-line interface app for ordering pizzas (created with Click), with a Python Flask backend.

We created an API for our use, as well as JSON schemas. We also include unit and integration tests crafted for good coverage of the repository.

Functionality: displaying the menu; ordering drinks and pizzas with toppings; editing, submitting, and cancelling orders; specifying delivery options.

This was a course project done together with İsmail Atadinç (kralgeliy1).

Run unit tests with coverage by running `pytest --cov-report term-missing --cov=. tests/*`

We used `autopep8` for code formatting, organized imports in VS Code, and used `pylint`.

## Testing Instructions
0. Install additional modules: `pip3 install requests click click-shell jsonschema simplejson colorama` <br>
(`requests` is for making HTTP requests, `jsonchema` for validating json schemas, `simplejson` for json encoding, `click` and `click-shell` for the command-line interface, `colorama` for pretty terminal output)
1. Run the main Flask module: `python3 PizzaParlour.py`
2. In another shell, run the command-line interface: `python3 cli.py` and type in commands according to the usage instructions below.


## CLI Usage Instructions:
- `order new` creates a new order, or discards the previous one in progress.
- `order drink [type]` adds a drink of the given type to the order. (run `order drink --help` for valid options.)
- `order pizza [size] [type] [-t [topping]] [-t [topping]]` adds a pizza of the given size, type, and toppings to the order. (run `order pizza --help` for valid options; use one `-t` option for each topping.)
- `order edit` can be used to edit the current order (follow the prompts to delete or edit items)
- `order submit` submits the order to the server; follow the prompts to select pickup/delivery option; at the end the assigned order number and the total price of the order is displayed (the order number is ).
- `order edit [order number]` can be used to edit a submitted order (follow the prompts to delete or edit items)
- `order cancel [order number]` cancels a submitted order.
- `menu` displays the full menu.
- `menu [item]` displays the price of the given menu item.
