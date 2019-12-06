# micropython
PYTHON=micropython

# python
#PYTHON=python -B

clean:
	rm mysense/config/*

decode:
	@read -p "Enter measurement string: " m; cd mysense; ${PYTHON} -c "import MySense; print(MySense.decode(\"$${m}\"))"

default_config:
	cd mysense; ${PYTHON} -c "import MySense; MySense.default_config()"

run:
	cd mysense; ${PYTHON} -c "import MySense; MySense.run()"

test:
	cd mysense; ${PYTHON} -c "import MySense; MySense.test()"
