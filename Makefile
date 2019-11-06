
# python without creating cache directories (-B)
#PYTHON=python -B

# micropython
PYTHON=micropython

clean:
	rm mysense/config/*

run:
	cd mysense; ${PYTHON} -c "import MySense; MySense.run()"

test:
	cd mysense; ${PYTHON} -c "import MySense; MySense.test()"
