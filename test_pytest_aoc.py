import datetime

import pytest

import pytest_aoc

def test_get_cookie(testdir):
    testdir.maketxtfile(cookie='spam')
    testdir.makepyfile(test_get_cookie='''
        import pytest_aoc
        def test_get_cookie_from_session_id():
            assert pytest_aoc.get_cookie('eggs', 'cookie.txt') == 'eggs'
        def test_get_cookie_from_session_file():
            assert pytest_aoc.get_cookie(None, 'cookie.txt') == 'spam'
    ''')
    testdir.runpytest().assert_outcomes(passed=2)

def test_create_input_dir_1(testdir):
    testdir.makepyfile(test_download_inputs='''
        import pytest_aoc
        def test_create_input_dir_1(mocker):
            makedirs = mocker.patch('os.makedirs')
            pytest_aoc.create_input_dir('input')
            makedirs.assert_called_once_with('input')
    ''')
    testdir.runpytest().assert_outcomes(passed=1)

def test_create_input_dir_2(testdir):
    testdir.mkdir('input')
    testdir.makepyfile(test_download_inputs='''
        import pytest_aoc
        def test_create_input_dir_1(mocker):
            makedirs = mocker.patch('os.makedirs')
            pytest_aoc.create_input_dir('input')
            makedirs.assert_not_called()
    ''')
    testdir.runpytest().assert_outcomes(passed=1)

@pytest.mark.freeze_time('2018-12-01 04:59:59.999')
def test_get_available_days_before():
    assert pytest_aoc.get_available_days(2018, datetime.datetime.utcnow()) == []

@pytest.mark.freeze_time('2014-12-18 16:16')
def test_get_available_days_during():
    assert pytest_aoc.get_available_days(2014, datetime.datetime.utcnow()) == [*range(1, 18+1)]

@pytest.mark.freeze_time('2018-08-14 19:26')
def test_get_available_days_after():
    assert pytest_aoc.get_available_days(2017, datetime.datetime.utcnow()) == [*range(1, 25+1)]

def test_download_inputs_1(testdir):
    testdir.makepyfile(test_download_inputs='''
        import pytest_aoc
        def test_download_inputs(responses):
            responses.add(responses.GET, 'https://adventofcode.com/2018/day/1/input', body='spam')
            pytest_aoc.download_inputs(2018, [1], '.', 'spam', '.cookie')
            with open('day01.txt', 'r') as f:
                assert f.read() == 'spam'
    ''')
    testdir.runpytest().assert_outcomes(passed=1)

def test_download_inputs_2(testdir):
    testdir.makepyfile(test_download_inputs='''
        import os.path
        import pytest_aoc
        def test_download_inputs(responses):
            responses.add(responses.GET, 'https://adventofcode.com/2018/day/1/input', status=400)
            pytest_aoc.download_inputs(2018, [1], '.', 'spam', '.cookie')
            assert not os.path.exists('day01.txt')
    ''')
    testdir.runpytest().assert_outcomes(passed=1)

@pytest.mark.freeze_time('2018-12-01 05:00:00')
@pytest.mark.parametrize('name,text,value', [
    ('text', 'spam ', '"spam"'),
    ('raw', 'spam ', '"spam "'),
    ('lines', 'spam\neggs\n', '["spam", "eggs"]'),
    ('numbers', '529\n127\n', '[529, 127]'),
    ('number', '529', '529'),
    ('grid', 'a b\nc d\n', '[["a", "b"], ["c", "d"]]'),
    ('number_grid', '1 2\n3 4\n', '[[1, 2], [3, 4]]')
])
def test_fixture(testdir, name, text, value):
    with open('day01.txt', 'w') as f:
        f.write(text)
    testdir.makepyfile(test_fixture=f'def test_{name}(day01_{name}): assert day01_{name} == {value}')
    testdir.runpytest('--aoc-year=2018', '--aoc-input-dir=.').assert_outcomes(passed=1)

def test_module_reload(): # this probably breaks pytest assertion rewriting...
    from importlib import reload
    reload(pytest_aoc)
