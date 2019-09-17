from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome home"

@app.route('/files/create', methods=['POST'])
def create():
    # empty string, a new resource has been created
    return "", 201


app.run(debug=True)

