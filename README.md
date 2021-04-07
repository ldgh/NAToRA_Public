# NAToRA
# NAToRA toolkit

NAToRA toolkit consists of a series of scripts to execute kinship control analyses as described by Kehdy et al. 2015.

## Requirements

NAToRA toolkit was implemented using two programming languages:

* Perl
* Python

Besides having both of the languages installed, it is necessary to install python’s library NetworkX as well. An installation guide is present in [NetworkX] website.(https://networkx.github.io/documentation/stable/install.html)

## Brief Introduction to the scripts


In this section we are going to present all the scripts and provide execution examples. We are going to utilize the file Teste0.txt in the examples. 

### Natora2.py and individuo.py:

These are the main scripts in the kinship control analyses execution. In order to allow the utilization of any kinship analysis software (PLINK, REAP, Matriz G, etc), we utilize a 3 column input:

```
IND1	IND2	Coefficient
```

In the toolkit, we provide two scripts to convert PLINK and REAP files to this column format (PLINK2NAToRA.pl and REAP2NAToRA.pl, respectively). 
The parameters are described below:

#### Parameters

```
	     --input or -i		Input file					
	     --cutValue or -c		Minimum value to be considered kinship	(α value)
	     	--valueMin or -v	Minimum tiebreaker value			
	     	--valueMax or -V	Maximum tiebreaker value			
	     --folder or -l		Output folder 	
	     --elimination or -e	Elimination method (default=1)	
						1: Centrality Degree				
						2: Betweenness Degree            		
						3: Closeness Degree              		
	     --maxValuePossible or -m	When the elimination method used is 2 or 3, a normalization must be done: 					
					valorMaximoDaMatrica - Link value			
	     --help or -h		show this message		
```

Execution example

```
python Natora.py -i teste.txt -c 0.1 -v 0.01 -V 0.2 -l ./ -e 1
```

#### Known issues

There are function incompatibilities between the different NetworkX versions, and that can lead to errors. If the library used is NetworkX 2.0, we recommend the utilization of Natora_Public.py, because NetworkX’s update modified some functions. In this version we maintain only Node Degree centrality based on heuristic exclusion and the optimum algorithm. For old versions of NetworkX we recomend the use of NAToRA_Old.py


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
perl PLINK2NAToRA.pl -i <output REAP> -o <file name>
```

### criaGML.pl:

This script was made to convert data in PLINK, REAP or NAToRA format to GML (compatible with most complex network softwares and libraries). In simpler plots, we recommend the utilization of the software yED.

#### Parâmetros
```
	-corte					cut value	(α value)			
	-lista					List containing excluded individuals			
	-input					File containing the kinship matrix			
	-output					GML output file name			
	-plink					SSignals that it’s a PLINK’s file		
	-reap					Signals that it’s a REAP’s file		
	-default				Signals that it’s NAToRA’s model file		
	-split					splits ID by _ in order to decrease the label	
	-h					Shows this message	
```

Execution example:

```
perl criaGML.pl -i teste.txt -c 0.1 -o teste.gml -default
```

Given these parameters, the software will open the file teste.txt and insert only links in which the edge value (or kinship value) are bigger than 0.1 (parameter -c). The cut value was implemented because it enables plotting with different kinship degrees. 

The parameter -lista is used to remove some individual(s) of the plot without modifying the source file.
