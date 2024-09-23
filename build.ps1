# Thanks to kungfoo for this script.
# Needs some debugging to get to run correctly, more so adding to repo for isntructions on pyinstaller build.
del -r dist
pip install pyinstaller
pip install -r requirements.txt

pyinstaller --onefile -w .\FalconShaker.py
cp -r .\Profiles\ .\dist\
cp -r '.\Sound Files\' .\dist\

Compress-Archive -Update .\"FalconShaker 1.3"\ "FalconShaker 1.3.zip"