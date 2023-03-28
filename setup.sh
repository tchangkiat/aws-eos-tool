if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv could not be found."
    echo "You need to execute the command 'python -m pip install virtualenv'"
    exit
fi

echo Creating virtual environment...
virtualenv eks-eos -p python3

echo Virtual environment created at `pwd`/eks-eos

echo Activating virtual environment with 'source `pwd`/eks-eos/bin/activate'

echo "OS is $OSTYPE";

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    set SCRIPTPATH=eks-eos/bin
elif [[ "$OSTYPE" == "darwin"* ]]; then
    export SCRIPTPATH=eks-eos/bin
elif [[ "$OSTYPE" == "cygwin" ]]; then
    export SCRIPTPATH=eks-eos/Scripts
elif [[ "$OSTYPE" == "msys" ]]; then
    export SCRIPTPATH=eks-eos/Scripts
elif [[ "$OSTYPE" == "win32" ]]; then
    export SCRIPTPATH=eks-eos/Scripts
else
    echo "Couldn't find activate script.";
    exit 1;
fi

echo Activating virtual environment with 'source `pwd`/$SCRIPTPATH/activate'
source $SCRIPTPATH/activate

echo Installing dependencies...

$SCRIPTPATH/python -m pip install -r requirements.txt;

echo "Done"
	
