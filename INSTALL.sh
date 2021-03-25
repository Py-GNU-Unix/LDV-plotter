#!/bin/bash

#     This file is part of LDV-plotter.
# 
#     LDV-plotter is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     LDV-plotter is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with LDV-plotter.  If not, see <https://www.gnu.org/licenses/>.

python3 -m venv venv

source venv/bin/activate

python3 -m pip install -r REQUIREMENTS.txt

mkdir /opt/LDV-plotter
cp -r ./images ./scripts ./stylesheets ./venv /opt/LDV-plotter/
cp ./root/bin/ldv-plt /bin/ldv-plt
cp ./root/usr/share/applications/LDV-plotter.desktop /usr/share/applications/LDV-plotter.desktop

