#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 13:54:58 2020

@author: thiago
"""

import sys
import argparse
import networkx as nx
import numpy as np

def makeTests(inputFile, maxValue, outputName, kinship):
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np 
    import math as mt

    print("We will perform the tests. The minimum cutoff will be 0.01 and the maximum will be "+str(maxValue))
    cutoffs=[]
    estimations=[]
    estimationsO=[]
    estimationsH=[]

    points=50
    
    
    for cutoff in np.arange(0.01, maxValue, maxValue/points):
        #print(f"\t Calculating to cutoff {cutoff:.2f}")
        N, Nc = createNetworks(inputFile, cutoff, 0, maxValue)
        if(supportsClique(Nc)):
            toRemove=optimalElimination(Nc)
            estimationsO.append(len(toRemove))
            estimationsH.append(None)
        else:
            toRemove=heuristicElimination(Nc, N)
            estimationsH.append(len(toRemove))
            estimationsO.append(None)
            
        estimations.append(len(toRemove))
        cutoffs.append(cutoff)
        
    numberOfNodes=N.number_of_nodes()
    
    df=pd.DataFrame(dict(x=cutoffs, y=estimationsH,  label="Heuristic"))
    df2=pd.DataFrame(dict(x=cutoffs, z=estimationsO, label="Optimal"))
    groups = df.groupby('label')
    groups2= df2.groupby('label')
    
    fig, ax = plt.subplots()
    if(kinship):
        selfDegree=(mt.sqrt(0.5*0.25), 0.5)
        firstDegree=(mt.sqrt(0.125*0.25), mt.sqrt(0.5*0.25))
        secondDegree=(mt.sqrt(0.0625*0.125),mt.sqrt(0.25*0.125))
        thirdDegree=(mt.sqrt(0.03125*0.0625),mt.sqrt(0.125*0.0625))
        fourthDegree=(mt.sqrt(0.015625*0.03125),mt.sqrt(0.0625*0.03125))
        
        print("\n\n")
        print("\tValues by degree\t\tMin\t\t\tTheoretical\t\tMax")
        print("\tSelf degree interval:\t",selfDegree[0],"\t\t0.5\t\t",selfDegree[1])
        print("\tFirst degree interval:\t",firstDegree[0],"\t\t0.25\t\t",firstDegree[1])
        print("\tSecond degree interval:\t",secondDegree[0],"\t\t0.125\t\t",secondDegree[1])
        print("\tThird degree interval:\t",thirdDegree[0],"\t\t0.0625\t\t",thirdDegree[1])
        print("\tFourth degree interval:\t",fourthDegree[0],"\t\t0.03125\t\t",fourthDegree[1])
        print("\n\n")
        
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', label="Heuristic", color="green")

    for name, group in groups2:    
            ax.plot(group.x, group.z, marker='P', linestyle='', label="Optimal", color="green")

    plt.xticks(np.arange(0.01, maxValue, maxValue/(points/2)), rotation=45)
    plt.yticks(np.arange(0, int(max(estimations)+max(estimations)/10), int(max(estimations)/20)))
    
    title="Number of individuals to be removed by cutoff value (N="+str(numberOfNodes)+")"
    plt.title(title)
    legend_without_duplicate_labels(ax)
    

    plt.ylabel('Number of individuals to be eliminated')
    plt.xlabel('Cutoff value')
    #plt.grid(True)
    plt.tight_layout()
    plt.savefig(outputName+".png")
    print ('The '+outputName+'.png was generated')
    sys.exit()
    
def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique),loc='upper center', ncol=1, fancybox=True, shadow=True)

def chooseElimination(Nc, N):
    if(supportsClique(Nc)):
        print("Our algorithm will run the optimal algorithm.\nIf you think it is taking too long we ask you to cancel the execution and run with the flag --elimination 1")
        toRemove=optimalElimination(Nc)
    else:
        print("Our algorithm will run the heuristic algorithm.")
        toRemove=heuristicElimination(Nc, N)
    return toRemove
def finish():
    print("Please, re-run with the flag -h to see the help")
    exit()

def getchar():
    print("Aperte ENTER")
    sys.stdin.read(1)

def outputToRemove(toRemove, output):
    print("\n\n")
    print("Saving the list in "+str(output)+"_toRemove.txt")
    file=open(output+"_toRemove.txt","w")
    
    for item in toRemove:
        file.write(str(item)+"\n")
    file.close()

def tiebreaker(listOfNodes, network):
    
    sumToRemove=-np.inf
    for node in listOfNodes:
        edges=network.edges(node)
        sumCandidate=0
        for node1,node2 in edges:
            sumCandidate=network[node1][node2]["weight"]+sumCandidate
        #print("The node "+str(node)+" has the sum "+str(sumCandidate))
                    
        if(sumCandidate>sumToRemove):
            toRemove=node
            sumToRemove=sumCandidate
    return toRemove
    

def familyDetection(network, output):
    connectedComponent=nx.connected_component_subgraphs(network)
    
    count=1
    
    file=open(output+"_familyList.txt","w")
    
    for component in connectedComponent:
        for node in component.node():
            file.write(str(node)+"\t"+str(count)+"\n")
        count=count+1
    file.close()

def optimalElimination(Nc):
    connectedComponent=nx.connected_component_subgraphs(Nc)
    
    toRemove=[]
    for component in connectedComponent:
        complementNetwork=nx.complement(component)
        cliqueMax=nx.find_cliques(complementNetwork)
        cliqueWanted=[]
        for clique in cliqueMax:
            if(len(clique) > len (cliqueWanted)):
                cliqueWanted=clique
                    
        for node in component.nodes():
            if(node not in cliqueWanted):
                toRemove.append(node)
    return toRemove


def supportsClique(G):
    largest_cc = max(nx.connected_components(G), key=len)
    sub=G.subgraph(largest_cc)
    if(len(largest_cc) <= 100):
        if(len(largest_cc) <= 50):
            return True
        else:
            if(nx.density(sub) > 0.5):
                return True
            else:
                return False
    else:
        if(nx.density(sub) > 0.8):
            return True
        else:
            return False
    
    

def heuristicElimination(Nc, N):
    removedIndividuals=[]
    
    centralityN=nx.degree_centrality(N)
    
    connectedComponent=nx.connected_component_subgraphs(Nc)
    for component in connectedComponent:
        runStep1=True
        while runStep1:
            centralityNc=nx.degree_centrality(component)
            #If the component is empty
            if not centralityNc.values():
                runStep1=False
                break
            
            #Get the biggest centrality and all nodes with the same centrality
            biggestCentrality=max(centralityNc.values())
            listOfNodes=[k for k,v in centralityNc.items() if v == biggestCentrality]
            
            
            #Two conditions: 1) Have individuals to remove and 2) The individuals has more than 1 neighbor
            runStep1=False
            if(len(listOfNodes) < 1):
                runStep1=False
            
            #Check if there's at least one candidate with more than 1 neighbor            
            for node in listOfNodes:
                if(component.degree(node) > 1):
                    runStep1=True            
            
            
            if runStep1:
                #If exist, lets remove
                toRemove=listOfNodes[0]
                if(len(listOfNodes) > 1):
                    toRemove=tiebreaker(listOfNodes, component) 
                
                component.remove_node(toRemove)
                removedIndividuals.append(toRemove)
        
        remainingNodes=component.nodes()
        
        alreadyRemoved=[]
                
        for node in remainingNodes:
            if component.degree(node) > 0:
                if node not in alreadyRemoved:
                    neighborhood=component.neighbors(node)
                    for neighbor in neighborhood:
                        if centralityN[node] > centralityN[neighbor]:
                           toRemove=node
                        elif centralityN[node] < centralityN[neighbor]:
                           toRemove=neighbor
                        else:
                           toRemove=tiebreaker([node,neighbor], N)
                    alreadyRemoved.append(node)
                    alreadyRemoved.append(neighbor)
                    
                    removedIndividuals.append(toRemove)
            
    #print(len(removedIndividuals))
    return removedIndividuals
 

def createNetworks(inputFile, cutoff, valueMin, valueMax):
    file=open(inputFile,"r")
    
    N=nx.Graph()
    Nc=nx.Graph()
    #added=[]
    for line in file:
        splited=line.split()
        value=float(splited[2])
        
        Nc.add_node(splited[0])
        Nc.add_node(splited[1])
            
        if value >= cutoff:
            Nc.add_edge(splited[0],splited[1],weight=value)
        if value>= valueMin and value<=valueMax:
            N.add_edge(splited[0],splited[1],weight=value)
    
    return N, Nc
    
def getMax(inputFile):
    file=open(inputFile,"r")
    maxValue=-np.inf
    for line in file:
        splited=line.split()
        value=float(splited[2])
        if maxValue < value:
            maxValue=value
    
    return maxValue
    

def cutoffBasedOnDegree(degree):
    if(degree == None):
        print('The elimination method with --kinship requires --degree')
        finish()
    if(degree == 0):
        cutValue=0.3535
        valueMin=0.0221
        valueMax=0.3535
    elif(degree == 1):
        cutValue=0.1768
        valueMin=0.0221
        valueMax=0.1768
    elif(degree == 2):
        cutValue=0.0884
        valueMin=0.0221
        valueMax=0.0884
    elif(degree == 3):
        cutValue=0.0442
        valueMin=0.0221
        valueMax=0.0442
    elif(degree == 4):
        cutValue=0.0221
        valueMin=0.0221
        valueMax=0.5
    else:
        print('The degree provided('+str(degree)+') is not accepted')
        finish()

    return(cutValue, valueMin, valueMax)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NAToRA: Network Algorithm To Relatedness Analysis')
    
    
    required= parser.add_argument_group("Required arguments")
    required.add_argument('-i','--input', help='Input file in NAToRA format (indx indy kinship)', required=True)
    required.add_argument('-o', '--output', help='Output file. NAToRA will creates two files: <output>_familyList.txt and <output>_toRemove.txt', required=True)

    optional= parser.add_argument_group("Optional arguments")
    optional.add_argument('-c','--cutoff', help='Cutoff value that defines the minimum value for two individuals to be considered related (optional if --kinship)')
    optional.add_argument('-v', '--valueMin',help='Minimum value in tiebreaker (default = 0)', required=False)
    optional.add_argument('-V', '--valueMax',help='Maximum value in tiebreaker (default = highest kinship value of the input)', required=False)
    optional.add_argument('-e','--elimination', help= 'Elimination method (default= NAToRA choose based on network).1- Heuristic based on node centrality degree 2- Optimal algorithm (based on clique)', required=False)
    optional.add_argument('-t','--test', help='Estimation of how many samples will be lost. The algorithm requires the --max',action="store_true", default=False )
    optional.add_argument('-m', '--max', help='Maximum possible value of metric')
    optional.add_argument('-k', '--kinship', help='Signals that the file uses kinship coefficient.This allows to NAToRA use the flag --degree to set --cutoff, --valueMin and --valueMax based on kinship degree or make --test showing the regions of each degree',action="store_true", default=False )
    optional.add_argument('-d', '--degree', help='Flag used with --kinship to set automatically the --cutoff based on kinship coefficient.0 = Self degree (-c 0.3535) 1 = First degree (-c 0.1768) 2 = Second degree (-c 0.0884) 3 = Third degree (-c 0.0442) 4 = Fourth degree (-c 0.0221) ')

    
    args=parser.parse_args()
    
    inputFile=args.input
    outputFile=args.output

    #Two ways : --test and exclusion
    test=args.test
    kinship=args.kinship
    
    if(test):
    #Test
        if(kinship):
            maxMetricValue=0.5
        else:
            maxMetricValue=float(args.max)
            if(maxMetricValue == None):
                print("The --test requires --max <value> or --kinship")
                finish()
        
                
        makeTests(inputFile,maxMetricValue, outputFile, kinship)
    else:
    #exclusion
        if(kinship):
            degree=args.degree
            cutoffValue, valueMin, valueMax=cutoffBasedOnDegree(degree)
        else:
            if args.cutoff == None:
                print('The elimination requires a cutoff value (--cutoff <cutoff>) or a degree (--kinship -- degree <degree>)')
                finish
            else:
                cutoffValue = float(args.cutoff)
                
            valueMax=args.valueMax
            if(args.valueMax == None):
                print('Getting the --maxValue')
                valueMax=getMax(inputFile)
            else:
                valueMax=float(args.valueMax)
            if(args.valueMin == None):
                valueMin=0.0
            else:
                valueMin=float(args.valueMin)
        
        print('Creating the Networks N and Nc (cutoff='+str(cutoffValue)+', valueMin='+str(valueMin)+', valueMax='+str(valueMax)+')')
        N, Nc = createNetworks(inputFile, cutoffValue, valueMin,valueMax)
        
        familyDetection(Nc, outputFile)
        
        
        elimination=args.elimination
        print("Elimination = "+str(elimination))
        if(elimination==None):
            toRemove=chooseElimination(Nc, N)
        else:
            elimination=int(args.elimination)
            if(elimination==1):
                print("Heuristic elimination")
                toRemove=heuristicElimination(Nc, N)
            elif(elimination==2):
                toRemove=optimalElimination(Nc)
            else:
                print("The elimination choosed does not exist.")
                finish()
            
        outputToRemove(toRemove, outputFile)