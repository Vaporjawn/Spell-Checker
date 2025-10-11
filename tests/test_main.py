import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main


@pytest.fixture
def app():
    return main.app


@pytest.fixture
def test_client(app):
    app.config["TESTING"] = True
    return app.test_client()


def test_title(test_client):
    response = test_client.get("/")
    assert "Check Yo Self" in response.data.decode("utf-8")


def test_text_box(test_client):
    response = test_client.get("/")
    assert "Write something here to have it spell checked!" in response.data.decode(
        "utf-8"
    )
