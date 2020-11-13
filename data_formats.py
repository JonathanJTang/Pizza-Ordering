order_schema_csv = {
  "type": "object",
  "properties": {
    "data_format": { "type": "string", "pattern": "^csv$" },
    "csv_string": { "type": "string" }
  },
  "required": ["data_format", "csv_string"]
}

order_schema_json_tree = {
  "type": "object",
  "properties": {
    "data_format": { "type": "string", "pattern": "^json_tree$" },
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
                "enum": ["small", "medium", "large", "extra_large"]
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
            "required": ["product_category", "size", "type", "toppings"]
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
              }
            },
            "required": ["product_category", "type"]
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
            }
          },
          "required": ["type"]
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
                "address": { "type": "string" },
                "order_no": { "type": "integer" }
              },
              "required": ["address"]
            }
          },
          "required": ["type", "details"]
        }
      ]
    }
  },
  "required": ["data_format", "products", "delivery_method"]
}

edit_order_schema = {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "cart_item_id": { "type": "integer" },
      "type": { "type": "string" },
      "size": { "type": "string" },
      "toppings": { "type": "array", "items": { "type": "string" } }
    },
    "required": ["cart_item_id"],
    "additionalProperties": false
  }
}