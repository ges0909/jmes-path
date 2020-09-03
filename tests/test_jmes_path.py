import jmespath
import pytest

from impl.random_functions import RandomFunctions


@pytest.fixture
def data():
    return {
        "key": ["a", "b", "c"],
    }


@pytest.fixture
def data2():
    return {
        "cmts #1": [
            {
                "model": "A",
                "vendor": "A GmbH",
                "mac": "11:11:11:11:11:11:11:11",
            },
            {
                "model": "B",
                "vendor": "B AG",
                "mac": "22:22:22:22:22:22:22:22",
            },
        ],
        "cmts #2": [
            {
                "model": "A",
                "vendor": "A GmbH",
                "mac": "33:33:33:33:33:133:33:133",
            },
        ],
    }


def test_array_access(data):
    assert jmespath.search("key[0]", data) == "a"


def test_on_of(data):
    options = jmespath.Options(custom_functions=RandomFunctions())
    result = jmespath.search("one_of(key)", data, options=options)
    assert result in ("a", "b", "c")


def test_mac_by_model(data2):
    result = jmespath.search("*[?model=='A'].mac[]", data2)
    assert result == ["11:11:11:11:11:11:11:11", "33:33:33:33:33:133:33:133"]


def test_one_of_mac_by_model(data2):
    options = jmespath.Options(custom_functions=RandomFunctions())
    result = jmespath.search("one_of(*[?model=='A'].mac[])", data2, options=options)
    assert result in ("11:11:11:11:11:11:11:11", "33:33:33:33:33:133:33:133")


def test_some_of_mac_by_model(data2):
    options = jmespath.Options(custom_functions=RandomFunctions())
    result = jmespath.search(
        "some_of(*[?model=='A'].mac[], `2`)", data2, options=options
    )
    assert all(
        r in ["11:11:11:11:11:11:11:11", "33:33:33:33:33:133:33:133"] for r in result
    )
