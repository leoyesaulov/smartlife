setup:
	py -m venv venv
	venv\Scripts\python -m pip install --upgrade pip
	pip install -r requirements.txt
	py main.py

clean:
	rmdir /s /q __pycache__
	rmdir /s /q venv

run:
	py main.py

upd_req:
	venv\Scripts\python -m pip install --upgrade pip
	pip freeze > requirements.txt