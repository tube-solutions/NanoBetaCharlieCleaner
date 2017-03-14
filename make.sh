#!/bin/bash

#make sure pip is installed
easy_install pip

#make sure virtualenv is installed
pip install virtualenv

#create virtualenv and install reqs
virtualenv --python=python3 .env
source .env/bin/activate
pip install -r requirements.txt

#create executable
echo -e "cd $PWD\nsource .env/bin/activate\npython NanoBetaCharlieMaker.py" >> NanoBetaCharlie.command

#Authorize Executable
chmod 777 NanoBetaCharlie.command
