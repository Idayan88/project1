#!/bin/bash
echo "Starting tpp_app..."
sh /usr/local/bin/tpp/prereq.sh
source /etc/tpp/venv/bin/activate
python3 /usr/local/bin/tpp/app.py

