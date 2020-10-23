import random

import pytest
from flaky import flaky

# class TestFlaky:
#     def setup_class(cls):
#         pass
#
#     def teardown_class(cls):
#         pass
#
#     def setup_method(self):
#         pass
#
#     def teardown_method(self):
#         pass
#
#     @flaky(max_runs=3)
#     def test_flaky(self):
#         number = random.randint(1, 2)
#         assert number % 2 == 0
#
#     @pytest.mark.flaky(max_runs=3)
#     def test_pytest_flaky(self):
#         number = random.randint(1, 2)
#         assert number % 2 == 0


@flaky(max_runs=3)
def test_flaky():
    number = random.randint(1, 2)
    assert number % 2 == 0


@pytest.mark.flaky(max_runs=3)
def test_pytest_flaky():
    number = random.randint(1, 2)
    assert number % 2 == 0
