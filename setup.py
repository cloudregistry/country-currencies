from setuptools import setup, find_packages

from country_currencies import __version__


setup(
    name = "country-currencies",
    version = __version__,
    author = "Wil Tan",
    author_email = "wil@cloudregistry.net",
    description = "mapping of ISO-3166 country codes to their respective currencies",
    license = "MIT/X",
    install_requires = [],
    packages = ['country_currencies']
)
