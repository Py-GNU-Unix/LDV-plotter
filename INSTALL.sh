#!/bin/bash
python3 -m venv venv

source venv/bin/activate

python3 -m pip install -r REQUIREMENTS.txt

mkdir /opt/LDV-plotter
cp -r ./images ./scripts ./stylesheets ./venv /opt/LDV-plotter/
cp ./root/bin/ldv-plt /bin/ldv-plt
cp ./root/usr/share/applications/LDV-plotter.desktop /usr/share/applications/LDV-plotter.desktop

