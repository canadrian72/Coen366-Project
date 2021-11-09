import requests
from flask import Flask, render_template, Response, request
from Client import Client, RegisterWithServer, DeRegisterFromServer, RemoveFilesFromServer

app = Flask("__main__", static_url_path='', static_folder='build', template_folder='build')
client = Client()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    register_request = request.get_json(force=True)
    name = register_request['name']
    client.name = name
    registration = RegisterWithServer(client)
    registration.start()
    return {'register': registration.join()}


@app.route("/de_register", methods=["POST"])
def de_register():
    de_registration = DeRegisterFromServer(client)
    de_registration.start()
    de_registration.join()
    return Response(status=201)


@app.route("/remove_files", methods=["POST"])
def remove_files():
    remove = RemoveFilesFromServer(client)
    remove.start()
    remove.join()
    return Response(status=201)


@app.route("/shutdown", methods=['GET'])
def shutdown():
    shutdown_func = requests.request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."


def start():
    app.run(host='0.0.0.0', threaded=True, port=5001)


def stop():
    resp = requests.get('http://localhost:5001/shutdown')


start()
stop()
