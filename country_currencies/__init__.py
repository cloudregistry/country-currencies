from .data import CURRENCIES_BY_COUNTRY_CODE


__version__ = '0.1'

def get_by_country(country_code, default=None):
    currencies = CURRENCIES_BY_COUNTRY_CODE.get(country_code)
    if not currencies:  # it could be an empty tuple
        return default
    else:
        return currencies
