from flask import Flask

app = Flask(__name__)

from ieoapp import routes
