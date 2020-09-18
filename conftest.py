def pytest_sessionstart(session):
    pass


def pytest_sessionfinish(session, exitstatus):
    pass


def pytest_generate_tests(metafunc):
    if "fixture" in metafunc.fixturenames:
        metafunc.parametrize("fixture", ["injected #1", "injected #2"])
