# micropython
PYTHON=micropython

clean:
	rm mysense/config/*

config:
	cd mysense; ${PYTHON} -c "import MySense; MySense.config()"

default_config:
	cd mysense; ${PYTHON} -c "import MySense; MySense.default_config()"

run:
	cd mysense; ${PYTHON} -c "import MySense; MySense.run()"

test:
	cd mysense; ${PYTHON} -c "import MySense; MySense.test()"
