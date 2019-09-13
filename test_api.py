import requests


# define class
class test_api():
    # define function, param self refers to the class itself

    def text_index(self):
        # get request to index endpoint (local server:port)
        r = requests.get("http://127.0.0.7:5000/")
        # check for success status code
        assert r.status_code == 200

