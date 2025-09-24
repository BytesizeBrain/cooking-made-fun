# Purpose of this .py file: to fulfill A3 requirement (individual per prompt)
# - Goal: Test HTTPS API end-point 
# By: Danny Tran
# - Test from a separate branch

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Testing API with HTTPS for Assignment #3 for CS 4800." \
    "<br><br>Please try adding /testingA3?name=(your name) at the end of current website link to try our 2nd page!" \
    "<br><br>For example: http://127.0.0.1:5000/testingA3?name=Danny" \
    "<br><br> The goal: practice routing pages & getting into HTTPS API."

@app.route('/testingA3', methods=['GET'])
def testingAPI():
    visitorName = request.args.get('name', 'stranger')
    response_data = {
        "message": f"Hello, {visitorName}!"
    }
    return jsonify(visitorName), 200

if __name__ == '__main__':
    app.run(debug=True)
