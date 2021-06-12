# GeoProps: Obtaining Geometric Properties of Nanoclusters and Other Chemical Systems

[![PyPI - Python Version](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://docs.python.org/3/)
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

When you execute this program by running ``python3 run_GeoProps.py`` in the terminal, GeoProps will look through all subdirectories from where you place the ``run_GeoProps.py`` program and create radial distribution function plots, number of neighbour plots, and text files giving information about the number of neighbours and number of bonds within your nanocluster/chemical system for each nanoclusters and chemical systems that is found as either a XYZ file (ending with ``.xyz``) or ASE trajectory file (ending with ``.traj``). 

## What will GeoProps do when you run the ``run_GeoProps.py`` script?

Geoprops will search through all the subdirectories that are contained in the same directory as the ``run_GeoProps.py`` python file and make folders of these subdirectories that contain ``GeoProps`` in the name. It will do this one for folders that contain ``.xyz`` or ``.traj`` files. ``GeoProps`` will then work on these files and give structural and geometric data on those ``.xyz`` and ``.traj`` files. 

## Output files that are created by GeoProps

Examples of the plots that are created are shown below. These include a radial distribution function plot, and number of neighbours bar plot, a text document describing all the number of neighbours found in your cluster with the associated atoms (these can be seen by opening up the xyz file, where the tags describe the index for each atom. These can be coloured by the ASE GUI), and a text document describing all the bonds that are found in your nanocluster/chemical system.

A example radial distribution function plot of a Cu<sub>10</sub>Pd<sub>28</sub> nanocluster: 

<p align="center">
	<img src="https://github.com/GardenGroupUO/GeoProps/blob/main/Images/cu10pd28_RDF.png">
</p>

A bar plot of the number of neighbour for each atom within a Cu<sub>10</sub>Pd<sub>28</sub> nanocluster: 

<p align="center">
	<img src="https://github.com/GardenGroupUO/GeoProps/blob/main/Images/cu10pd28_No_of_Neighbours.png">
</p>

A text document describing the number of neighbour for each atom within a Cu<sub>10</sub>Pd<sub>28</sub> nanocluster: 

```
The following file contains information about the number of neighbours that each atom contains in the cluster, as well as the atom indices of atoms in the cluster with those number of neighbours.

To see each atom in your cluster, open the xyz file of your nanocluster/chemical system, and in View -> Colors, change the colouring of your cluster to "By tag".

The colours represent the index for each atom, which corresponce to the atom indices in this document.

No of neighbours	|	Atom Indices in Cluster/Chemical System
---------------------------------------------------------------
		5			|		2 (Cu), 4 (Cu), 7 (Cu), 16 (Cu), 33 (Cu), 34 (Cu), 35 (Cu), 37 (Cu)
		7			|		0 (Pd), 3 (Pd), 5 (Pd), 6 (Pd), 8 (Pd), 12 (Pd), 14 (Pd), 17 (Pd), 20 (Pd), 21 (Pd), 22 (Pd), 23 (Pd), 25 (Pd), 27 (Pd), 30 (Pd), 32 (Pd)
		8			|		13 (Cu), 36 (Cu)
		9			|		1 (Pd), 9 (Pd), 10 (Pd), 18 (Pd), 19 (Pd), 24 (Pd), 26 (Pd), 28 (Pd)
		14			|		11 (Pd), 15 (Pd), 29 (Pd), 31 (Pd)

This is the same list as above, but without elements given for each atom

No of neighbours	|	Atom Indices in Cluster/Chemical System
---------------------------------------------------------------
		5			|			2, 4, 7, 16, 33, 34, 35, 37
		7			|			0, 3, 5, 6, 8, 12, 14, 17, 20, 21, 22, 23, 25, 27, 30, 32
		8			|			13, 36
		9			|			1, 9, 10, 18, 19, 24, 26, 28
		14			|			11, 15, 29, 31

```

A text document describing the types of bonds that are found within a Cu<sub>10</sub>Pd<sub>28</sub> nanocluster: 

```
This text file contains all the information about the number of bonds in this cluster/chemical system.

Total Number of Bonds = 148

Number of ('Cu', 'Pd') Bonds = 56
Number of ('Pd', 'Pd') Bonds = 92

Bond lengths

('Cu', 'Pd'): [2.1426188343062393, 2.1427583193546424, 2.1432650445862267, 2.143300820985679, 2.1433095103614477, 2.143380473937092, 2.1433839899624885, 2.1434279554194773, 2.143507790605591, 2.1437730945180347, 2.1438763872817526, 2.1439948295534226, 2.144006910513814, 2.1440639238653416, 2.144205373937482, 2.144493576045379, 2.178961208591983, 2.179887442593907, 2.1806525368249456, 2.1810616814402115, 2.181135064498954, 2.1815224144682235, 2.1816343117860595, 2.1816578674672766, 2.182015356466698, 2.1821257243283667, 2.182864657104268, 2.1828785262204318, 2.18302277865161, 2.183386345004728, 2.1834696152952877, 2.184521453798309, 2.217582435677598, 2.218172444316745, 2.2187914425746462, 2.2191048987125654, 2.220141304533914, 2.2205328743133554, 2.221514996477335, 2.22154726929384, 2.358535891394043, 2.3592521580784362, 2.3593498449566153, 2.3602507521567317, 2.3602969850076247, 2.361987794973941, 2.362088885121336, 2.3628606855912677, 2.59450012702186, 2.59548672244819, 2.5957151669869707, 2.5963379770634623, 2.5963452624928935, 2.5966444264082984, 2.5966541916292996, 2.5969446051485834]
('Pd', 'Pd'): [2.53371554658355, 2.534070088067998, 2.5342318599496294, 2.534432572208152, 2.5346591614609326, 2.534747097401316, 2.5347748674838084, 2.534955457000947, 2.5740522808982362, 2.574164244902007, 2.5747521491283845, 2.574943804555506, 2.5752974443694345, 2.5755487995606403, 2.5763093979612304, 2.5763258504937077, 2.585286152404103, 2.5853496319609794, 2.5855440296721075, 2.5863472844610604, 2.587268362421799, 2.588225939568966, 2.5883859393806694, 2.588981455960284, 2.5994533249150997, 2.600159636544112, 2.60068668255829, 2.6012124609572282, 2.654168913395472, 2.65689031132755, 2.6576241356976653, 2.6579748494763265, 2.658025020530186, 2.6595973390046317, 2.659746674540581, 2.660005934961473, 2.660578844208819, 2.6613002992039054, 2.66184445696002, 2.662789933778821, 2.663056027294901, 2.664147560864939, 2.6647311328700805, 2.665685035213337, 2.6752655328698767, 2.6759345230031872, 2.677247048785563, 2.678104132030415, 2.680797897001479, 2.681261423810827, 2.681442991272282, 2.6821099371289026, 2.6821525108011843, 2.6821742304107947, 2.682202318865889, 2.682213923244818, 2.6822737895008983, 2.6823470477962554, 2.68253424712709, 2.6827883619378263, 2.6828303710984174, 2.683032599296767, 2.6831520137342086, 2.6840670632573294, 2.735669657462604, 2.736685619285227, 2.736900711681779, 2.7374891499595178, 2.7377133709569943, 2.738549835325026, 2.7387186235763226, 2.73957905227037, 2.7798282332909934, 2.7833749587071575, 2.7836822303565953, 2.7857944595947397, 2.8408295701934363, 2.842052785220107, 2.843253412723664, 2.8432975618208345, 2.843855460526484, 2.8445754358180295, 2.8447587971949986, 2.8454969731182698, 2.8468719651232313, 2.8474147920619752, 2.8479874357866053, 2.8481862322274885, 2.8487682483616887, 2.849951244492647, 2.8512530194249783, 2.853020129286062]

```

## Other useful programs in GeoProps

In a folder called ``Useful_Subsidiary_Programs`` are some other useful scripts that have been written when developing this program. 

* ``make_pages_of_plots.py``: This script allows you to turn a number of plots into pages that contain 12 plots each on them.

## About

<div align="center">

| Python        | [![PyPI - Python Version](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://docs.python.org/3/) | 
|:-------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Repositories  | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/GeoProps)](https://github.com/GardenGroupUO/GeoProps) |
| Documentation | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/GardenGroupUO/GeoProps)](https://github.com/GardenGroupUO/GeoProps) | 
| Citation      | [![Citation](https://img.shields.io/badge/Citation-click%20here-green.svg)](https://dx.doi.org/10.1021/acs.jcim.0c01128) | 
| Tests         | [![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/GeoProps)](https://lgtm.com/projects/g/GardenGroupUO/GeoProps/context:python)
| License       | [![Licence](https://img.shields.io/github/license/GardenGroupUO/GeoProps)](https://www.gnu.org/licenses/agpl-3.0.en.html) |
| Authors       | Geoffrey R. Weal, Caitlin A. Casey-Stevens, and Dr. Anna L. Garden |
| Group Website | https://blogs.otago.ac.nz/annagarden/ |

</div>
