from setuptools import find_packages
from setuptools import setup

NAME = "yelp_consumer"

VERSION = "1.0.0"

REQUIRES = [

]

DEV_REQUIRES = {
    'dev': [
        'tox'
    ]
}

setup(
    name=NAME,
    version=VERSION,
    description="Simple module to stream data from kafka into cassandra",
    author_email="kruglov.dima@gmail.com",
    keywords=["cassandra", "kafka"],
    install_requires=REQUIRES,
    extras_require=DEV_REQUIRES,
    dependency_links=[],
    packages=find_packages(),
    package_data={
        'consumer': ['*.sh',
                     '*.md']
    }
)
