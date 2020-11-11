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
        "type": "pizzeria",
        "details": {
            "address": "74 random street",
            "order_no": 1
        }
    }
}

order_schema_csv = {
    "type": "object",
    "properties": {
        "data_format": {"type": "string", "pattern": "^csv$"},
        "products": {"type": "string"},
        "delivery_method": {"type": "string"}
    },
    "required": [
        "data_format",
        "products",
        "delivery_method"
    ]
}

order_schema_json_tree = {
    "type": "object",
    "properties": {
        "data_format": {"type": "string", "pattern": "^json_tree$"},
        "products": {
            "type": "array",
            "items": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "product_category": {
                                "type": "string",
                                "pattern": "^pizza$"
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
                                "pattern": "^drink$"
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
            "oneOf": [
                {
                    "properties": {
                        "type": {
                            "type": "string",
                            "pattern": "^pickup$"
                        },
                    },
                    "required": [
                        "type",
                    ]
                },
                {
                    "properties": {
                        "type": {
                            "type": "string",
                            "pattern": "^(pizzeria|uber_eats|foodora)$"
                        },
                        "details": {
                            "type": "object",
                            "properties": {
                                "address": {"type": "string"},
                                "order_no": {"type": "integer"}
                            },
                            "required": [
                                "address"
                            ]
                        }
                    },
                    "required": [
                        "type",
                        "details"
                    ]
                },
            ]
        }
    },
    "required": [
        "data_format",
        "products",
        "delivery_method"
    ]
}
