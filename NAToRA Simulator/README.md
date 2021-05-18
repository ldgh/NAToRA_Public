# NAToRASimulator

This simulator aims to create genealogy with reproductive behavior similar to expected in human populations based on parameters provided by the user, allowing to create several different scenarios. In our model, we defined that full siblings can not have children and it is only possible to have offspring between individuals of the same generation. After generating the genealogy, the algorithm calculates the theoretical kinship coefficient among all pairs of related individuals.


The input file is:
```
# of men \t # of women \t Proportion of unrelated \t Proportion of half-siblings
```

An exemple of command line:
```
main.py --input inputData --output relationships.txt
```
