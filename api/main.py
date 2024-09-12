from flask import Flask

if __name__ == "__main__":
    app = Flask('api')
    app.run(debug=True)
