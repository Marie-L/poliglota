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


app.run(debug=True)

