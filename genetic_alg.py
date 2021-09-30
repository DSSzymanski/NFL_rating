import math
from random import randint, random
from stat_eval import prediction_expanded_stats

def genetic_algorithm(pop_size=100, generations=100):
    """
    Genetic algorithm is the main function that is called to try and generate
    the ideal weights to be used in the elo calculations. The entities are
    a list of values representing the weights for the k-factor, rating-factor,
    home field advantage, seasonal scaling, and playoff_multiplier. The algorithm
    is run with a population of pop_size and generations number of times.

    :param pop_size: int value representing how many entities are in a population.
    :param generations: int value representing how many times the genetic algorithm
                        will run.

    :return list: returns list of lists, representing the final population made
                  up of the entity and it's associated fitness value.
    """
    #generate initial population
    population = initial_population(pop_size)
    #find fitness of initial population and prune so that only 2/3 remain
    pop_fitness = population_fitnesses(population)[:2*math.floor(pop_size/3)]
    #get best entity and fitness for print statement
    pop_fitness[0][1] = round(pop_fitness[0][1], 5)
    #get worst entity and fitness for print statement
    pop_fitness[len(pop_fitness)-1][1] = round(pop_fitness[len(pop_fitness)-1][1], 5)
    print(f'Initial Generation: Best: {pop_fitness[0]} Worst: {pop_fitness[len(pop_fitness)-1]}')

    #loops 1 through generations+1 because generation 0 is the initial gen.
    for gen in range(1, generations+1):
        new_population = []
        #elitism, add previous generation's best fitness valued entity
        new_population.append(pop_fitness[0][0])

        for _ in range(1, pop_size):
            #genetic selection
            parent1 = pop_fitness[randint(0, len(pop_fitness)-1)][0]
            parent2 = pop_fitness[randint(0, len(pop_fitness)-1)][0]
            #reproduce and add to new population
            child = reproduce(parent1, parent2)
            new_population.append(child)

        #update population to new children generated in function
        population = new_population
        #find fitness of new population and prune so that only 2/3 remain
        pop_fitness = population_fitnesses(population)[:2*math.floor(pop_size/3)]
        #get best and worst fitness based entities for print statement
        pop_fitness[0][1] = round(pop_fitness[0][1], 5)
        pop_fitness[len(pop_fitness)-1][1] = round(pop_fitness[len(pop_fitness)-1][1], 5)
        print(f'Generation {gen}: Best: {pop_fitness[0]} Worst: {pop_fitness[len(pop_fitness)-1]}')

    return pop_fitness

def reproduce(parent1, parent2):
    """
    Simulates reproduction between 2 entities. Instead of selecting a crossover
    point as traditionally is done, generates random number to decide. Each
    parent has a 45% chance of having their gene selected while there's a 10%
    chance of the gene mutating. Returns a new entity.
    """
    child = []
    for index, (gene1, gene2) in enumerate(zip(parent1, parent2)):
        prob = random()
        if prob <= .45:
            child.append(gene1)
        elif prob <= .9:
            child.append(gene2)
        else:
            child.append(mutate(index))
    return child

def mutate(index):
    """
    Simulates a 'mutated gene' by taking which gene is being mutated and generating
    a new random value for that gene.

    :param index: int representing which index gene of an entity is being mutated.

    :return int/float: returns an int if indes is for k-factor, rating-factor,
                       or homefield advantage, and a float for the others
                       representing a new mutated gene.
    """
    if index == 0:
        return random_k()
    if index == 1:
        return random_rf()
    if index == 2:
        return random_hfa()
    if index == 3:
        return random_scale()
    return random_playoff_multiplier()

def population_fitness(entity):
    """
    Calculates the fitness value for a single entity using an evaluation of
    how many games are predicted right that are in the dataset.

    :param entity: a single entity made up of values of:
                   [k-factor, rating-factor, home field advantage, seasonal scaling,
                   playoff multiplier].

    :return list: a list containing the entity and it's fitness value.
    """
    prediction = prediction_expanded_stats(entity[0], entity[1], entity[2], entity[3], entity[4])[1]
    return [entity, prediction]

def population_fitnesses(pop):
    """
    Calculates the fitness values for every entity in a population using an
    evaluation of how many games are predicted right that are in the dataset.

    :param pop: a list of entities representing a population. Each entity is a
                list made up of values of:
                [k-factor, rating-factor, home field advantage, seasonal scaling,
                 playoff multiplier].

    :return list: returns sorted list of lists, the inner list being a single
                  entity and it's associated fitness value.
    """
    pop_fitness = []
    for entity in pop:
        #run against every game and get percentage of games predicted right
        prediction = prediction_expanded_stats(entity[0], entity[1], entity[2],\
                                               entity[3], entity[4])[1]
        pop_fitness.append([entity, prediction])
    """
    Sort all values according to their fitness value.
    IMPORTANT: entities in population are pruned later for reproduction, so a
    change in ordering will cause the algorithm to choose non-ideal candidates
    for reproduction.
    """
    return sorted(pop_fitness, key=lambda x:x[1], reverse=True)

def initial_population(pop_size):
    """
    Initializes a population to be used in the genetic algorithm. The population
    is determined on the input size of randomly created entities and returned
    as a list.

    :param pop_size: an integer value representing how many entities are in a
                     population.

    :return list:    returns a list of entities as an initial population.
    """
    pop = []
    for _ in range(pop_size):
        pop.append(create_single())
    return pop

def create_single():
    """
    Creates a single entity for a population. Entity consists of random numbers
    for each gene and is returned as a list.

    :return list: returns a list of random number representing a single entity.
    """
    k = random_k()
    rating_factor = random_rf()
    hfa = random_hfa()
    scale = random_scale()
    playoff_multiplier = random_playoff_multiplier()
    return [k, rating_factor, hfa, scale, playoff_multiplier]

def random_k():
    """
    Generates a random number for the k-factor in the elo calculation between
    1 and 1000. K-factor is a boundry on the max amount an elo can change in 1
    game.

    NOTE: if zero, ratings won't change after games.

    :return int: returns an int between 1 and 1000.
    """
    return randint(1, 1000)

def random_rf():
    """
    Generates a random number for the rating-factor in the elo calculation between
    50 and 1000. The rating factor determines how much elo it takes to increase
    the percent chance of a winner by a factor of 10.

    NOTE: if changed, factors of below 50 tend to make the function too
    exponential to run.

    :return int: returns an int between 50 and 1000.
    """
    return randint(50, 10000)

def random_hfa():
    """
    Generates a random number between 0 and 500 for the home field advantage,
    which is a flat elo increase for the home team.

    :return int: returns an int between 0 and 500.
    """
    return randint(0, 500)

def random_scale():
    """
    Generates a random number between 0 and 100 to scale the teams elo after
    each season. The number is divided by 100 to create and return a float.

    :return float: returns an float between 0 and 1.
    """
    return randint(0, 100)/100

def random_playoff_multiplier():
    """
    Generates a random number between 1 and 200 to scale the elo changes
    that result from playoff games. The number is divided by 100 to create and
    return a float.

    :return float: returns an float greater than 0 and <= 2.
    """
    return randint(1, 200)/100

genetic_algorithm(250, 250)
print(f'Base elo calculation: {population_fitness([32, 400, 0, 1, 1])}')
