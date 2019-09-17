import requests
import pexpect
import pytest


# define class
class TestAPI():

    # declare a new fixture - a pytest mechanism which allows us to declare functions or method which are common to tests within a suite
    # (autouse=True) is passed as a param so that it doesn't need to be passed within the tests
    @pytest.fixture(autouse=True)
    def setup(self):
        self.url ='http://127.0.0.1:5000'

    def start_server(self):
        # use pexpect to start server in the background - so that running tests aren't blocked
        server = pexpect.spawn("python api.py")
        server.expect('Running on http://127.0.0.1:5000')
        yield server
        # stop the background process
        server.kill(9)

    # define function, param self refers to the class itself
    def test_index(self):
        # get request to index endpoint (local server:port)
        r = requests.get(self.url)
        # check for success status code
        assert r.status_code == 200
