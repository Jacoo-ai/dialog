from services.flask_service import app as flask_server
# import requests
import time

import nltk

if __name__ == "__main__":

    # nltk.download('punkt')
    flask_server.flask_server_start(port=5000)
