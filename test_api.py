# allows HTTP requests to be sent
import requests
# for spawning child applications - here used to create server
import pexpect
# testing framework of choice
import pytest
# offers high-level operations on files and collections of files - used here for dir removal
import shutil
# creates temporary files and directories
import tempfile
# provides functions for interacting with machines os - used here to delete file
import os

# SETUP ------------------------------------------------------------------------------------------------------------#


class TestAPI():
    """
    - @pytest.fixture declares a fixture - a pytest mechanism which provides a fixed baseline allows (functions or
    methods to be declared) and where tests can be repeatedly executed. - fixtures are an alternative to classic
    xunit-style setup (setup/teardown - setup is used to setup items or state that need to exist for the test to run,
    teardown - is used to remove the newly created items from setup)
    - (autouse=True) allows the fixture to run without a test
    """

    @pytest.fixture(autouse=True)
    # self is passed in to provide access to super class, the class must always be referenced by using self param
    # tmp_dir is passed in to be assigned to self.tmp
    def setup(self, tmp_dir):
        # root
        self.url = 'http://127.0.0.1:5000'
        self.tmp = tmp_dir

    @pytest.fixture()
    def tmp_dir(self):
        # create temporary directory, call .mkdtemp method
        tmp = tempfile.mkdtemp(prefix="pcrud")
        # yield - pytest statement used instead of `return` to send back value
        yield tmp
        # rm temp dir
        shutil.rmtree(tmp)

    @pytest.fixture(autouse=True)
    def start_server(self):
        # use pexpect to start server in the background - so that running tests aren't blocked
        server = pexpect.spawn("python api.py " + self.tmp)
        server.expect('Running on http://127.0.0.1:5000')
        yield server
        # stop the background process
        server.kill(9)

# TEST ------------------------------------------------------------------------------------------------------------#

    def test_index(self):
        # get request to index endpoint (local server:port)
        r = requests.get(self.url)
        # check for success status code
        assert r.status_code == 200

    def test_post_create(self):
        # server response header - var needed to declare the data type used in the requests
        content_header = {'Content-Type': 'application/json'}
        # var needed to indicate the info that will be requested
        data = {'name': 'test-file', 'contents': 'hello'}
        # create response object `r` which makes POST request to'/files/create' end point
        r = requests.post(self.url + "/files/create", headers=content_header, json=data)

        # call .status_code method to check for 201 created status code
        assert r.status_code == 201
        # call .text method to read results of servers response and check that a POST request was used to create a file
        assert r.text == "File 'test-file' created."

        # open file (path/url, permissions) - "r" == reading rights
        file_object = open(self.tmp + "/test-file", "r")
        read_content = file_object.read()
        file_object.close()
        assert read_content == "hello"

    def test_get_read(self):
        expected_contents = "contents of the test file"
        # open file (file_path/url, mode/permissions) - "r" == reading rights
        file_object = open(self.tmp + '/test-file', "w")
        # call .write method to append content
        file_object.write(expected_contents)
        file_object.close()

        # create response object for 'read' endpoint
        r = requests.get(self.url + "/files/read/test-file")
        assert r.status_code == 200
        assert r.text == expected_contents

    def test_put_update(self):
        f = open(self.tmp + '/test-file', "w")
        f.write('boring old contents')
        f.close()

        expected_new_contents = 'new shiny updated contents'

        content_header = {'Content-Type': 'application/json'}
        data = {'contents': expected_new_contents}
        r = requests.put(self.url + "/files/update/test-file", headers=content_header, json=data)

        assert r.status_code == 200
        assert r.text == "File 'test-file' in '" + self.tmp + "' updated."

        file_object = open(self.tmp + "/test-file", "r")
        read_content = file_object.read()
        file_object.close()
        assert read_content == expected_new_contents

    def test_delete_delete(self):
         write_file(self.tmp+'/test-file', 'goodbye')
         r = requests.delete(self.url+"/files/delete/test-file")

         assert r.status_code == 200
         "File 'test-file-to-delete' deleted from '"+self.tmp+"'."
         assert os.path.exists(self.tmp+'/test-file') == False

# REUSABLE FUNCTIONS & VARS -------------------------------------------------------------------------------------------------#

def write_file(filename, contents):
    f = open(filename, "w")
    f.write(contents)
    f.close()
    return contents