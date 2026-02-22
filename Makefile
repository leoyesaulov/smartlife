#check_system:
#	echo $(SHELL)

all: makeC

setup:
	python -m venv venv
	source venv/bin/activate && pip install -r requirements.txt && python setup.py && python main.py

clean:
	rm -rf main.out

run:
	source venv && pip install -r requirements.txt && python main.py

makeC:
	@echo 'I am compiling!'
	gcc -std=c23 -Iinclude src/main.c -o main.out

.PHONY: makeC

#
#freeze:
#	venv\Scripts\activate && pip freeze > requirements.txt
