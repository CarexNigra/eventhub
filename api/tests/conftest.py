from unittest.mock import MagicMock

from fastapi.testclient import TestClient
import pytest

from api.app import app, create_kafka_producer


@pytest.fixture(scope="session")
def kafka_producer_mock():
    m = MagicMock()
    m.produce = MagicMock()
    yield m


@pytest.fixture(scope="function", autouse=True)
def reset_mock(kafka_producer_mock):
    yield
    kafka_producer_mock.reset_mock()


@pytest.fixture(scope="session")
def client(kafka_producer_mock) -> TestClient:
    app.dependency_overrides[create_kafka_producer] = lambda: kafka_producer_mock
    return TestClient(app)
