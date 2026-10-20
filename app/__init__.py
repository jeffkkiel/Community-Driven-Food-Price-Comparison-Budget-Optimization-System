from flask import Flask

app = Flask(__name__)

from app import routes  # isort: skip  # noqa: E402
