from random import randint, random
from stat_eval import prediction_expanded_stats
import math

def genetic_algorithm(pop_size, generations=1):
    population = initial_population(pop_size)
    pop_fitness = population_fitnesses(population)[:2*math.floor(pop_size/3)]
    print(f'Initial Generation: Best: {pop_fitness[0]} Worst: {pop_fitness[len(pop_fitness)-1]}')
    for gen in range(1, generations+1):
        new_population = []
        
        new_population.append(pop_fitness[0][0])
        
        
        for i in range(1, pop_size):
            parent1 = pop_fitness[randint(0, len(pop_fitness)-1)][0]
            parent2 = pop_fitness[randint(0, len(pop_fitness)-1)][0]
            child = reproduce(parent1, parent2)
            new_population.append(child)
            
        population = new_population
        pop_fitness = population_fitnesses(population)[:2*math.floor(pop_size/3)]
        print(f'Generation {gen}: Best: {pop_fitness[0]} Worst: {pop_fitness[len(pop_fitness)-1]}')
        
    return pop_fitness
    
def reproduce(p1, p2):
    child = []
    for gene in range(len(p1)):
        prob = random()
        
        if prob <= .45:
            child.append(p1[gene])
        elif prob <= .9:
            child.append(p2[gene])
        else:
            child.append(mutate(gene))
    return child
    
def mutate(index):
    if index == 0:
        return randomK()
    elif index == 1:
        return randomRF()
    else:
        return randomHFA()

def population_fitnesses(pop):
     pop_fitness = []
     for single in pop:
         pop_fitness.append([single, prediction_expanded_stats(single[0], single[1], single[2])[1]])
     return sorted(pop_fitness, key=lambda x:x[1], reverse=True)

def initial_population(pop_size):
    pop = []
    for x in range(pop_size):
        K = randomK()
        rating_factor = randomRF()
        hfa = randomHFA()
        pop.append([K, rating_factor, hfa])
    return pop

def randomK():
    return randint(0, 1000)

def randomRF():
    return randint(50, 1000)

def randomHFA():
    return randint(0, 500)

genetic_algorithm(50, 25)