from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome home"

@app.route('/files/create', methods=['POST'])
def create():
    data = request.get_json()
    name, contents = data['name'], data['contents']

    f = open(name, 'w')
    f.write(contents)
    f.close()

    # formatted string, a new resource has been created
    return "File '{}' created.".format(name), 201


app.run(debug=True)

