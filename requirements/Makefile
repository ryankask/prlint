objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

all: $(outputs)

%.txt: %.in
	pip-compile -v --output-file $@ $<

test.txt: base.txt
