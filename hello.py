# Testing Flask
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, world!"

@app.route("/users/<username>")
def greet_user(username):
    return f"Ello, {username}! Greetings from Cal Poly Pomona."

    



#RUN THE PROGRAM
if __name__ == "__main__":
    app.run(debug=True)