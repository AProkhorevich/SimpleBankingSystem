class NoSuchCard(Exception):
    def __str__(self):
        return 'Such a card does not exist.'


class IsNotLuhn(Exception):
    def __str__(self):
        return 'Probably you made a mistake in the card number.\nPlease try again!'


class WrongPIN(Exception):
    def __str__(self):
        return 'Wrong card number or PIN!'


class NoMoney(Exception):
    def __str__(self):
        return 'Not enough money!'
