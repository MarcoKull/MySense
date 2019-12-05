# micropython
MICROPYTHON=micropython

# python
PYTHON=python -B

clean:
	rm mysense/config/*

config:
	cd myconf; ${PYTHON} -c "import MyConf; MyConf.run()"

default_config:
	cd mysense; ${MICROPYTHON} -c "import MySense; MySense.default_config()"

run:
	cd mysense; ${MICROPYTHON} -c "import MySense; MySense.run()"

test:
	cd mysense; ${MICROPYTHON} -c "import MySense; MySense.test()"
