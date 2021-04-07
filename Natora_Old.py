# -*- coding: utf-8 -*-
import getopt, sys
import networkx as nx
import os
import resource
from networkx import *
import time
from individuo import Individuo
from operator import itemgetter
from resource import getrusage as resource_usage, RUSAGE_SELF
from time import time as timestamp

def getchar():
	sys.stdin.read(1)

def main():
	#HUGE GETOPT
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:c:e:l:v:V:m:", ["help","input=","cutValue=","elimination=","folder=", "valueMin=", "valueMax=", "maxValuePossible="])
	except getopt.GetoptError as err:
        # print help information and exit:
		print (str(err)) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	
	#Input files
	inputFile=None
	
	#Elimination
	elimination=1;
	#Using information of kinship value
	cutValue=None
	valueMin=None
	valueMax=None
	maxValuePossible=None
	#Output
	folder=None
	printFiles=False
	
	
	for o, a in opts:
		#Input
		if o in ("-i", "--input"):
			inputFile = a
		elif o in ("-h", "--help"):
			usage()
		
		#Cut value
		elif o in ("-c", "--cutValue"):
			cutValue=float(a)
		elif o in ("-v", "--valueMin"):
			valueMin=float(a)
		elif o in ("-V", "--valueMax"):
			valueMax=float(a)
		elif o in ("-m", "--maxValuePossible"):
			maxValuePossible=float(a)
		#Elimination
		elif o in ("-e", "--elimination"):
			elimination=int(a)
		#Output
		elif o in ("-l", "--folder"):
			folder=a
		else:
			assert False, "unhandled option"

	#Read Input file and storage in dictonaries
	objects=readInputFile(inputFile) 
	
	#Create output folders
	createFolders(folder)
	
	#Create the network and make all process
	network=createTheNetwork(cutValue, objects, folder, valueMax, valueMin, maxValuePossible, elimination)
	
	
	
def createTheNetwork(cutValue, objects, folder, maxValue, minValue, maxValuePossible, elimination):
	#print elimination
	
	if cutValue == None :
		print ('Error: You have to choose a cut value (--cutValue)')
		usage()
		exit()
	
	NetworkN=nx.Graph()
	NetworkNc=nx.Graph()
	
	#Insert the nodes
	for o in objects.keys():
		NetworkN.add_node(o)
		NetworkNc.add_node(o)
		
	#Insert the edges
	for o in objects.keys():
		if(elimination==1):
			adjacence=objects[o].getAdjacenceListWithCutsNormal(cutValue)
		else:
			#Betweenness and Closeness calculate te centraliy based in 
			#minimum distances and we want to exclude the biggest relations.
			if maxValuePossible:
				adjacence=objects[o].getAdjacenceListWithCutsNormalized(cutValue,maxValuePossible)
			else:
				print ('you have to inform the highest possible value to elimination 2 and 3 (--maxValuePossible)')
				usage()
				exit()
				
		for a in adjacence:
			NetworkNc.add_edge(o,a,weight=adjacence[a])
		
		#NetworkN
		if(elimination==1):
			adjacenceWithoutCuts=objects[o].getAdjacenceListWithoutCutsNormal(cutValue, minValue, maxValue)
		else:
			adjacenceWithoutCuts=objects[o].getAdjacenceListWithoutCutsNormalized(cutValue, maxValuePossible, minValue, maxValue)
		
		
		for a in adjacenceWithoutCuts:
			NetworkN.add_edge(o,a,weight=adjacenceWithoutCuts[a])
	
	printFamiliesFile(NetworkNc, folder)
	#print NetworkNc.nodes()
	#print NetworkNc.edges(data=True)
	#Network N and Nc Created. Groups detected.
	
	
	if(elimination==1):
		degreeCentrality(NetworkNc, NetworkN, objects, folder, maxValue, minValue, cutValue)
		
	if(elimination==2):
		betweennessCentrality(NetworkNc, NetworkN, objects, folder, maxValue, minValue, cutValue)
		
	if(elimination==3):
		closenessCentrality(NetworkNc, NetworkN, objects, folder, maxValue, minValue, cutValue)
		
	if(elimination==4):
		clique(NetworkNc, NetworkN, objects, folder, maxValue, minValue, cutValue)

def printFamiliesFile(NetworkNc, folder):
	familyFile = open(folder+'/List.txt', 'w')
	
	contador=1
	connectedComponent=connected_component_subgraphs(NetworkNc)
	for component in connectedComponent:
		familyFile.write("Familia "+str(contador)+":\n")
		for node in component:
			familyFile.write(str(node)+"\n")
		familyFile.write("\n")
		contador=contador+1


def clique (NetworkNc, NetworkN, objects, folder, maxValue, minValue, cutValue):
	#print ('Looking for the maximum clique of Nc')
	fileExclusion = open(folder+'/Clique.txt', 'w')
	
	#print ('')
	connectedComponent=connected_component_subgraphs(NetworkNc)
	
	for component in connectedComponent:
		complementNetwork=complement(component)
		cliqueMax=find_cliques(complementNetwork)
		cliqueWanted=[]
		for clique in cliqueMax:
			##print clique
			if(len(clique) > len (cliqueWanted)):
				cliqueWanted=clique
					
		for node in component.nodes():
			if(node not in cliqueWanted):
				fileExclusion.write(str(node)+'\n')

def closenessCentrality (NetworkNc, NetworkN, objects, folder, maxValue, minValue, cutValue):
	#print 'Closeness Degree'
	fileExclusion = open(folder+'/ClosenessCentrality', 'w')
	position=-1;
	exit =0;
	while exit !=1 :
		biggest=-1
		centrality=nx.closeness_centrality(NetworkNc)
		if not centrality:
			exit=1
		
		for i in centrality:
			if biggest <= centrality[i]:
				if(biggest == centrality[i]):
					if(objects[i].getSumEdges() > objects[position].getSumEdges()):
						if (NetworkNc.degree(i) > 1):
							biggest=centrality[i]
							position=i
							exit=0
				else:	
					if (NetworkNc.degree(i) > 1):
						biggest=centrality[i]
						position=i
						exit=0
					else:
						exit=1
				
		if exit!=1:
			if position > -1:
				fileExclusion.write(position+'\n')
				#UpdateTheSum
				for neighbors in NetworkNc.neighbors(position):
					objects[neighbors].updateSum(position)
				NetworkNc.remove_node(position)
	exit=0
	nodes=NetworkNc.nodes()
	centrality=nx.closeness_centrality(NetworkN)
	for n in nodes:
		neighbors=NetworkNc.neighbors(n)
		#print neighbors
		#print len(neighbors)
		if len(neighbors)>0:
			for i in neighbors:
				if centrality[n] < centrality[i]:
					fileExclusion.write(i+'\n')
				elif centrality[n] > centrality[i]:
					fileExclusion.write(n+'\n')
				#Extreme case: centrality equals
				else:
					sumIndividual1=0.0
					sumIndividual2=0.0
					
					individual1=objects[n].getAdjacenceListWithoutCutsNormal(cutValue, minValue, maxValue);
					individual2=objects[i].getAdjacenceListWithoutCutsNormal(cutValue, minValue, maxValue);
					
					for j in individual1:
						sumIndividual1=sumIndividual1+individual1[j]
					for j in individual2:
						sumIndividual2=sumIndividual2+individual2[j]
					
					if(sumIndividual1 >= sumIndividual2):
						fileExclusion.write(n+'\n')
					else:
						fileExclusion.write(i+'\n')
				NetworkNc.remove_edge(n,i)
	


def betweennessCentrality (NetworkNc, NetworkN, objects, folder, maxValue, minValue, cutValue):
	#print 'Betweenness Degree'
	fileExclusion = open(folder+'/BetweennessCentrality', 'w')
	position=-1;
	exit =0;
	while exit !=1 :
		biggest=-1
		centrality=nx.betweenness_centrality(NetworkNc)
		if not centrality:
			exit=1
		
		for i in centrality:
			if biggest <= centrality[i]:
				if(biggest == centrality[i]):
					if(objects[i].getSumEdges() > objects[position].getSumEdges()):
						if (NetworkNc.degree(i) > 1):
							biggest=centrality[i]
							position=i
							exit=0
				else:	
					if (NetworkNc.degree(i) > 1):
						biggest=centrality[i]
						position=i
						exit=0
					else:
						exit=1
				
		if exit!=1:
			if position > -1:
				fileExclusion.write(position+'\n')
				#UpdateTheSum
				for neighbors in NetworkNc.neighbors(position):
					objects[neighbors].updateSum(position)
				NetworkNc.remove_node(position)
	exit=0
	nodes=NetworkNc.nodes()
	centrality=nx.betweenness_centrality(NetworkN)
	for n in nodes:
		neighbors=NetworkNc.neighbors(n)
		#print neighbors
		#print len(neighbors)
		if len(neighbors)>0:
			for i in neighbors:
				if centrality[n] < centrality[i]:
					fileExclusion.write(i+'\n')
				elif centrality[n] > centrality[i]:
					fileExclusion.write(n+'\n')
				#Extreme case: centrality equals
				else:
					sumIndividual1=0.0
					sumIndividual2=0.0
					
					individual1=objects[n].getAdjacenceListWithoutCutsNormal(cutValue, minValue, maxValue);
					individual2=objects[i].getAdjacenceListWithoutCutsNormal(cutValue, minValue, maxValue);
					
					for j in individual1:
						sumIndividual1=sumIndividual1+individual1[j]
					for j in individual2:
						sumIndividual2=sumIndividual2+individual2[j]
					
					if(sumIndividual1 >= sumIndividual2):
						fileExclusion.write(n+'\n')
					else:
						fileExclusion.write(i+'\n')
				NetworkNc.remove_edge(n,i)
	


def degreeCentrality (NetworkNc, NetworkN, objects, folder, maxValue, minValue, cutValue):
	#print 'Centrality Degree'
	fileExclusion = open(folder+'/NodeDegreeCentrality', 'w')
	position=-1;
	exit =0;
	while exit !=1 :
		biggest=-1
		centrality=nx.degree_centrality(NetworkNc)
		if not centrality:
			exit=1
		
		for i in centrality:
			if biggest <= centrality[i]:
				if(biggest == centrality[i]):
					if(objects[i].getSumEdges() > objects[position].getSumEdges()):
						if (NetworkNc.degree(i) > 1):
							biggest=centrality[i]
							position=i
							exit=0
				else:	
					if (NetworkNc.degree(i) > 1):
						biggest=centrality[i]
						position=i
						exit=0
					else:
						exit=1
				
		if exit!=1:
			if position > -1:
				fileExclusion.write(position+'\n')
				#UpdateTheSum
				for neighbors in NetworkNc.neighbors(position):
					objects[neighbors].updateSum(position)
				NetworkNc.remove_node(position)
	exit=0
	nodes=NetworkNc.nodes()
	centrality=nx.degree_centrality(NetworkN)
	for n in nodes:
		neighbors=NetworkNc.neighbors(n)
		#print neighbors
		#print len(neighbors)
		if len(neighbors)>0:
			for i in neighbors:
				if centrality[n] < centrality[i]:
					fileExclusion.write(i+'\n')
				elif centrality[n] > centrality[i]:
					fileExclusion.write(n+'\n')
				#Extreme case: centrality equals
				else:
					sumIndividual1=0.0
					sumIndividual2=0.0
					
					individual1=objects[n].getAdjacenceListWithoutCutsNormal(cutValue, minValue, maxValue);
					individual2=objects[i].getAdjacenceListWithoutCutsNormal(cutValue, minValue, maxValue);
					
					for j in individual1:
						sumIndividual1=sumIndividual1+individual1[j]
					for j in individual2:
						sumIndividual2=sumIndividual2+individual2[j]
					
					if(sumIndividual1 >= sumIndividual2):
						fileExclusion.write(n+'\n')
					else:
						fileExclusion.write(i+'\n')
				NetworkNc.remove_edge(n,i)
	
def createFolders(folder):
	if folder: 
		if not os.path.exists(folder):
			os.makedirs(folder)
	else:
		usage()
		exit()
		
def readInputFile(inputFile):
	
	individuals={}
	try:
		fileOpened=open(inputFile,'r')
		for line in fileOpened:
			data=line.split()
			#print data
			
			if (not data[0] in individuals):
				individuals[data[0]]= Individuo(data[0])
			
			#print data
			
			if (not data[1] in individuals):
				individuals[data[1]]=Individuo(data[1])
			
			#print data
			individuals[data[0]].insertRelationship(data[1], data[2])
			individuals[data[1]].insertRelationship(data[0], data[2])
	
	
	
	
	except IOError:
		print ('Error: Input file not found: '+inputFile)
		exit()
	
	return individuals
	

def usage():
	print ('==========================================================================================')
	print ('**											**')
	print ('**											**')
	print ('** Required parameters:									**')
	print ('**											**')
	print ('**     --input or -i		Arquivo de entrada					**')
	print ('**     --cutValue or -c		Forma de selecao de ligacoes a serem consideradas	**')
	print ('**     	--valueMin or -v	Valor minimo no criterio de desempate			**')
	print ('**     	--valueMax or -V	Valor maximo no criterio de desempate			**')
	print ('**     --folder or -l		Pasta aonde serao armazenados os arquivos de saida 	**')
	print ('**     --elimination or -e	Método de eliminação (default 1)			**')
	print ('**					1: Centrality Degree				**')
	print ('**					2: Betweenness Degree            		**')
	print ('**					3: Closeness Degree              		**')
	print ('**     --maxValuePossible or -m	Se o método de eliminação for o 2 ou 3, uma norma-	**')
	print ('**				lização deve ser feita:					**')
	print ('**				valorMaximoDaMatrica - valor da ligação			**')
	print ('**     --help or -h		Mostra essa mensagem					**')
	print ('**											**')
	print ('==========================================================================================')
	sys.exit()

def exit():
	print ('If you wanna help, call this script with flag -h')
	sys.exit()




def unix_time(function):
    '''Return `real`, `sys` and `user` elapsed time, like UNIX's command `time`
    You can calculate the amount of used CPU-time used by your
    function/callable by summing `user` and `sys`. `real` is just like the wall
    clock.
    Note that `sys` and `user`'s resolutions are limited by the resolution of
    the operating system's software clock (check `man 7 time` for more
    details).
    '''
    start_time, start_resources = timestamp(), resource_usage(RUSAGE_SELF)
    function()
    end_resources, end_time = resource_usage(RUSAGE_SELF), timestamp()

    return {'real': end_time - start_time,
            'sys': end_resources.ru_stime - start_resources.ru_stime,
            'user': end_resources.ru_utime - start_resources.ru_utime}






if __name__ == "__main__":
	start_time, start_resources = timestamp(), resource_usage(RUSAGE_SELF)



	main()
	end_resources, end_time = resource_usage(RUSAGE_SELF), timestamp()
	print ('real '+ str(end_time - start_time))
	print ('sys '+ str(end_resources.ru_stime - start_resources.ru_stime))
	print ('user '+str( end_resources.ru_utime - start_resources.ru_utime))



	#Possible Function of Pl

	#try:
		#import matplotlib.pyplot as plt
	#except:
		#raise

	#pos=fruchterman_reingold_layout(NetworkN)
	#edgesBigger=[(u,v) for (u,v,d) in NetworkN.edges(data=True) if d['weight'] > cutValue]
	#edgesSmaller=[(u,v) for (u,v,d) in NetworkN.edges(data=True) if d['weight'] <= cutValue]
	
	#print edgesBigger
	#print edgesSmaller
	
	#nx.draw_networkx_nodes(NetworkN,pos,node_size=700)
	#nx.draw_networkx_edges(NetworkN,pos,edgelist=edgesBigger,width=6)
	#nx.draw_networkx_edges(NetworkN,pos,edgelist=edgesSmaller,width=6,alpha=0.5,edge_color='b',style='dashed')
	#nx.draw_networkx_labels(NetworkN,pos,font_size=20,font_family='sans-serif')

	#plt.axis('off')
	#plt.savefig("weighted_graph.png") # save as png
	#plt.show() 
