del -r dist
pip install pyinstaller
pip install -r requirements.txt

pyinstaller --onefile -w .\FalconShaker.py
cp -r .\Profiles\ .\dist\
cp -r '.\Sound Files\' .\dist\

Compress-Archive -Update .\dist\ falcon-shaker.zip