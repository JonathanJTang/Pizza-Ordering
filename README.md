# Assignment 2 - Team 47, Jonathan Tang (JonathanJTang) and İsmail Atadinç (kralgeliy1)

Run unit tests with coverage by running `pytest --cov-report term-missing --cov=. tests/*`

We used `autopep8` for code formatting, organized imports in VS Code, and used `pylint`.

## Testing Instructions
0. Install additional modules: `pip3 install requests click click-shell jsonschema colorama` <br>
(`requests` is for making HTTP requests, `jsonchema` for validating json schemas, `click` and `click-shell` for the command-line interface, `colorama` for pretty terminal output)
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
- `order menu` displays the full menu.
- `order menu [item]` displays the price of the given menu item.


## Pair-programming write-up:
For pair programming, we held planning stages totalling 3 hours, where we figured out our 2 features and how they would fit in the program and designed them.  We chose to switch roles based on completing a checkpoint of the feature, which initially took around 90 minutes (we considered switching after a shorter amount of time, but decided not to since it interrupted our training of thought while we were midway through the feature checkpoint).
 
Then for our first feature, we chose the Pizza, Product, Drink, Cart classes. We started off with Ismail as the driver and implemented the Pizza class, and wrote unit tests for it. Then we switched drivers to Jonathan and implemented Product, Drink and tests for them. Then we switched back to Ismail and implemented the Cart class and tests for it.
 
For our second feature, we chose the Order, OrderParser, DeliveryMethod, PickupDelivery, PizzeriaDelivery, FoodoraDelivery, UberEatsDelivery classes. We started off with Jonathan as the driver and implemented the DeliveryMethod, Order, OrderParser, Pickup, PizzeriaDelivery. Then we switched to Ismail, and implemented FoodoraDelivery, UberEatsDelivery and tests. We forgot to push/pull our latest changes at the testing stage, so we had a git conflict.
 
Pair programming was slower than working separately, and it sometimes felt like a less worthwhile use of time because of that. But it was slower because we planned everything in a very detailed way, drew diagrams and so on. If we hadn't planned so much, then pair programming would have been faster in the sense that it would reduce differences in design choices. It was actually nice to have someone find the small bugs in our code while we were writing it. We realised that when we are writing code, even though we try not to, we tend to overlook edge cases and focus more on the general behaviour of our program. Having someone else watch over our code who isn't worried about the general behaviour of the program helped us find bugs on the spot. We still had some bugs, but they were much less than they would have been with traditional programming. Also, the navigator was often able to help think of better ways to achieve the task at hand than what the driver initially coded.


## Design patterns used:
Abstract superclass for products and delivery detail parsers
Dependency injection in Order class