# SflE #

----

  * Download the SflE software ( [sfle.tar.gz](https://bitbucket.org/biobakery/sfle/get/tip.tar.gz) ) then follow the [steps to install and run](#markdown-header-getting-started-with-sfle).

  * Please direct questions to the [SflE google group](https://groups.google.com/forum/#!forum/sfle-users) (subscribe to receive SflE news).

  * If you use this environment, the included scripts, or any related code in your work, please let us know.

----

SflE (pronounced "souffle") is a Scientific workFLow Environment built around the [SCons](http://www.scons.org/) build system. SflE's goal is to rapidly, reliably, and reproducibly turn input data into analysis products. It allows researchers to combine [Python](https://www.python.org/) scripts or other data processing programs with [Sphinx reStructuredText](http://sphinx-doc.org/rest.html) documentation, much like [Sweave](https://www.statistik.lmu.de/~leisch/Sweave/) combines [R](https://www.r-project.org) scripts with [LaTeX](https://www.latex-project.org/) documentation. SflE can include R scripts, command line programs, or any combination of steps needed to produce calculations, text, or publication-ready figures from input data. It can automatically download files from remote servers, parallelize and document analysis steps, minimize recalculations on an as-needed basis, and ensure you get the correct results quickly, every time.
SflE workflows are packaged as "projects," and the quickest way to get started is to look at some of the example analyses provided with SflE itself. 


## Getting started with SflE ##

### Prerequisites ###

SflE has several required prerequisites that must be installed and executable in order for it to run. We also suggest several optional prerequisites that will make your analyses more pleasant.

#### Required ####

1. [Python](https://www.python.org/) (version >= 2.7) 
2. [SCons](http://www.scons.org/) (version >= 2.1)
3. [Sphinx](http://sphinx-doc.org) (version >= 1.1.2)
4. Operating system (Linux or Mac)

#### Recommended ####

1. [R](https://www.r-project.org)
2. [Matplotlib](http://matplotlib.org/) (version >= 1.1.0)

### Installation ###

1. Download and unpack the SflE software
    * Download the software: [sfle.tar.gz](https://bitbucket.org/biobakery/sfle/get/tip.tar.gz)
    * `` $ tar xzvf sfle.tar.gz ``
    * `` $ cd sfle ``
2. Add the SflE software to your PYTHONPATH
    * `` $ export PYTHONPATH=$PYTHONPATH:`pwd`/src ``
3. (Optional) Run SflE on all of its default workflows to test the install
    * `` $ scons ``

### How to run ###

For a quick start, from the SflE directory, just type:
    $ scons

That's it! SflE automatically performs the following steps:

1. Set up a default environment including convenience scripts and Sphinx utilities.
2. Look for each project subdirectory in input, containing a file tree:

```
input                   # Main sfle input directory
  project1              # First project
    SConscript          # Workflow rules for project1
    input               # Input files specific to project1
      data.pcl
      metadata.pcl
      ...
    src                 # Scripts specific to project1
      script.py
      script.R
      ...
  project2              # Second project
    ...
Run each project's SConscript rules, generating intermediate and final output files:

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
```

## Dependency-based workflows ##
SflE manages projects, each of which represents a workflow for transforming inputs (typically data files) into outputs (typically calculation results, figures, documents, or reports). Each workflow is a list of one or more modules, and each module performs exactly one processing step. 

For example, a workflow might consist of the following steps:

1. Normalize an input data file
2. Combine the normalized file with a metadata file
3. Generate a report on the combined file

Each step represents one or a few modules, and each module runs exactly one command to generate a new output. Normalizing an input file creates one new, normalized output file. Combining two files might require creating two intermediate files and then joining them into another new output file.

Please note, projects are typically each stored in their own separate Mercurial repository. The SflE package includes several demonstration projects, but these are atypical. You should generally hg init your own new projects and then hg push them to their own remote repositories possibly hosted by a site like [Bitbucket](https://bitbucket.org).

SflE defines commands within modules, and assembles modules into workflows, using the [SCons](http://www.scons.org/) build system. [SCons](http://www.scons.org/), like [make](http://www.gnu.org/software/make/manual/make.html), is a dependency-based "language" in which rules are descriptive, not imperative. 

That is, in order to perform a series of steps:

1. Call program1 to convert infile1 to tmpfile1
2. Call program2 to combine infile2 and tmpfile1 into tmpfile2
3. Call program3 to convert tmpfile2 into outfile1

You should instead describe what inputs and outputs each step requires:

 * tmpfile1 requires calling program1 to convert infile1
 * tmpfile2 requires calling program2 to combine infile2 and tmpfile1
 * tmpfile3 requires calling program3 to convert tmpfile2

This distinction is subtle, but notice that in the second form, you've only defined rules; you've not executed any of them yet! Nothing will happen until you execute the key step, create tmpfile3.

If you're not familiar with software build systems like SCons or make, we recommend the following background reading:

1. Sections 1-4 of the [GNU make manual](http://www.gnu.org/software/make/manual/make.html)
2. [The SCons tutorial](https://bitbucket.org/scons/scons/wiki/SconsTutorial1)
3. Sections 2-3, 6-7, and 18 of the [SCons user guide](http://www.scons.org/doc/HTML/scons-user/)