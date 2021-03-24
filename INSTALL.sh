#!/bin/bash
python3 -m pip install venv
python3 -m venv venv

source venv/bin/activate

python3 -m pip install -r REQUIREMENTS.txt

mkdir /opt/LDV-plotter
cp ./images ./scripts ./stylesheets ./venv /opt/LDV-plotter/
cp -fr ./root /

