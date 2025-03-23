setup:
	py -m venv venv
	venv\Scripts\activate && pip install -r requirements.txt && py setup.py && py main.py

clean:
	rmdir /s /q __pycache__
	rmdir /s /q venv

run:
	venv\Scripts\activate && py main.py

upd_req:
	venv\Scripts\activate && pip freeze > requirements.txt