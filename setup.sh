#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=content_boost.py
flask run
