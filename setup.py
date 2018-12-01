#!/usr/bin/env python3

from setuptools import setup

setup(
    name="pytest-aoc",
    py_modules=["pytest_aoc"],
    install_requires=['requests'],
    setup_requires=['setuptools-version-command'],
    version_command=('git describe', 'pep440-git'),
    author="Joost Molenaar",
    author_email="j.j.molenaar@gmail.com",
    entry_points={
        "pytest11": ["pytest-aoc=pytest_aoc"]
    },
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7"
    ])
