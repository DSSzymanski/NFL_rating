from random import randint, random
from stat_eval import prediction_expanded_stats
import math

def genetic_algorithm(pop_size, generations=1):
    checked = {}
    checked['saved'] = 0
    population = initial_population(pop_size)
    pop_fitness = population_fitnesses(population, checked)[:2*math.floor(pop_size/3)]
    pop_fitness[0][1] = round(pop_fitness[0][1], 5)
    pop_fitness[len(pop_fitness)-1][1] = round(pop_fitness[len(pop_fitness)-1][1], 5)
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
        pop_fitness = population_fitnesses(population, checked)[:2*math.floor(pop_size/3)]
        pop_fitness[0][1] = round(pop_fitness[0][1], 5)
        pop_fitness[len(pop_fitness)-1][1] = round(pop_fitness[len(pop_fitness)-1][1], 5)
        print(f'Generation {gen}: Best: {pop_fitness[0]} Worst: {pop_fitness[len(pop_fitness)-1]}')
        print(checked['saved'], len(checked.keys()))
        
    return pop_fitness
    
def reproduce(p1, p2):
    child = []
    #print(p1, p2)
    for gene in range(len(p1)):
        prob = random()
        if prob <= .4:
            child.append(p1[gene])
        elif prob <= .8:
            child.append(p2[gene])
        else:
            child.append(mutate(gene))
    return child
    
def mutate(index):
    if index == 0:
        return randomK()
    elif index == 1:
        return randomRF()
    elif index == 2:
        return randomHFA()
    else:
        return randomScale()

def population_fitness(single, checked):
    if str(single) not in checked:
        prediction = prediction_expanded_stats(single[0], single[1], single[2], single[3])[1]
        checked[str(single)] = prediction
        return [single, prediction]
    else:
        checked['saved'] += 1
        return [single, checked[str(single)]]

def population_fitnesses(pop, checked):
     pop_fitness = []
     for single in pop:
         if str(single) not in checked:
             prediction = prediction_expanded_stats(single[0], single[1], single[2], single[3])[1]
             checked[str(single)] = prediction
             pop_fitness.append([single, prediction])
         else:
             checked['saved'] += 1
             pop_fitness.append([single, checked[str(single)]])
     return sorted(pop_fitness, key=lambda x:x[1], reverse=True)

def initial_population(pop_size):
    pop = []
    for x in range(pop_size):
        pop.append(create_single())
    return pop

def create_single():
    K = randomK()
    rating_factor = randomRF()
    hfa = randomHFA()
    scale = randomScale()
    return [K, rating_factor, hfa, scale]

def randomK():
    return randint(0, 1000)

def randomRF():
    return randint(50, 1000)

def randomHFA():
    return randint(0, 500)

def randomScale():
    return randint(0, 100)/100

genetic_algorithm(250, 100)