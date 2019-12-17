# micropython
PYTHON=micropython

# python
#PYTHON=python -B

# most make targets are just shortcuts to the main mysense commands
define myrun
	cd mysense; ${PYTHON} -c "import MySense; MySense.$(1)()"
endef

all:

clean:
	rm mysense/config/*

decode:
	@read -p "Enter measurement string: " m; cd mysense; ${PYTHON} -c "import MySense; print(MySense.decode(\"$${m}\"))"

default_config:
	$(call myrun,default_config)

run:
	$(call myrun,run)

test:
	$(call myrun,test)
