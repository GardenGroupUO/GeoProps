# GeoProps: Obtaining Geometric Properties of Nanoclusters and Other Chemical Systems

[![Citation](https://img.shields.io/badge/Citation-click%20here-green.svg)](https://dx.doi.org/10.1021/acs.jcim.0c01128)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/GeoProps)](https://github.com/GardenGroupUO/GeoProps)
[![Licence](https://img.shields.io/github/license/GardenGroupUO/GeoProps)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/GeoProps)](https://lgtm.com/projects/g/GardenGroupUO/GeoProps/context:python)

Authors: Geoffrey R. Weal, Caitlin A. Casey-Stevens and Dr. Anna L. Garden (University of Otago, Dunedin, New Zealand)

Group page: https://blogs.otago.ac.nz/annagarden/

Page to cite with work from: *XXX*; XXX; 

## What is this Program?

GeoProps is a program designed to provide information about the geometric properties of individual nanoclusters, including the radial distribution function and the number of neighbours surrounding each atom within the nanocluster. This program utilises modules from the Atomic Simulation Environment (ASE) and As Soon As Possible (ASAP3) packages. 

## Installation

To install this program on your computer, pop open your terminal, ``cd`` to where you want to place this program on your computer, and clone the program to your computer by typing the following into your terminal:

```
git clone https://github.com/GardenGroupUO/GeoProps
```

If you do not have ``git`` installed on your computer, see https://www.atlassian.com/git/tutorials/install-git

Once you have done this, type ``pwd`` into the terminal and copy this path into your ``~\.bashrc`` in the following format:

```bash
#####################################################################################
# These lines will allow python to locate this program on your computer.
export PATH_TO_GeoProps='/PATH_GIVEN_BY_THE_PWD_COMMAND/GeoProps'
export PYTHONPATH="$PATH_TO_GeoProps":$PYTHONPATH
#####################################################################################
```

This will allow your computer to run this program through your terminal on python3.

## How to Run GeoProps

An example of the script used to run this program is given below, called ``run_GeoProps.py``.

```python
from GeoProps import GeoProps_Program

rdf_max_dist = 15.0
no_of_bins = 500
colours = {'Cu': 'y', 'Pd': 'b', ('Cu','Pd'): 'm'}

r_cut = 2.9

xlim_RDF = (1.8,8.2)
xlim_CN  = None

GeoProps_Program(rdf_max_dist, no_of_bins, colours, r_cut, xlim_RDF=xlim_RDF, xlim_CN=xlim_CN)
```

This program will look through all subdirectories from where you place the ``run_GeoProps.py`` program and create radial distribution function plots and number of neighbour plots for each nanoclusters and chemical systems that is found as either a XYZ file (ending with ``.xyz``) or ASE trajectory file (ending with ``.traj``). Examples of the plots that are created are shown below:

![A example radial distribution function plot of a CuPd nanocluster.](https://github.com/GardenGroupUO/GeoProps/blob/main/Images/cu3pd35_RDF.png?raw=true)

![A bar plot of the number of neighbour for each atom within a CuPd nanocluster.](https://github.com/GardenGroupUO/GeoProps/blob/main/Images/cu3pd35_No_of_Neighbours.png?raw=true)

## About

<div align="center">

| Python        | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/GeoProps)](https://docs.python.org/3/) | 
|:-------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Repositories  | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/GeoProps)](https://github.com/GardenGroupUO/GeoProps) |
| Documentation | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/GeoProps)](https://github.com/GardenGroupUO/GeoProps) | 
| Citation      | [![Citation](https://img.shields.io/badge/Citation-click%20here-green.svg)](https://dx.doi.org/10.1021/acs.jcim.0c01128) | 
| Tests         | [![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/GeoProps)](https://lgtm.com/projects/g/GardenGroupUO/GeoProps/context:python)
| License       | [![Licence](https://img.shields.io/github/license/GardenGroupUO/GeoProps)](https://www.gnu.org/licenses/agpl-3.0.en.html) |
| Authors       | Geoffrey R. Weal, Caitlin A. Casey-Stevens, and Dr. Anna L. Garden |
| Group Website | https://blogs.otago.ac.nz/annagarden/ |

</div>
