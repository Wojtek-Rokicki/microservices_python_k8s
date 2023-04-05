import os, gridfs, pika, json, sys # gridfs enables storing larger files (>16MB) in MongoDB; pika interface to rabbitmq
from flask import Flask, request
from flask_pymongo import PyMongo

# At first not implemented
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
try:
    mongo_video = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos") # gives us the access to the host of clusters
except Exception as err:
    print(err, file=sys.stderr)

try:
    fs = gridfs.GridFS(mongo_video.db) # it divides the file into parts, or chunks enabling larger files, and each chunk is stored as separate file
    # collections in MongoDB are just like tables
except Exception as err:
    print(err, file=sys.stderr)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq")) # synchronous
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err
    
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    if err:
        return err
    
    access = json.loads(access)

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400
        
        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access)

            if err:
                return err
            
        return "success!", 200
    else:
        return "not authorized", 401

@server.route("/download", methods=["GET"])
def download():
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)