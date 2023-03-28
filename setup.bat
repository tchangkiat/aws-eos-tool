echo Upgrading pip
python -m pip install --upgrade pip

echo Installing virtualenv
python -m pip install --user virtualenv

echo Creating virtual environment...

python -m virtualenv eks-eos -p python

echo Installing dependencies...
eks-eos\Scripts\python.exe -m pip install --upgrade pip
eks-eos\Scripts\python.exe -m pip install -r requirements.txt
