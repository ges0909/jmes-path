def setup_module(module):
    pass


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


# -- class


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


# -- function


def test_1(fixture):
    assert "injected" in fixture


def test_2():
    assert True
