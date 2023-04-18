import random
import Chromosome as ch
import numpy.random as npr


# create a random chromosome 
def create_random_list(n_list):
    start = n_list[0]  # start and end points should be same, so keep the first point before shuffling

    temp = n_list[1:]
    temp = random.sample(temp, len(temp))  # shuffle the node list

    temp.insert(0, start)  # add start point to the beginning of the chromosome
    temp.append(start)  # add start point to the end, because route should be ended where it started
    return temp


# initialization
def initialization(data, pop_size):
    initial_population = []
    for i in range(0, pop_size):  # create chromosomes as much as population size
        temp = create_random_list(data)
        new_ch = ch.Chromosome(temp)
        initial_population.append(new_ch)
    return initial_population


# selection of parent chromosomes to create child chromosomes
def tournament_selection(population):  # tournament selection
    ticket_1, ticket_2, ticket_3, ticket_4 = random.sample(range(0, 99), 4)  # random 4 tickets

    # create candidate chromosomes based on ticket numbers
    candidate_1 = population[ticket_1]
    candidate_2 = population[ticket_2]
    candidate_3 = population[ticket_3]
    candidate_4 = population[ticket_4]

    # select the winner according to their costs
    if candidate_1.fitness_value > candidate_2.fitness_value:
        winner = candidate_1
    else:
        winner = candidate_2

    if candidate_3.fitness_value > winner.fitness_value:
        winner = candidate_3

    if candidate_4.fitness_value > winner.fitness_value:
        winner = candidate_4

    return winner  # winner = chromosome

# Roulette Wheel Selection 
def roulette_selection(population):
    max = sum([c.fitness for c in population])
    selection_probs = [c.fitness/max for c in population]
    return population[npr.choice(len(population), p=selection_probs)]



# Two points crossover
def crossover(p_1, p_2):  # two points crossover
    point_1, point_2 = random.sample(range(1, len(p_1.chromosome)-1), 2)
    begin = min(point_1, point_2)
    end = max(point_1, point_2)

    child_1 = p_1.chromosome[begin:end+1]
    child_2 = p_2.chromosome[begin:end+1]

    child_1_remain = [item for item in p_2.chromosome[1:-1] if item not in child_1]
    child_2_remain = [item for item in p_1.chromosome[1:-1] if item not in child_2]

    child_1 += child_1_remain
    child_2 += child_2_remain

    child_1.insert(0, p_1.chromosome[0])
    child_1.append(p_1.chromosome[0])

    child_2.insert(0, p_2.chromosome[0])
    child_2.append(p_2.chromosome[0])

    return child_1, child_2



# Mutation 
def mutation(chromosome):  # swap two nodes of the chromosome
    mutation_index_1, mutation_index_2 = random.sample(range(1, 19), 2)
    chromosome[mutation_index_1], chromosome[mutation_index_2] = chromosome[mutation_index_2], chromosome[mutation_index_1]
    return chromosome


# Find the best chromosome of the generation based on the cost
def find_best(generation):
    best = generation[0]
    for n in range(1, len(generation)):
        if generation[n].cost < best.cost:
            best = generation[n]
    return best


# used elitism, crossover, mutation operators to create a new generation based on a previous generation
def create_new_generation(previous_generation, mutation_rate):
    new_generation = [find_best(previous_generation)]  # this is for elitism. keep the best of the previous generation.

    # used two chromosomes and create two chromosomes. so iteration size will be half of the population size
    for a in range(0, int(len(previous_generation)/2)):
        parent_1 = tournament_selection(previous_generation)
        parent_2 = tournament_selection(previous_generation)

        child_1, child_2 = crossover(parent_1, parent_2)  
        child_1 = ch.Chromosome(child_1) #objects created
        child_2 = ch.Chromosome(child_2)

        if random.random() < mutation_rate:
            mutated = mutation(child_1.chromosome)
            child_1 = ch.Chromosome(mutated)

        new_generation.append(child_1)
        new_generation.append(child_2)

    return new_generation


