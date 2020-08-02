from typing import Dict

# Note that largest values come first
COINS = (200, 100, 50, 20, 10, 5, 2, 1)


def return_coins(coffee_price: float, eur_inserted: float) -> Dict[int, int]:
    """Return euro coins for the given amount inserted.

    :return: dict with keys of the coin's denomination (in cents) and
             value of how many coins to return.
    """
    change_dict = {}

    change = eur_inserted - coffee_price

    # Return early if no change is to be given
    if change <= 0:
        return change_dict

    # Work in cents to deal with integers, fix floating-point issues
    change_cents = int(round(change * 100))

    # Euro is "canonical", so greedy algorithms work (try to use highest coins first)
    for coin in COINS:
        # Number of coins is integer division
        num_coins = int(change_cents / coin)
        # Only add to dict if the denomination is to be used
        if num_coins > 0:
            change_dict[coin] = num_coins
            # Remaining change is modulo
            change_cents = change_cents % coin

    return change_dict
