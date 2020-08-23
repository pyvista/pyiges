# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

clean:
	rm -rf $(BUILDDIR)/*
	rm -rf examples/
	rm -f errors.txt

deploy:
	rm -rf /tmp/pyiges
	cd /tmp; git clone --single-branch --branch gh-pages https://$(github_pat)@github.com/pyvista/pyiges.git
	rm -rf /tmp/pyiges/*
	cp -r _build/html/* /tmp/pyiges/
	touch /tmp/pyiges/.nojekyll
	cd /tmp/pyiges; git add .
	cd /tmp/pyiges; git commit -am "Manual build"
	cd /tmp/pyiges; git push

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
