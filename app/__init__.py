from flask import Flask
import os 

template_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'templates')

static_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
static_dir = os.path.join(static_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

from app import routes