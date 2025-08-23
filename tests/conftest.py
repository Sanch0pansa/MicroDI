import pytest
from src.micro_di import DIContainer

@pytest.fixture(scope="function")
def di() -> DIContainer:
    return DIContainer()