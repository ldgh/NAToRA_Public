# NAToRA
# NAToRA toolkit

NAToRA toolkit consists of a series of scripts to execute kinship control analyses as described in the manuscript by Leal et al. 2022 (https://doi.org/10.1016/j.csbj.2022.04.009), entitled "NAToRA, a relatedness-pruning method to minimize the loss of dataset size in genetic and omics analyses"

## Requirements

NAToRA toolkit was implemented using two programming languages:

* Perl
* Python3
* NetworkX 2.5

Besides having both of the languages installed, it is necessary to install python’s library NetworkX as well. An installation guide is present in [NetworkX] website.(https://networkx.github.io/documentation/stable/install.html)

## Brief Introduction to the scripts


In this section we are going to present all the scripts and provide execution examples. We are going to utilize the file Datasets/Test.txt in the examples. 

### NAToRA_Public.py

These are the main scripts in the kinship control analyses execution. In order to allow the utilization of any kinship analysis software (PLINK, REAP, Matriz G, etc), we utilize a 3 column input:

```
IND1	IND2	Coefficient
```

In the toolkit, we provide three scripts to convert PLINK, KING and REAP files to this column format (PLINK2NAToRA.pl, KING2NAToRA.pl and REAP2NAToRA.pl, respectively). 
The parameters are described below:

#### Parameters

```
usage: NAToRA_Public.py [-h] -i INPUT -o OUTPUT [-c CUTOFF] [-v VALUEMIN] [-V VALUEMAX] [-e ELIMINATION] [-t] [-m MAX] [-k] [-d DEGREE]

NAToRA: Network Algorithm To Relatedness Analysis

optional arguments:
  -h, --help            show this help message and exit

Required arguments:
  -i INPUT, --input INPUT
                        Input file in NAToRA format (indx indy kinship)
  -o OUTPUT, --output OUTPUT
                        Output file. NAToRA will creates two files: <output>_familyList.txt and <output>_toRemove.txt

Optional arguments:
  -c CUTOFF, --cutoff CUTOFF
                        Cutoff value that defines the minimum value for two individuals to be considered related (optional if --kinship)
  -v VALUEMIN, --valueMin VALUEMIN
                        Minimum value in tiebreaker (default = 0)
  -V VALUEMAX, --valueMax VALUEMAX
                        Maximum value in tiebreaker (default = highest kinship value of the input)
  -e ELIMINATION, --elimination ELIMINATION
                        Elimination method (default= NAToRA choose based on network).1- Heuristic based on node centrality degree 2- Optimal algorithm (based on clique)
  -t, --test            Estimation of how many samples will be lost. The algorithm requires the --max
  -m MAX, --max MAX     Maximum possible value of metric
  -k, --kinship         Signals that the file uses kinship coefficient.This allows to NAToRA use the flag --degree to set --cutoff, --valueMin and --valueMax based on kinship degree or
                        make --test showing the regions of each degree
  -d DEGREE, --degree DEGREE
                        Flag used with --kinship to set automatically the --cutoff based on kinship coefficient.0 = Self degree (-c 0.3535) 1 = First degree (-c 0.1768) 2 = Second degree
                        (-c 0.0884) 3 = Third degree (-c 0.0442) 4 = Fourth degree (-c 0.0221)
  -s, --sets            Create independent sets

```

Execution example

```
python NAToRA_Public.py --input Datasets/Test.txt -o Out -c 0.08 
```

### REAP2NAToRA.pl:

This script was conceived in order to convert REAP output into NAToRA’s model.

#### Parameters
```
	    --input ou -i		REAP output file
	    --output ou -o		File name in NAToRA’s format
```

Execution example:

```
perl REAP2NAToRA.pl -i <output REAP> -o <file name>
```

### PLINK2NAToRA.pl:

This script was conceived in order to convert PLINK output (--genome) into NAToRA’s model.

#### Parameters
```
	     --input ou -i		PLINK output file
	     --output ou -o		File name in NAToRA’s format
```

Execution example:

```
perl PLINK2NAToRA.pl -i <output PLINK> -o <file name>
```
### KING2NAToRA.pl:

This script was conceived in order to convert KiING .kin0 into NAToRA’s model.

#### Parameters
```
	     --input ou -i		Input file from KING (.kin file)
	     --output ou -o		File name in NAToRA’s format
```

Execution example:

```
perl KING2NAToRA.pl -i <output KING> -o <file name>
```

### createGML.pl:

This script was made to convert data in PLINK, REAP or NAToRA format to GML (compatible with most complex network softwares and libraries). In simpler plots, we recommend the utilization of the software yED.

#### Parâmetros
```
	-corte					cut value	(α value)			
	-lista					List containing excluded individuals			
	-input					File containing the kinship matrix			
	-output					GML output file name			
	-plink					Signals that it’s a PLINK’s file		
	-reap					Signals that it’s a REAP’s file		
	-default				Signals that it’s NAToRA’s model file		
	-split					splits ID by _ in order to decrease the label	
	-h					Shows this message	
```

Execution example:

```
perl createGML.pl --input Datasets/Test.txt -c 0.1 -out Test.gml --default
```

Given these parameters, the software will open the file teste.txt and insert only links in which the edge value (or kinship value) are bigger than 0.1 (parameter -c). The cut value was implemented because it enables plotting with different kinship degrees. 

The parameter -lista is used to remove some individual(s) of the plot without modifying the source file.

## NAToRA heuristic running

We made this gif using the biggest family in Bambuí dataset data with relationship inferred by PLINK (Datasets/PLINK/BAMBUI_PLINK_IDChanged.genome.gz). In this representation, we show in red the edges that will be removed after the exclusion of the individual with highest node degree centrality

![Bambui Removal](./Figures/Bambui.gif?style=centerme)
