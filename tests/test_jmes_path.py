import random
from typing import List, Any

import jmespath
import pytest
from jmespath import functions


class AddOns(functions.Functions):
    """selects randomly element(s) from list"""

    @functions.signature({"types": ["array"]})
    def _func_one_of(self, iterable):
        """selects randomly one element from list"""
        return random.choice(iterable)

    @functions.signature({"types": ["array"]}, {"types": ["number"]})
    def _func_some_of(self, iterable, number: int) -> List[Any]:
        """selects randomly `number` elements from list"""
        return random.sample(iterable, number if number <= len(iterable) else len(iterable))

    @functions.signature({"types": ["array"]})
    def _func_unique(self, iterable):
        """makes list elements unique"""
        return list(set(iterable))

    @functions.signature({"types": ["array"]}, {"types": ["string"]})
    def _func_group_by(self, iterable, key: str):
        """groups list elements by key"""

        groups = {}
        for o in iterable:
            if key in o:
                if o[key] not in groups:
                    groups[o[key]] = []
                groups[o[key]].append(o)
        return groups

    @functions.signature({"types": ["array"]}, {"types": ["string"]})
    def _func_first_of_grouped_by(self, iterable, key: str):
        """ """
        groups = self._func_group_by(iterable=iterable, key=key)
        return [v[0] for v in groups.values()]

    @functions.signature({"types": ["array"]}, {"types": ["string"]})
    def _func_one_of_grouped_by(self, iterable, key: str):
        """ """
        groups = self._func_group_by(iterable=iterable, key=key)
        return [self._func_one_of(v) for v in groups.values()]

    @functions.signature({"types": ["array"]}, {"types": ["string"]})
    def _func_some_of_grouped_by(self, iterable, key: str):
        """ """
        groups = self._func_group_by(iterable=iterable, key=key)
        return [self._func_some_of(v) for v in groups.values()]


@pytest.fixture
def options():
    """custom funtion fixture for test support"""
    return jmespath.Options(custom_functions=AddOns())


data = {
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
            "mac": "33:33:33:33:33:33:33:33",
        },
    ],
}


def test_array_element_access():
    assert jmespath.search("x[0]", data={"x": ["a", "b", "c"]}) == "a"


def test_select_one_element_of_array_randomly(options):
    result = jmespath.search("one_of(x)", data={"x": ["a", "b", "c"]}, options=options)
    assert result in ["a", "b", "c"]


@pytest.mark.repeat(9)
def test_select_one_element_of_array_randomly_with_pipe(options):
    result = jmespath.search("x | one_of(@)", data={"x": ["a", "b", "c"]}, options=options)
    assert result in ["a", "b", "c"]


def test_select_some_elements_of_array_randomly(options):
    result = jmespath.search("x | some_of(@, `2`)", data={"x": ["a", "b", "c"]}, options=options)
    assert set(result).issubset({"a", "b", "c"})


def test_select_some_elements_of_array_randomly_with_pipe(options):
    """'number' is greater than the number of set elements"""
    result = jmespath.search("x | some_of(@, `9`)", data={"x": ["a", "b", "c"]}, options=options)
    assert set(result).issubset({"a", "b", "c"})


def test_filter_by_attribute_and_flatten(options):
    result = jmespath.search("*[?model=='A'].mac[]", data)
    assert result == ["11:11:11:11:11:11:11:11", "33:33:33:33:33:33:33:33"]


def test_filter_by_attribute_and_flatten_and_select_one(options):
    result = jmespath.search("one_of(*[?model=='A'].mac[])", data, options=options)
    assert result in ("11:11:11:11:11:11:11:11", "33:33:33:33:33:33:33:33")


def test_filter_by_attribute_and_flatten_and_select_some(options):
    result = jmespath.search("some_of(*[?model=='A'].mac[], `2`)", data, options=options)
    assert all(r in ["11:11:11:11:11:11:11:11", "33:33:33:33:33:33:33:33"] for r in result)


@pytest.mark.repeat(9)
def test_miscellenoeus(options):
    result = jmespath.search("*", data, options=options)
    assert result == list(data.values())
    #
    result = jmespath.search("*[]", data, options=options)
    assert result == [val for val_list in data.values() for val in val_list]  # flattened
    #
    result = jmespath.search("*[].model", data, options=options)
    assert result == ["A", "B", "A"]


def test_unique(options):
    result = jmespath.search("*[].model | unique(@)", data, options=options)
    assert set(result) == {"A", "B"}


def test_unique_and_sort(options):
    result = jmespath.search("*[].model | unique(@) | sort(@)", data, options=options)
    assert result == ["A", "B"]


def test_group_by(options):
    result = jmespath.search("*[] | group_by(@, `model`)", data, options=options)
    assert result == {
        "A": [
            {"model": "A", "vendor": "A GmbH", "mac": "11:11:11:11:11:11:11:11"},
            {"model": "A", "vendor": "A GmbH", "mac": "33:33:33:33:33:33:33:33"},
        ],
        "B": [
            {"model": "B", "vendor": "B AG", "mac": "22:22:22:22:22:22:22:22"},
        ],
    }


def test_group_by_and_select_first(options):
    result = jmespath.search("*[] | first_of_grouped_by(@, `model`)", data, options=options)
    assert result == [
        {"model": "A", "vendor": "A GmbH", "mac": "11:11:11:11:11:11:11:11"},
        {"model": "B", "vendor": "B AG", "mac": "22:22:22:22:22:22:22:22"},
    ]


def test_group_by_and_select_one_of(options):
    result = jmespath.search("*[] | one_of_grouped_by(@, `model`)", data, options=options)
    assert result == [
        {"model": "A", "vendor": "A GmbH", "mac": "11:11:11:11:11:11:11:11"},
        {"model": "B", "vendor": "B AG", "mac": "22:22:22:22:22:22:22:22"},
    ] or [
        {"model": "A", "vendor": "A GmbH", "mac": "33:33:33:33:33:33:33:33"},
        {"model": "B", "vendor": "B AG", "mac": "22:22:22:22:22:22:22:22"},
    ]
