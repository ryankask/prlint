objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)
PIP_TOOLS_INSTALLED: ; @which pip-compile > /dev/null

all: $(outputs)

%.txt: %.in
	pip-compile -v --output-file $@ $<

test.txt: base.txt

check: PIP_TOOLS_INSTALLED

clean: check
	- rm *.txt
