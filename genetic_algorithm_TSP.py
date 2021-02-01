import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

# Create necessary classes and functions
# Create class to handle "markers"

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return round(c * r,3)


class Marker:
    def __init__(self, x, y):
        '''
        Intialize the coordinates for the markers
        '''
        self.x = x
        self.y = y
    
    def distance(self, Marker):
        '''
        Calculate the distance between 2 markers
        '''
        distance = haversine(self.x,self.y,Marker.x,Marker.y)
        return distance
    
    def __repr__(self):
        '''
        To print the coordinates
        '''
        return "(" + str(self.x) + "," + str(self.y) + ")"


# Create a fitness function
class Fitness:
    def __init__(self, route):
        '''
        To intialize the route 
        '''
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        '''
        Calculate the whole distance for the route
        '''
        # print("Inside calculate"+ str(len(self.route)))
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromMarker = self.route[i]
                toMarker = None
                if i + 1 < len(self.route):
                    toMarker = self.route[i + 1]
                else:
                    toMarker = self.route[0]
                pathDistance += fromMarker.distance(toMarker)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        '''
        Inverse of the route distance is the fitness of the route
        '''
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness


# ## Create our initial population

# Route generator

def createRoute(MarkerList, home):
    ''' Create route by random the list of markers '''
    route = random.sample(MarkerList, len(MarkerList))
    route.remove(home)
    route.insert(0,home)
    route.append(home)
    # print(len(route))
    return route


# Create first "population" (list of routes)

def initialPopulation(popSize, MarkerList , home):
    '''
    Create a list of routes as initial population
    '''
    population = []

    for i in range(0, popSize):
        population.append(createRoute(MarkerList, home))
    return population


## Create the genetic algorithm

# Rank individuals

def rankRoutes(population):
    '''
    Rank the route based on fitness values.
    The most fitted are at the start of the list.
    '''
    fitnessResults = {}
    for i in range(0,len(population)):
        # print("Solution length: "+ str(len(population[i])))
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)


# Create a selection function that will be used to make the list of parent routes

def selection(popRanked, eliteSize):
    '''
    Return route IDs of the best route.
    '''
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize): # elitism
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults


# Create mating pool


def matingPool(population, selectionResults):
    '''
    Create a mating pool with routes with best fitness value.
    '''
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool


# Create a crossover function for two parents to create one child

def breed(parent1, parent2):
    '''
    Crossover between 2 routes.
    
    '''
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    # print("Child lenght: "+ (str(len(child))))
    return child


# Create function to run crossover over full mating pool

def breedPopulation(matingpool, eliteSize):
    '''
    Crossover on the whole population.
    '''
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children


# Create function to mutate a single route

def mutate(individual, mutationRate, home):
    '''
    Swapping the markers to make the route not the same as the generations before
    '''
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            Marker1 = individual[swapped]
            Marker2 = individual[swapWith]
            
            individual[swapped] = Marker2
            individual[swapWith] = Marker1
    individual = [i for i in individual if i != home]
    individual.insert(0,home)
    individual.append(home)
    return individual


# Create function to run mutation over entire population

def mutatePopulation(population, mutationRate, home):
    '''
    Run mutation on whole population
    '''
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate, home)
        mutatedPop.append(mutatedInd)
    return mutatedPop


# Put all steps together to create the next generation


def nextGeneration(currentGen, eliteSize, mutationRate, home):
    '''
    A function to get the next generation
    '''
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate, home)
    return nextGeneration


# Final step: create the genetic algorithm

def geneticAlgorithm(population,home, popSize, eliteSize, mutationRate, generations):
    '''
    A function to run the whole GA
    '''
    pop = initialPopulation(popSize, population, home)
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))
    
    for i in range(0, generations):
        # print("Generattion: " + str(i))
        pop = nextGeneration(pop, eliteSize, mutationRate, home)
    
    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute


# ## Running the genetic algorithm

# Create list of markers


# markers = [(3.119629449776096, 101.65642710502878),
# (3.119570613676185, 101.65657144167113),
# (3.11950698203576, 101.65672277258696),
# (3.119450850925013, 101.65687356698822),
# (3.1194002523972264, 101.65702708276075),
# (3.1193620989000945, 101.65717911039806),
# (3.119237741578333, 101.65733614239487),
# (3.119210480539193, 101.65748546964066),
# (3.1193747311242292, 101.65732762732425),
# (3.1193651207520348, 101.65747932987146),
# (3.1191452863986697, 101.6576379980372),
# (3.119117835549454, 101.6577883650018),
# (3.119318123645613, 101.65763163276269),
# (3.1193085095435045, 101.65778339418767),
# (3.1190526841770363, 101.65794065912831),
# (3.119025140123476, 101.65809153663653),
# (3.1192615207635943, 101.65793556564249),
# (3.119251904521294, 101.65808736085103),
# (3.118962905339048, 101.65824361260565),
# (3.1189384653502845, 101.65839337817877),
# (3.119207798610268, 101.65823943589713),
# (3.1191981812041214, 101.65839124947732),
# (3.11899320291459, 101.65852313161388),
# (3.119190524651296, 101.65854303493941),
# (3.1192110057350386, 101.65867096627734)
# ]



# MarkerList = []
# for i in range(len(markers)):
#     MarkerList.append(Marker(x=markers[i][0], y=markers[i][1]))

# home = MarkerList[0]

# ## Marker mapping
# mapping_dict = {}
# for idx, i in enumerate(MarkerList):
#     mapping_dict[i] = idx

# print(mapping_dict)

# # Run the genetic algorithm

# bestpath = geneticAlgorithm(population=MarkerList,home=home, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)
# for idx,i in enumerate(bestpath):
#     # bestroute.append(mapping_dict[i])
#     print(mapping_dict[i])


# tes = [1,1,2,3,4]
# tes = [i for i in tes if i != 1]
# tes
# route = random.sample(MarkerList, len(MarkerList))
# type(route[0])
# route.remove(home)
# route.insert(0,home)
# route.append(home)
# print(route)