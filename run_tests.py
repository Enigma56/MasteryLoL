import sys
import unittest

from dotenv import load_dotenv

if __name__ == "__main__":
    print('Using Python version {0!s}'.format(sys.version))
    print("Loading Environment variables")
    load_dotenv()
    #app = Flask(__name__)
    #app.run(debug=True)

    test_suite = unittest.TestLoader().discover('test')
    test_results = unittest.TextTestRunner(verbosity=2).run(test_suite)

    if not test_results.wasSuccessful():
        sys.exit(1)
