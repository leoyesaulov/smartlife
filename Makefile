check_system:
	echo $(SHELL)

setup:
	ifeq ($(SHELL), sh.exe)
	py -m venv venv
	venv\Scripts\activate && pip install -r requirements.txt && py setup.py && py main.py
	else
  	python3 -m venv venv
  	source venv && pip install -r requirements.txt && python setup.py && python main.py
	endif

clean:
	rmdir /s /q __pycache__
	rmdir /s /q venv

run:
	ifeq ($(SHELL), sh.exe)
	venv\Scripts\activate && pip install -r requirements.txt && py main.py
	else
  	source venv && pip install -r requirements.txt && python main.py
	endif

freeze:
	venv\Scripts\activate && pip freeze > requirements.txt