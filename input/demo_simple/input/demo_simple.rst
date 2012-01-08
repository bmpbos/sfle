.. _data.pcl:				../../input/demo_simple/input/data.pcl
.. _metadata.pcl:			../../input/demo_simple/input/metadata.pcl
.. _data.tsv:				../tmp/demo_simple/data.tsv
.. _metadata.tsv:			../tmp/demo_simple/metadata.tsv
.. _merged.tsv:				../tmp/demo_simple/merged.tsv
.. _merged.pcl:				../demo_simple/merged.pcl
.. _report.txt:				../demo_simple/report.txt
.. _demo_simple SConscript:	../../input/demo_simple/SConscript

demo_simple
-----------

This simple example converts two input files into two output files, specifically:

* Input `data.pcl`_ is a tab-delimited text file of gene measurements from several experiments.

* Input `metadata.pcl`_ is a tab-delimited text file of metadata describing each experiment.

* Output `merged.pcl`_ is a tab-delimited text file in which the normalized data
	has been combined with the metadata.

* Output `report.txt`_ is a simple plain-text report describing the merged data file.

It generates four intermediate files in order to do this:

* `data.pcl: <../tmp/demo_simple/data.pcl>`_ a column-normalized copy of the input data.

* `data.tsv`_: a transposed copy of this column-normalized data.

* `metadata.tsv`_: a transposed copy of the input metadata.

* `merged.tsv`_: a transposed join of the data and metadata, using experiment IDs as keys.

.. note::

	This could be done in essentially two steps, normalization plus merge, using the
	column join feature of the :ref:`merge_tables` script.  We instead use the
	:ref:`transpose` script separately for demonstration purposes.

The `demo_simple SConscript`_ file includes all major elements of a `SflE`_ project:
setup blocks defining constant values, inputs, outputs, and scripts, as well as
several demonstration processing modules.

Imports
~~~~~~~

Every `SflE`_ project ``SConscript`` should begin with standard `Python`_ ``imports``,
including ``sfle`` itself, and an `SCons`_ ``Import`` statement:

.. literalinclude:: ../../demo_simple/SConscript
	:start-after:	StartImport
	:end-before:	EndImport

The ``Import( "*" )`` reads in all of the variables set up for the project by the
`SflE`_ infrastructure, including its input, output, and temporary directories and
the variety of default processors provided in the `SflE`_ distribution.

Constants
~~~~~~~~~

Like any standard script or program, a `SflE`_ workflow should define its constants
at the top of ``SConscript``.  These can include configuration values, but as `SflE`_
is mainly a file processing environment, they'll often include filename suffixes
(and sometimes prefixes):

.. literalinclude:: ../../demo_simple/SConscript
	:start-after:	StartConstants
	:end-before:	EndConstants
	
Inputs
~~~~~~

Project-specific input files are assumed to come from the ``fileDirInput`` directory,
defined for each project by the `SflE`_ infrastructure.  They should be of type
``File`` as defined by `SCons`_, and they can easily be looked up from the appropriate
directory using the :py:meth:`sfle.d` convenience function:

.. literalinclude:: ../../demo_simple/SConscript
	:start-after:	StartInFiles
	:end-before:	EndInFiles

Outputs and intermediate files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The distinction between "output" and "intermediate" files is entirely up to individual
projects.  `SflE`_ provides distinct ``fileDirTmp`` and ``fileDirOutput`` directories
that can be used as desired to specify where each file is produced.  A guideline
is that output files are to be inspected upon completion as research products,
whereas intermediate files do not need to be viewed or distributed except for debugging.

The :py:meth:`sfle.rebase` convenience function is useful for renaming a file into a
new directory, optionally with a new file type extension as well.

.. literalinclude:: ../../demo_simple/SConscript
	:start-after:	StartOutFiles
	:end-before:	EndOutFiles

Programs and scripts
~~~~~~~~~~~~~~~~~~~~

All of the utility scripts included with `SflE`_ are available to any project by default,
under the appropriate ``c_fileProg`` variable names.  Any project can include its own
scripts (in any language, although `Python`_ is preferred) in a ``src`` subdirectory
with which to build processing modules.
	
.. literalinclude:: ../../demo_simple/SConscript
	:start-after:	StartPrograms
	:end-before:	EndPrograms

SCons Environment
~~~~~~~~~~~~~~~~~

`SCons` provides a variety of local variables and methods to normal ``SConstruct`` and
``SConscript`` files that `SflE`_ is, as a standard `Python`_ module, not able to access
natively.  Instead, all `SflE`_ methods that interact with `SCons`_ rules must be passed
an `Environment <http://www.scons.org/doc/production/HTML/scons-user/c1385.html>`_
object.  By default this should, unsurprisingly, be the ``DefaultEnvironment``, which we
store for convenience in a local variable.
	
.. literalinclude:: ../../demo_simple/SConscript
	:start-after:	StartEnvironment
	:end-before:	EndEnvironment
	
Module 1: Normalization
~~~~~~~~~~~~~~~~~~~~~~~

The input data is first normalized into an intermediate PCL file using the ``normalize.py``
script and the core `SflE`_ :py:meth:`sfle.pipe` method.  This runs a script with one
input on standard in, stores its output, and reruns if either the input file or
script itself is modified.  For more information, see the documentation for
:py:meth:`sfle.pipe`.

Here, we provide the data PCL as input, pipe it through the normalization script, and
create the normalized PCL as an intermediate output file.

.. literalinclude:: ../../demo_simple/SConscript
	:start-after:	StartNormalize
	:end-before:	EndNormalize

Module 2: Transposition
~~~~~~~~~~~~~~~~~~~~~~~

This module demonstrates automatic filename generation and caching in `SflE`_.  It runs
the same steps for two different files, the input metadata and the newly normalized data
PCLs.  A filename is generated for each by rebasing it into the temporary directory and
changing its extention from PCL to TSV.  The :ref:`transpose` script is used each time
to pipe each input into the new output, and the results of each :py:meth:`sfle.pipe` are
accumulated into a list for subsequent reuse.
	
.. literalinclude:: ../../demo_simple/SConscript
	:start-after:	StartTranspose
	:end-before:	EndTranspose
	
Module 3: Merge
~~~~~~~~~~~~~~~

The module first autogenerates another intermediate filename for a merged, but still
transposed, TSV file containing both metadata and data.  It then combines all of the
previously stored transposed files using :ref:`merge_tables` with the :py:meth:`sfle.cmd`
method, which takes nothing on standard input and sends its output to a new file.
Instead, :py:meth:`sfle.cmd` accepts command line arguments that may be constants
that will never change for `SCons`_ (marked with ``False`` and not present here) or
files that must be monitored for dependency changes (marked with ``True`` here).
For more information, see the documentation for :py:meth:`sfle.cmd`.

Here, we provide the newly generated intermediate TSV files as command line arguments
to the :ref:`merge_tables` script and pipe its output to yet another new intermediate
file.

.. literalinclude:: ../../demo_simple/SConscript
	:start-after:	StartMerge
	:end-before:	EndMerge

Modules 4-5: Reverse transposition and reporting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final two modules are each one line pipes.  The first un-transposes the merged
intermediate TSV file into a final merged PCL output file.  The second runs a new
script, ``report.py``, which summarizes the merged output file's contents into a
simple plain text report.

.. literalinclude:: ../../demo_simple/SConscript
	:start-after:	StartOutput
	:end-before:	EndOutput

It is _critical_ that any files you wish to produce for a project are marked as
``Default``.  Other files will only be created if specifically requested by an
`SCons`_ call.  Only ``Default`` files, and any files they depend on, are expected
outputs of `SflE`_ projects.
