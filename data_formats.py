# JSON data sample for Uber Eats
{
    "products": [
        {
            "product_category": "pizza",
            "size": "small",
            "type": "custom",
            "toppings": [
                "olive",
                "chicken"
            ]
        },
        {
            "product_category": "drink",
            "type": "coke"
        }
    ],
    "delivery_method": {
        "delivery_type": "pickup",
        "details": {}
    }
}

order_schema = {
    "type": "object",
    "properties": {
        "products": {
            "type": "array",
            "items": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "product_category": {
                                "type": "string",
                                "pattern": "pizza"
                            },
                            "size": {
                                "type": "string",
                                "enum": [
                                    "small",
                                    "medium",
                                    "large",
                                    "extra_large"
                                ]
                            },
                            "type": {
                                "type": "string",
                                "enum": [
                                    "pepperoni",
                                    "margherita",
                                    "vegetarian",
                                    "neapolitan",
                                    "custom"
                                ]
                            },
                            "toppings": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": [
                                        "olive",
                                        "tomato",
                                        "mushroom",
                                        "jalapeno",
                                        "chicken",
                                        "beef",
                                        "pepperoni",
                                        "pineapple",
                                        "bacon",
                                        "cheese"
                                    ]
                                }
                            }
                        },
                        "required": [
                            "product_category",
                            "size",
                            "type",
                            "toppings"
                        ]
                    },
                    {
                        "type": "object",
                        "properties": {
                            "product_category": {
                                "type": "string",
                                "pattern": "drink"
                            },
                            "type": {
                                "type": "string",
                                "enum": [
                                    "coke",
                                    "diet_coke",
                                    "coke_zero",
                                    "pepsi",
                                    "diet_pepsi",
                                    "dr_pepper",
                                    "water",
                                    "juice"
                                ]
                            },
                        },
                        "required": [
                            "product_category",
                            "type"
                        ]
                    }
                ]
            }
        },
        "delivery_method": {
            "type": "object",
            "properties": {
                "delivery_type": {
                    "type": "string",
                    "enum": [
                        "pickup",
                        "pizzeria",
                        "ubereats",
                        "foodora"
                    ]
                },
                "details": {
                    "type": "object"
                }
            },
            "required": [
                "delivery_type",
                "details"
            ]
        }
    },
    "required": [
        "products",
        "delivery_method"
    ]
}

# csv data for Foodora
"ProductType,Proda, adjf, asdijfai"