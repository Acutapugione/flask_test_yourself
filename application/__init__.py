from flask import Flask



flask_app = Flask(__name__, template_folder="../tamplates")


from . import routes
