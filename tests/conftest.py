# Add command line argument to specify the model path

import importlib
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent


def pytest_addoption(parser):
    parser.addoption("--model", action="store", default="sm")


def pytest_configure(config):
    model = config.getoption("--model")
    config.option.model = model


@pytest.fixture
def model(request):
    return request.config.option.model


@pytest.fixture
def package(model):
    package_name = f"en_us_address_ner_{model}"
    paths = (REPO_ROOT / "models" / model / "package").glob(
        f"{package_name}-*/{package_name}"
    )
    path = next(paths)
    try:
        sys.path.append(str(path.parent))
        yield importlib.import_module(package_name)
    finally:
        sys.path.remove(str(path.parent))
