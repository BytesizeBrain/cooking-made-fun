# Testing Flask
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome home, my world."

#GET: retrieve something
@app.route("/hello", methods=["GET"])
def hello_get():
    return "Hello, world! Greetings from the GET API."


# @app.route("/users/<username>")
# def greet_user(username):
#     return f"Ello, {username}! Greetings from Cal Poly Pomona."

#POST: create something
@app.route("/hello", methods=["POST"])
def hello_post():
    data = request.json
    return jsonify({"message": "POST request received.", "your_data": data}), 201

#DELETE: delete something
@app.route("/hello", methods=["DELETE"])
def hello_delete():
    return "DELETE request received. Resource deleted.", 200

#PUT: replace something
@app.route("/hello", methods=["PUT"])
def hello_put():
    data = request.json
    return jsonify({"message": "Resource replaced", "changes": data})

#PATCH: partially update something
@app.route("/hello", methods=["PATCH"])
def hello_patch():
    data = request.json
    return jsonify({"message": "Resource updated!", "changes": data})

#RUN THE PROGRAM
if __name__ == "__main__":
    app.run(debug=True)