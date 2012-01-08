.. include:: global.rst

.. toctree::
	:hidden:

	global

====
SflE
====

`SflE`_ (pronounced "`souffle <http://en.wikipedia.org/wiki/Souffle>`_") is a
Scientific workFLow Environment built around the `SCons`_ build system.
`SflE`_'s goal is to rapidly, reliably, and reproducibly turn input data into
analysis products.  It allows researchers to combine `Python`_ scripts or
other data processing programs with `Sphinx`_ `reStructuredText`_ documentation,
much like `Sweave`_ combines `R`_ scripts with `LaTeX`_ documentation.  `SflE`_
can include `R`_ scripts, command line programs, or any combination of
steps needed to produce calculations, text, or publication-ready figures from
input data.  It can automatically download files from remote servers, parallelize
and document analysis steps, minimize recalculations on an as-needed basis,
and ensure you get the correct results quickly, every time.

`SflE`_ workflows are packaged as "projects," and the quickest way to get
started is to look at some of the example analyses provided with `SflE`_ itself.
Feel free to :doc:`dive in <demos>`, or read on below for an overview of
:ref:`getting started <getting_started>` and `SflE`_'s workflow philosophy.

Contents
========

* :ref:`download`
* :ref:`getting_started`
* :ref:`philosophy`

.. toctree::
	:maxdepth: 2
	
	demos
	utilities
	sfle
..	about

* :ref:`history`

.. _download:

Downloading and installing SflE
===============================

.. warning::

	`SflE`_ is currently under development; these instructions will change
	in the future.

Choose one of the following methods to obtain `SflE`_:

* `Mercurial`_ install (strongly recommended)::

	hg clone ssh://hg@bitbucket.org/chuttenh/sfle

* `SflE install <https://bitbucket.org/chuttenh/sfle/get/default.tar.gz>`_::

	tar -xzf chuttenh-sfle-###.tar.gz
	mv chuttenh-sfle-### sfle

`SflE`_ is compatible with Linux and Mac OS, and runs with some issues
on Windows using `Cygwin`_.  After ensuring that you have the following
`Prerequisites`_ installed, you can tell `SflE`_ to execute all of
its default workflows with a single :command:`scons` command::

	cd sfle
	export PYTHONPATH=`pwd`/src
	scons

Prerequisites
-------------

`SflE`_ has several required prerequisites that must be installed and executable
in order for it to run.  We also suggest several optional prerequisites that will
make your analyses more pleasant.

* `Python`_ >= 2.7
* `SCons`_ >= 2.1
* `Sphinx`_ >= 1.1.2

Recommended
~~~~~~~~~~~

* `R`_
* `Matplotlib`_ >= 1.1.0

.. _getting_started:

Getting started
===============

For a quick start, from the `SflE`_ directory, just type::

	scons

That's it!  `SflE`_ automatically performs the following steps:

#. Set up a default environment including convenience scripts and `Sphinx`_ utilities.
#. Look for each project subdirectory in ``input``, containing a file tree::

	input                   # Main sfle input directory
	  project1              # First project
	    SConscript          # Workflow rules for project1
	    input               # Input files specific to project1
	      data.pcl
	      metadata.pcl
	      ...
	    src                 # Scripts specifi to project1
	      script.py
	      script.R
	      ...
	  project2              # Second project
	    ...

#. Run each project's ``SConscript`` rules, generating intermediate and final output files::

	output                  # Main sfle output directory
	  tmp                   # Main sfle intermediate file directory
	    project1            # Intermediate files specific to project1
	      intermediate1.txt
	      intermediate2.txt
	      ...
	    project2            # Intermediate files specific to project2
	      ...
	  project1              # Output files specific to project1
	    output1.txt
	    output2.txt
	    ...
	  project2              # Output files specific to project2
	    ...

Dependency-based workflows
--------------------------

`SflE`_ manages :dfn:`projects`, each of which represents a workflow for transforming
inputs (typically data files) into outputs (typically calculation results, figures,
documents, or reports).  Each :dfn:`workflow` is a list of one or more :dfn:`modules`,
and each module performs exactly one processing step.  For example, a workflow might
consist of the following steps:

#. Normalize an input data file
#. Combine the normalized file with a metadata file
#. Generate a report on the combined file

Each step represents one or a few modules, and each module runs exactly one :dfn:`command`
to generate a new output.  Normalizing an input file creates one new, normalized output
file.  Combining two files might require creating two intermediate files and then joining
them into another new output file.

.. note::

	Projects are typically each stored in their own separate `Mercurial`_
	repository.  The `SflE`_ package includes several demonstration projects,
	but these are atypical.  You should generally ``hg init`` your own new
	projects and then ``hg push`` them to an appropriate location such as
	`Bitbucket`_.

`SflE`_ defines commands within modules, and assembles modules into workflows, using
the `SCons`_ build system.  `SCons`_, like `make`_, is a dependency-based "language" in
which rules are **descriptive**, not **imperative**.  That is, in order to perform a
series of steps::

	Call program1 to convert infile1 to tmpfile1
	Call program2 to combine infile2 and tmpfile1 into tmpfile2
	Call program3 to convert tmpfile2 into outfile1

you should instead describe what inputs and outputs each step requires::

	tmpfile1 requires calling program1 to convert infile1
	tmpfile2 requires calling program2 to combine infile2 and tmpfile1
	tmpfile3 requires calling program3 to convert tmpfile2

This distinction is subtle, but notice that in the second form, you've only defined rules;
you've not executed any of them yet!  Nothing will happen until you execute the key step::

	Create tmpfile3

If you're not familiar with software build systems like `SCons`_ or `make`_ and this
doesn't make sense to you, we recommend the following background reading:

* Sections 1-4 of the `GNU make manual <http://www.gnu.org/software/make/manual/make.html>`_
* The `SCons tutorial <http://www.scons.org/wiki/SconsTutorial1>`_
* Sections 2-3, 6, and 17-18 of the `SCons manual <http://www.scons.org/doc/HTML/scons-user.html>`_

.. _philosophy:

SflE's design philosophy
========================

.. _history:

Updates and version history
===========================

* ``v0.1, 01-01-12``

Initial release, with partial functionality and documentation.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
