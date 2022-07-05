"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def one_member(id):
    member = jackson_family.get_member(id)
    return jsonify(member),200

@app.route('/member', methods=['POST'])
def add_member():

    jackson_family.first_name = request.json.get('first_name')
    jackson_family.age = request.json.get('age')
    jackson_family.lucky_numbers = request.json.get('lucky_numbers')
    jackson_family.id = request.json.get('id')

    if not jackson_family.first_name or jackson_family.first_name == "":
        return jsonify({"msg: Por favor, escriba un nombre"}), 404 

    if not jackson_family.age or jackson_family.age == "":
        return jsonify({"msg: Por favor, escriba su edad"}), 404 

    if not jackson_family.lucky_numbers or jackson_family.lucky_numbers == "":
        return jsonify({"msg: Por favor, escriba al menos un numero de la suerte"}), 404 

    member = {
        "first_name": jackson_family.first_name,
        "age": jackson_family.age,
        "lucky_numbers": jackson_family.lucky_numbers,
        "id": jackson_family.id
    }
    jackson_family.add_member(member)
    return jsonify(), 200


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.delete_member(id)
    return jsonify({"done":True}),200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)