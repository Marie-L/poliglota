from flask import Flask, request
import sys

app = Flask(__name__)

# use sys to fetch first argument from command line when server starts
app.config['store'] = sys.argv[1]
# save it to the app's config object
store = app.config.get('store')

@app.route('/')
def index():
    return "Welcome home"

@app.route('/files/create', methods=['POST'])
def create():
    data = request.get_json()
    name, contents = data['name'], data['contents']

    f = open(store+'/'+name, 'w')
    f.write(contents)
    f.close()

    # formatted string, a new resource has been created
    return "File '{}' created.".format(name), 201

# the variable name is passed inside < > in the url, then it's passed through as a param in the def function
@app.route('/files/read/<filename>')
def read(filename):
    f = open(store+'/'+filename, "r")
    contents = f.read()
    f.close()
    return contents


app.run(debug=True)

