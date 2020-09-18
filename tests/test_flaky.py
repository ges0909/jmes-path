import random

import pytest
from flaky import flaky


@flaky(max_runs=3)
def test_flaky():
    number = random.randint(1, 2)
    assert number % 2 == 0


@pytest.mark.flaky(max_runs=3)
def test_pytest_flaky():
    number = random.randint(1, 2)
    assert number % 2 == 0
