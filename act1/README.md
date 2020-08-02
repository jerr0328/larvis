# Coin change calculator

This challenge is to calculate the change needed to be given (in coins) for any positive euro amount.

## Interface

The `coins.py` file contains the `return_coins` function, which takes `coffee_price` and `eur_inserted` as floating-point numbers and returns the change with a dictionary where the keys are the coin face values in Eurocents.

Example:
```python-repl
>>> return_coins(coffee_price=1.12, eur_inserted=5)
{200: 1, 100: 1, 50: 1, 20: 1, 10: 1, 5: 1, 2: 1, 1: 1}
```

## Solution considerations

Since Euro's smallest denomination is 1 cent, which means we can actually represent the currency entirely as integer cents. However, to accept floating point numbers means we need to factor in binary errors (for instance, 2 - 1.12 is 0.88, but in Python you would see it as 0.87999999...). The easy way around this is to round the numbers.

While there's a "proper" solution to this problem for any currency, Euro is considered a "canonical" currency which means we can use a greedy approach to solve the problem. In a real system where some coins might be unavailable, the given solution would need to be modified to factor in real-world supply.


## Tests

Run `pip install -r requirements-dev.txt` from the parent (`larvis`) directory, then from there run `pytest -v act1`.
