# pytest-aoc

This pytest plugin downloads puzzle inputs for [Advent of Code][1] and
synthesizes fixtures that you can use in your tests.

[1]: https://adventofcode.com/

## Installing and configuring

Installing is easy: `pip install pytest-aoc`. Next you will need to configure
_two_ things: for which event (year) the plugin should download inputs, and a
valid session cookie. These are normally valid for about a month or so.

To set the year, put it in `setup.cfg`:

    [tool:pytest]
    aoc_year = 2018

Then, put a valid session ID in a file named `.cookie` and also name this file
in your `.gitignore`.

With these two things in place, when running pytest, this plugin will download
any missing inputs, and generate pytest fixtures that you can use in your test
functions, see 'Using' and 'Fixtures', below.

## Using

With this plugin properly configured, you can write tests like this:

    def test_01a(day01_numbers):
        assert sum(day01_numbers) == 123

Here, the parameter `day01_numbers` is a fixture that contains the numbers on
each line in the file `input/day01.txt`.

## Fixtures

These fixtures are synthesized for each available day. They're not executed
until you ask for them in a test.

- `dayNN_text`: The text in the input file, but stripped of any leading and trailing whitespace.
- `dayNN_raw`: The raw text in the input file.
- `dayNN_lines`: A list of stripped lines.
- `dayNN_numbers`: A list of numbers.
- `dayNN_number`: A single number.
- `dayNN_grid`: A list of lists, representing a grid of textual values.
- `dayNN_number_grid`: A list of lists, representing a grid of numbers.

## Command-line and configuration options

You can pass the options from the command line or set them in setup.cfg. The
command line takes precedence.

- `--aoc-year`/`aoc_year`: The year for which to download puzzle inputs.
  (Mandatory)
- `--aoc-session-id`: The session ID to use for requesting puzzle inputs. This
  one has no equivalent setup.cfg key; that's a security feature. (Optional)
- `--aoc-session-file`/`aoc_session_file`: The file from which to read the
  session ID. (Optional; default `.cookie`)
- `--aoc-input-dir`/`aoc_input_dir`: The directory in which inputs are stored.
  Will be created if it doesn't exist. (Optional; default `input`)
