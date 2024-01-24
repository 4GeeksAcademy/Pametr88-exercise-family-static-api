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


@app.route("/member/<int:id>", methods=['GET'])
def get_member(id):
    try:
        member_needed = jackson_family.get_member(id)
        if member_needed:
            # Corregir las claves en el diccionario devuelto
            return {
                "name": member_needed["first_name"],
                "id": member_needed["id"],
                "age": member_needed["age"],
                "lucky_numbers": member_needed["Lucky Numbers"]
            }, 200
        else:
            return {"error": "The member does not exist"}, 404

    except:
        return {"error": "There was an error in the server"}, 500



@app.route("/member", methods=['POST'])
def post_new_member():
    try:
        first_name = request.json.get("first_name")
        age = request.json.get("age")
        lucky_numbers = request.json.get("lucky_numbers")
        id = request.json.get("id")

        new_member = {
            "first_name": first_name,
            "age": age,
            "id": jackson_family._generateId(),
            "lucky_numbers": lucky_numbers,
            "last_name": "Jackson"
        }

        jackson_family.add_member(new_member)

        return jsonify({"message": "Member added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/member/<int:id>", methods=["DELETE"])
def delete_member(id):
    try:
        member_deleted = jackson_family.delete_member(id)
        print("Members after deletion:", len(jackson_family.get_all_members()), jackson_family.get_all_members())
        if member_deleted:
            # Correct the return statement
            return jsonify({"done": True}), 200
        else:
            return jsonify({"message": "The member does not exist!"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)