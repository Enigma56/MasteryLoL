from flask import Flask
import account_data

from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    account_data.get_account("Its Just A Prank", "6969")

    app = Flask('api')
    app.run(debug=True)
