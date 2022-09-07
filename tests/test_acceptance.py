import pytest

from ert_config_parser import parse
from ert_config_parser._parse import tokenize

test_file = "test.ert"


def test_tokenize():
    assert tokenize("my token") == ["my", "token"]
    assert tokenize('"my" token') == ["my", "token"]
    with pytest.raises(ValueError):
        tokenize('"my ')
    assert tokenize('"my token"') == ["my token"]
    assert tokenize("my token -- comment") == ["my", "token"]
    assert tokenize("my token--comment") == ["my", "token"]
    assert tokenize('"my token"token2"token3"') == ["my token", "token2", "token3"]


def write_config(filename, content):
    with open(filename, "w") as f:
        f.write(content)


@pytest.mark.parametrize(
    "content, expected",
    [
        (
            """ NUM_REALIZATIONS 100
RANDOM_SEED 1234""",
            ["1234"],
        ),
        (
            """ NUM_REALIZATIONS 100
RANDOM_SEED \"1234\"""",
            ["1234"],
        ),
        (
            """ NUM_REALIZATIONS 100,
RANDOM_SEED 1234 -- comment""",
            ["1234"],
        ),
        (
            """ NUM_REALIZATIONS 100
RANDOM_SEED \"1234 1234\"""",
            ["1234 1234"],
        ),
        (
            """ NUM_REALIZATIONS 100
                RANDOM_SEED \"1234 1234\"""",
            ["1234 1234"],
        ),
        (
            """ NUM_REALIZATIONS 100
RANDOM_SEED 1234 1234""",
            ["1234", "1234"],
        ),
        ('RANDOM_SEED 1234 "12 34--"', ["1234", "12 34--"]),
        ('"RANDOM_SEED" 1234 "12 34--"', ["1234", "12 34--"]),  # edge case
    ],
)
def test_parse_random_seed_config(content, expected, tmp_path):
    write_config(tmp_path / test_file, content)
    assert parse(tmp_path / test_file, keywords=["RANDOM_SEED"]) == {
        "RANDOM_SEED": expected
    }


@pytest.mark.parametrize(
    "contents",
    [
        '"RANDOM_SEED " 1234',
        "random_seed 1234",
        '"random_seed 1234"',
    ],
)
def test_parse_ignores_not_the_keyword(contents, tmp_path):
    write_config(tmp_path / test_file, contents)
    assert parse(tmp_path / test_file, keywords=["RANDOM_SEED"]) == {}
