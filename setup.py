#!/usr/bin/env python3

from setuptools import setup

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name="pytest-aoc",
    py_modules=["pytest_aoc"],
    install_requires=['requests'],
    setup_requires=['setuptools-version-command'],
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'pytest-freezegun', 'pytest-responses',
                'setuptools', 'wheel', 'setuptools-version-command',
                'twine', 'github-release']
        },
    version_command=('git describe', 'pep440-git'),
    author="Joost Molenaar",
    author_email="j.j.molenaar@gmail.com",
    description="Downloads puzzle inputs for Advent of Code and synthesizes PyTest fixtures",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/j0057/pytest-aoc",
    entry_points={
        "pytest11": ["pytest-aoc=pytest_aoc"]
    },
    classifiers=[
        "Framework :: Pytest",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7"
    ])
