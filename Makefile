.PHONY: help Makefile

test: .PHONY
	pytest -vx

docs: .PHONY
	make -C docs html

build: test
	rm dist/*
	python setup.py bdist_wheel
	python setup.py sdist

upload: build
	twine upload dist/* --skip-existing
