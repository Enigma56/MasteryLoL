from flask import Flask
from dotenv import load_dotenv
import account_data

def hello_world():
    print("Hello!")

if __name__ == "__main__":
    load_dotenv()
    account_data.get_account("Its%20Just%20A%20Prank", "6969")

    app = Flask('api')
    app.run(debug=True)

