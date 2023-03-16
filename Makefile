env:
	sudo apt install python3-pip
	pip3 install virtualenv
	python3 -m venv env

install: requirements.txt 
	pip3 install -r requirements.txt 

run:
	python main.py