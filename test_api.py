import requests
import pexpect
import pytest
import shutil
import tempfile


# define class
class TestAPI():

    # declare a new fixture - a pytest mechanism which allows us to declare functions or method which are common to tests within a suite
    # (autouse=True) is passed as a param so that it doesn't need to be passed within the tests
    @pytest.fixture(autouse=True)
    def setup(self, tmp_dir):
        self.url = 'http://127.0.0.1:5000'
        self.tmp = tmp_dir

    @pytest.fixture()
    def tmp_dir(self):
        # create temporary directory
        tmp = tempfile.mkdtemp(prefix = "pcrud")
        # yield sends back value
        yield tmp
        # rm temp dir
        shutil.rmtree(tmp)

    @pytest.fixture(autouse=True)
    def start_server(self):
        # use pexpect to start server in the background - so that running tests aren't blocked
        server = pexpect.spawn("python api.py "+self.tmp)
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

    def test_post_create(self):
        # var needed to declare the data type used in the requests
        content_header = {'Content-Type': 'application/json'}
        # var needed to indicate the info that will be requested
        data = {'name': 'test-file', 'contents': 'hello'}
        # make post request to'/files/create' end point
        r = requests.post(self.url + "/files/create", headers=content_header, json=data)

        # check create status code
        assert r.status_code == 201
        # check that a POST request is used to create a file
        assert r.text == "File 'test-file' created."

        file_object = open(self.tmp+"/test-file", "r")
        read_content = file_object.read()
        file_object.close()
        assert read_content == "hello"