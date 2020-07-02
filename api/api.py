import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from flask import jsonify
import logging

from src.utils.graphManager import executeNode

import os
import pathlib
import argparse
import sys

from src.projalgoGlobal import projectGlobal
from src.projalgoChoreo import projectChoreo
from src.projalgoRoles import projRoles
from src.utils.formatting import removeGroups

def getRoles():
    return ['Florist', 'Driver', 'Customer']


def reinit(filename):
    file = open(os.path.join(filename), 'r')
    data = file.readlines()
    file.close()

    target='src/resources/'

    _data = removeGroups(data)

    projectGlobal(_data, target)
    projectChoreo(_data, target)

    for role in getRoles():
        projRoles(_data, target, role)




logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, expose_headers='Authorization')

# Nassim
@app.route('/process', methods=['POST', 'GET'])
def processData():
   data = request.get_json(silent=True)
   status = executeNode(data)
   
   return status, 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/reinit', methods=['POST', 'GET'])
def reinitialise():
   filename = '../globalDCRs/shipvX.txt'
   reinit(filename)
   
   return 'ok', 200, {'Access-Control-Allow-Origin': '*'}




if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

