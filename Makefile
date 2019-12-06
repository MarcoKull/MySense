# micropython
MICROPYTHON=micropython

# python
PYTHON=python -B

clean:
	rm mysense/config/*

decode:
	@read -p "Enter measurement string: " m; cd mysense; ${MICROPYTHON} -c "import MySense; print(MySense.decode(\"$${m}\"))"

default_config:
	cd mysense; ${MICROPYTHON} -c "import MySense; MySense.default_config()"

run:
	cd mysense; ${MICROPYTHON} -c "import MySense; MySense.run()"

test:
	cd mysense; ${MICROPYTHON} -c "import MySense; MySense.test()"
