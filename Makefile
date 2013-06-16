TOP := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

test:
	@nosetests -v

run-test:
	@PYRANGE_CONFIG=$(TOP)/tests/config.py $(TOP)/range-server.py

run:
	@$(TOP)/range-server.py
