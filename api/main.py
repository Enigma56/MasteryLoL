from flask import Flask

def hello_world():
    print("Hello!")

if __name__ == "__main__":
    app = Flask('api')
    app.run(debug=True)

