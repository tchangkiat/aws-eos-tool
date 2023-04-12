if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv could not be found."
    echo "You need to execute the command 'python -m pip install virtualenv'"
    exit
fi

echo Creating virtual environment...
virtualenv eos-tool -p python3

echo Virtual environment created at `pwd`/eos-tool

echo Activating virtual environment with 'source `pwd`/eos-tool/bin/activate'

echo "OS is $OSTYPE";

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    set SCRIPTPATH=eos-tool/bin
elif [[ "$OSTYPE" == "darwin"* ]]; then
    export SCRIPTPATH=eos-tool/bin
elif [[ "$OSTYPE" == "cygwin" ]]; then
    export SCRIPTPATH=eos-tool/Scripts
elif [[ "$OSTYPE" == "msys" ]]; then
    export SCRIPTPATH=eos-tool/Scripts
elif [[ "$OSTYPE" == "win32" ]]; then
    export SCRIPTPATH=eos-tool/Scripts
else
    echo "Couldn't find activate script.";
    exit 1;
fi

echo Activating virtual environment with 'source `pwd`/$SCRIPTPATH/activate'
source $SCRIPTPATH/activate

echo Installing dependencies...

$SCRIPTPATH/python -m pip install -r requirements.txt;

echo "Done"
	
