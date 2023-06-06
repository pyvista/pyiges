def pytest_addoption(parser):
    parser.addoption("--expect-full-module", action="store_true", default=False)
