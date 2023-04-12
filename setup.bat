echo Upgrading pip
python -m pip install --upgrade pip

echo Installing virtualenv
python -m pip install --user virtualenv

echo Creating virtual environment...

python -m virtualenv eos-tool -p python

echo Installing dependencies...
eos-tool\Scripts\python.exe -m pip install --upgrade pip
eos-tool\Scripts\python.exe -m pip install -r requirements.txt
