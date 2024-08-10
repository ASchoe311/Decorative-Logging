"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_packages

setup(
    name="decorative_logging",
    author="Adam Schoenfeld",
    author_email="aschoe@umich.edu",
    url="adamschoe.com",
    description="Simplifies logging through the use of decorators",
    version="0.0.1",
    packages=find_packages(where=".", exclude=["tests"]),
    install_requires=[
        "setuptools>=45.0",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
    ],
)