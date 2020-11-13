# a2-starter

Run the main Flask module by running `python3 PizzaParlour.py`

Run unit tests with coverage by running `pytest --cov-report term-missing --cov=. tests/*`

Install requests library that lets us do HTTP requests easily. Run the command: `pip3 install requests click`
Install additional modules jsonschema, click-shell, colorama

We used autopep8 for code formatting, organized imports in VS Code, and used pylint.


Design patterns used:
Abstract superclass for products and delivery detail parsers
Dependency injection in Order class

Pair Programming:
For pair programming, we held planning stages totalling 3 hours, where we figured out our 2 features and how they would fit in the program and designed them.  We chose to switch roles based on completing a checkpoint of the feature, which initially took around 90 minutes (we considered switching after a shorter amount of time, but decided not to since it interrupted our training of thought while we were midway through the feature checkpoint).
 
Then for our first feature, we chose the Pizza, Product, Drink, Cart classes. We started off with Ismail as the driver and implemented the Pizza class, and wrote unit tests for it. Then we switched drivers to Jonathan and implemented Product, Drink and tests for them. Then we switched back to Ismail and implemented the Cart class and tests for it.
 
For our second feature, we chose the Order, OrderParser, DeliveryMethod, PickupDelivery, PizzeriaDelivery, FoodoraDelivery, UberEatsDelivery classes. We started off with Jonathan as the driver and implemented the DeliveryMethod, Order, OrderParser, Pickup, PizzeriaDelivery. Then we switched to Ismail, and implemented FoodoraDelivery, UberEatsDelivery and tests. We forgot to push/pull our latest changes at the testing stage, so we had a git conflict.
 
Pair programming was slower than working separately, and it sometimes felt like a less worthwhile use of time because of that. But it was slower because we planned everything in a very detailed way, drew diagrams and so on. If we hadn't planned so much, then pair programming would have been faster in the sense that it would reduce differences in design choices. It was actually nice to have someone find the small bugs in our code while we were writing it. We realised that when we are writing code, even though we try not to, we tend to overlook edge cases and focus more on the general behaviour of our program. Having someone else watch over our code who isn't worried about the general behaviour of the program helped us find bugs on the spot. We still had some bugs, but they were much less than they would have been with traditional programming. Also, the navigator was often able to help think of better ways to achieve the task at hand than what the driver initially codes.