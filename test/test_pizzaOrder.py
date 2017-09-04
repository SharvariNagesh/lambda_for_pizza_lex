import pytest
import pizzaOrder
import json

def test_pizza_order():
  assert pizzaOrder.to_test() == "OK"
  with open('test/data/pizza.json') as data_file:
    event = json.load(data_file)
  result = pizzaOrder.lambda_handler(event, None)
  print(result)
  assert result == 0

