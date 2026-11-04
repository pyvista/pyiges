.PHONY: help Makefile

test: .PHONY
	pytest -vx

docs: .PHONY
	make -C docs html

deploy_docs: .PHONY
	make -C docs html deploy

build: test
	rm -f dist/*
	flit build

upload: build
	twine upload dist/* --skip-existing
