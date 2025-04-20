import pytest
import requests

def test_reachabillity():
    response = requests.get("http://16.171.205.23:5000")
    assert response.status_code == 200 , f"site not reachable {response.status_code}"



