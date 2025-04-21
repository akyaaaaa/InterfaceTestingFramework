import pytest

from utils.data_loader import load_json
from utils.logger import log_info


def test_example():
    log_info("This is a test log message.")
    assert True


@pytest.mark.parametrize("user", load_json("example_data.json",modelname='reqres.in_api')["users"])
def test_example1(user):
    assert user["id"] > 0
    assert "@" in user["email"]
