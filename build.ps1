del -r dist
pip install pyinstaller
pip install -r requirements.txt

pyinstaller --onefile -w .\FalconShaker.py
cp .\Profiles\ .\dist\
cp '.\Sound Files\' .\dist\

Compress-Archive -Update .\dist\ falcon-shaker.zip