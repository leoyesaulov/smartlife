check_system:
	echo $(SHELL)

setup:
  	python3 -m venv venv
  	source venv && pip install -r requirements.txt && python setup.py && python main.py

clean:
	rmdir /s /q __pycache__
	rmdir /s /q venv

run:
  	source venv && pip install -r requirements.txt && python main.py

freeze:
	venv\Scripts\activate && pip freeze > requirements.txt
