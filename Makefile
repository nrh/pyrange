TOP := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

test:
	@nosetests -v

run-test:
	@$(TOP)pyrange-server.py -c tests/pyrange-test.conf

run:
	@$(TOP)pyrange-server.py -c etc/pyrange.conf

clean:
	@find . -name "*.pyc" -exec rm {} \;
