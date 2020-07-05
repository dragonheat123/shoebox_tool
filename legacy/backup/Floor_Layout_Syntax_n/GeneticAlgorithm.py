import random
import numpy as np
import Floor_Layout_Syntax.Constants as Constants
import time
#dnaList ops
def getLeastSpaceAndFilterOutDups(dnaList):
    leastSpace = float('inf')
    newList = []
    hashSet = set()
    for dna in dnaList:
        if dna.emptySpace < leastSpace:
            leastSpace = dna.emptySpace
            newList = [dna]
            hashSet = set([dna.hash])
        elif dna.emptySpace == leastSpace:
            if dna.hash not in hashSet:
                newList.append(dna)
                hashSet.add(dna.hash)
    return newList

def KL(P,Q):
    """ Epsilon is used here to avoid conditional code for
    checking that neither P nor Q is equal to 0. """
    #epsilon = 0.00001
    # You may want to instead make copies to avoid changing the np arrays.
    A = P#+epsilon
    B = Q#+epsilon
    divergence = np.sum(Q*np.abs(A-B))
    return divergence

#In our use case, 
#--dnaLength corresponds to number of floors being matched to a distribution
#--genePool to the possible values a floor can take
#Our fitness function is a minimization problem, the lower the difference between target and population, the better
#--min(magnitude(normalized(v)-targetDistribution))
#-->max(1-magnitude(normalized(v)-targetDistribution))
    
class Population:
    def __init__(self, targetDist, dnaLength, mutationRate, genePool, popCount):
        self.population = []
        self.matingPool = []
        self.generation = 0
        self.targetDist = targetDist
        self.mutationRate = mutationRate
        self.genePool = genePool
        self.bestFitness = float('-inf')
        self.bestResults = []
        self.fitnessSum=0
        for i in range(popCount):
            self.population.append(DNA(dnaLength, genePool))
        self.calcFitness()
    
    #calculates fitness for each member in population
    def calcFitness(self):
        self.fitnessSum=0
        for dna in self.population:
            dna.calcFitness(self.targetDist)
            self.fitnessSum+=dna.fitness
        
    
    #kills the unfit
    def naturalSelection(self):
        self.matingPool = []
        p=[]
        # for dna in self.population:
        #     p.append(dna.fitness/self.fitnessSum)
        # while len(self.matingPool)<len(self.population):
        #     x = np.random.randint(low=0, high=len(self.population))
        #     if np.random.binomial(1,p[x])==1:
        #         self.matingPool.append(self.population[x])
        #print("===============Generation ",self.generation)
        for dna in self.population:
            p.append(dna.fitness)
        #print(p)
        while len(self.matingPool)<100:
            fit_idx = p.index(max(p))
            #print("max index:",fit_idx,p)
            self.matingPool.append(self.population[fit_idx])
            self.population.pop(fit_idx)
            #print("Res. pop:",self.population)
            p.pop(fit_idx)
            #print("------------------------")
            #time.sleep(0.5)
        #time.sleep(0.5)
            
    def generate(self):
        self.new_gen = []                
        for i in range(Constants.GA_POPCOUNT-len(self.matingPool)):
            partnerA = self.matingPool[random.randrange(len(self.matingPool))]
            partnerB = self.matingPool[random.randrange(len(self.matingPool))]
            child = partnerA.crossover(partnerB)
            child.mutate(self.mutationRate)
            self.new_gen.append(child)
        self.population = self.new_gen + self.matingPool
        #print('gen',self.population)
        self.generation+=1
        
    def evaluate(self):
        #Consider multiple solutions// though they may just be different permutations
        worldRecord = float('-inf')
        worldFittests = []
        for g in self.population:
            if g.fitness > worldRecord: 
                worldRecord = g.fitness
                worldFittests = [g]
            elif g.fitness == worldRecord:
                for w in worldFittests:
                    if w.genes.sort() != g.genes.sort():
                        worldFittests.append(g)
        #if we don't care about best results, the conditional block can be removed
        if worldRecord > self.bestFitness:
            self.bestResults = worldFittests
            self.bestFitness = worldRecord
        elif worldRecord == self.bestFitness:
            self.bestResults.extend(worldFittests)
            self.bestResults = getLeastSpaceAndFilterOutDups(self.bestResults)
            self.bestFitness = worldRecord
        print('gen '+str(self.generation)+' record holder: '+str(worldFittests[0].genes)+' fitness: '+str(worldFittests[0].fitness))
        
    def printBestResults(self,unitCombinations,oriDist,drawComparisonChart):
        print('---Best records---\n'+'fitness: '+str(self.bestFitness))
        drawComparisonChart(oriDist, self.bestResults[0].v, "Comparison Distribution for DNA "+str(self.bestResults[0].genes))
#        for dna in self.bestResults:
#            drawComparisonChart(oriDist, dna.v, "Comparison Distribution for DNA "+str(dna.genes))
#            for layoutIndex in dna.genes:
#                print(unitCombinations[layoutIndex])
        print('------------------\n')


class DNA:
    def __init__(self, length, genePool):
        self.genes = []
        self.length = length
        self.genePool=genePool
        self.genePoolKeys = list(genePool.keys())   #changed to randomize index for dictionary
        self.v=[0]*len(Constants.UNIT_TYPES)   #normalized distribution of unit type counts [type0,type1,type2,type3,type4]
        self.fitness = float('-inf')
        self.emptySpace = 0
        self.hash = 0
        for i in range(length):
#            self.genes.append(random.randrange(len(genePool)))
            self.genes.append(random.choice(list(self.genePoolKeys)))
            
    def calcFitness(self,targetDist):
        self.emptySpace = 0
        #foreach floor in the gene, get cumulative total of units
        for g in self.genes:
            self.v=np.add(self.v,self.genePool[g]['countVector'])
            self.hash += g #simple function to filter duplicates later; can be improved by somehow combining emptySpace
            self.emptySpace += self.genePool[g]['emptySpace']
#        print(v)
        #normalize vector
        self.v = self.v/(np.sum(self.v, axis=0))
        
        #KL divergence
        self.fitness = -KL(self.v,targetDist)
        
        #find magnitude of difference between vector and target distribution
#        v=np.subtract(v, targetDist)
        #subtract from 1 to turn minimization to maximization
#        self.fitness = 1 - np.sqrt(v.dot(v))
#        print('fitness: '+str(self.fitness))
        
    def crossover(self,partner):
        child = DNA(self.length,self.genePool)
        midPoint = int(len(self.genes)/2) #random.randrange(len(self.genes))
        for i in range(len(self.genes)):
            if i > midPoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i]=partner.genes[i]
        return child
    
    def mutate(self,mutationRate):
        for i in range(len(self.genes)):
            if random.random() < mutationRate:
                self.genes[i] = random.choice(list(self.genePoolKeys))