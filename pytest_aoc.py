import datetime
import os
import os.path

import pytest
import requests

def pytest_addoption(parser):
    aoc = parser.getgroup('aoc')

    aoc.addoption('--aoc-year',         action='store', default=None,       help='year to download input files for')
    aoc.addoption('--aoc-input-dir',    action='store', default='input',    help='directory to store input files in')
    aoc.addoption('--aoc-session-id',   action='store', default=None,       help='session ID to use for retrieving input')
    aoc.addoption('--aoc-session-file', action='store', default='.cookie',  help='file from which to read session ID')

    parser.addini('aoc_year', help='year to download input files for')
    parser.addini('aoc_input_dir', help='directory to store input files in')
    parser.addini('aoc_session_id', help='session ID to use for retrieving input')
    parser.addini('aoc_session_file', help='file from which to read session ID')

def get_cookie(session_id, session_file):
    if session_id:
        return session_id
    with open(session_file, 'r') as f:
        return f.read().strip()

def download_inputs(year, input_dir, session_id, session_file):
    if not os.path.isdir(input_dir):
        os.makedirs(input_dir)
    for day in range(1, min(25, (datetime.datetime.utcnow() - datetime.datetime(year, 11, 30, 5, 0, 0)).days)+1):
        fn = os.path.join(input_dir, 'day{0:02}.txt'.format(day))
        if os.path.exists(fn):
            continue
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input",
                                cookies={'session': get_cookie(session_id, session_file)})
        print(f"download {fn}: {response.status_code} {response.reason}")
        if response.status_code != 200:
            continue
        with open(fn, 'w') as f:
            f.write(response.text)

def create_fixture(name, fn):
    def with_file(fn, read):
        with open(fn, 'r') as f:
            return read(f)
    globals().update({
        f"{name}_text"        : pytest.fixture(lambda: with_file(fn, lambda f: f.read().strip())),
        f"{name}_raw"         : pytest.fixture(lambda: with_file(fn, lambda f: f.read())),
        f"{name}_lines"       : pytest.fixture(lambda: with_file(fn, lambda f: [line.strip() for line in f])),
        f"{name}_numbers"     : pytest.fixture(lambda: with_file(fn, lambda f: [int(line.strip()) for line in f])),
        f"{name}_number"      : pytest.fixture(lambda: with_file(fn, lambda f: int(f.read()))),
        f"{name}_grid"        : pytest.fixture(lambda: with_file(fn, lambda f: [row.split() for row in f])),
        f"{name}_number_grid" : pytest.fixture(lambda: with_file(fn, lambda f: [[int(s) for s in row.split()] for row in f]))
    })

def create_fixtures(year, input_dir):
    for day in range(1, min(25, (datetime.datetime.utcnow() - datetime.datetime(year, 11, 30, 5, 0, 0)).days)+1):
        create_fixture("day{0:02}".format(day), os.path.join(input_dir, "day{0:02}.txt".format(day)))

def pytest_sessionstart(session):
    year = session.config.getoption('aoc_year') or session.config.getini('aoc_year')
    input_dir = session.config.getoption('aoc_input_dir') or session.config.getini('aoc_input_dir')
    session_id = session.config.getoption('aoc_session_id') or session.config.getini('aoc_session_id')
    session_file = session.config.getoption('aoc_session_file') or session.config.getini('aoc_session_file')
    if year:
        download_inputs(int(year), input_dir, session_id, session_file)
        create_fixtures(int(year), input_dir)
