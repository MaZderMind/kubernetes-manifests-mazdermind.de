.PHONY: all setup apply format

all: apply

setup:
	virtualenv -p python3 venv
	venv/bin/pip install -r requirements.txt

format:
	venv/bin/python3 formatter.py templates output

apply: format
	kubectl apply --recursive -f output
