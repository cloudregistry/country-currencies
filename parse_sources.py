#!/usr/bin/env python

"""
This script combines data from multiple sources to generate the mapping:
- https://github.com/hexorx/countries/blob/master/lib/data/countries.yaml
- https://github.com/limist/py-moneyed
"""

import sys
import yaml

CC_TO_CURRENCIES = {}

# hexorx_countries already has a country-to-currencies mapping
hexorx_countries = yaml.load(open('countries.yaml'))
assert hexorx_countries['LS']['currency'] == 'LSL'
assert hexorx_countries['LS']['alt_currency'] == 'ZAR'
for cc, entry in hexorx_countries.iteritems():
    currencies = CC_TO_CURRENCIES.setdefault(str(cc), [])
    for k in ('currency', 'alt_currency'):
        cur = entry.get(k)
        if cur and cur not in currencies:
            currencies.append(str(cur))


# pycountry gives us country-name-to-country-code mapping
import pycountry

def find_country(upper_name):
    try:
        return pycountry.countries.get(official_name=upper_name).alpha_2
    except KeyError:
        try:
            return pycountry.countries.get(name=upper_name).alpha_2
        except KeyError:
            return pycountry.countries.get(common_name=upper_name).alpha_2


# but we need to uppercase the country names in its indices
# because it is in Titlecase so Palau can be found, but not PALAU
assert find_country('Palau') is not None
try:
    find_country('PALAU')
    assert False, "expected KeyError"
except KeyError:
    pass

for idx in ('name', 'official_name', 'common_name'):
    index = pycountry.countries.indices[idx]
    for k in index.keys():
        index[k.upper()] = index[k]

# we should now be able to find both Palau and PALAU
assert find_country('Palau') is not None
assert find_country('PALAU') is not None



# search countries using py-moneyed data
from moneyed.classes import CURRENCIES
for cur_code, currency in CURRENCIES.iteritems():
    for country_name in currency.countries:
        try:
            cc = find_country(country_name)
            currencies = CC_TO_CURRENCIES.setdefault(str(cc), [])
            if cur_code not in currencies:
                print >> sys.stderr, "%s: %s augmenting hexorx data using py-moneyed" % (cc, cur_code)
                currencies.append(str(cur_code))
        except KeyError:
            print >> sys.stderr, "cannot find country by the name of %s"  % country_name
            continue

# Overrides based on some manual research (mostly Wikipedia)
OVERRIDES = {
    'WS': ('WST',),  # http://en.wikipedia.org/wiki/Samoa
    'GS': ('GBP',),  # http://en.wikipedia.org/wiki/South_Georgia_and_the_South_Sandwich_Islands
    'JE': ('GBP',),  # there is no JEP code in ISO4217 http://en.wikipedia.org/wiki/Jersey_pound
    'ZW': ('USD', 'ZAR', 'BWP', 'GBP', 'EUR'),  # ZWD was abandoned - http://en.wikipedia.org/wiki/Zimbabwe
    'FJ': ('FJD',),  # http://en.wikipedia.org/wiki/Fiji
    'CD': ('CDF',),  # http://en.wikipedia.org/wiki/Democratic_Republic_of_the_Congo
    'SK': ('EUR',),  # http://en.wikipedia.org/wiki/Slovakia
    'LV': ('EUR',),  # since 2014-01-01 (http://en.wikipedia.org/wiki/Latvia
    'IM': ('GBP',),  # http://en.wikipedia.org/wiki/Manx_pound
    'BL': ('EUR',),  # http://en.wikipedia.org/wiki/Saint_Barth%C3%A9lemy
    'BT': ('BTN', 'INR'),  # http://en.wikipedia.org/wiki/Bhutan
    'HT': ('HTG', 'USD'),  # http://en.wikipedia.org/wiki/Haiti
    'EE': ('EUR',),  # since 2011-01-01 - http://en.wikipedia.org/wiki/Estonia
    'TL': ('USD',),  # http://en.wikipedia.org/wiki/East_Timor
    'TM': ('TMT',),  # http://en.wikipedia.org/wiki/Turkmenistan
    'TJ': ('TJS',),  # http://en.wikipedia.org/wiki/Tajikistan
    'AX': ('EUR',),  # http://en.wikipedia.org/wiki/%C3%85land_Islands
    'ZM': ('ZMW',),  # https://en.wikipedia.org/wiki/Zambian_kwacha
}

for cc, v in OVERRIDES.iteritems():
    CC_TO_CURRENCIES[cc] = v


### output ###

varname = 'CURRENCIES_BY_COUNTRY_CODE'
print '%s = {' % varname
for cc, currencies in CC_TO_CURRENCIES.iteritems():
    print "    '%s': %s," % (cc, repr(tuple(currencies)))
print '}'
