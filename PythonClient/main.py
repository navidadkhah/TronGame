import pandas as pd
import pygad
import numpy


def get_data():
    train = pd.read_csv("train.csv")
    test = pd.read_csv("test.csv")

    return train, test

def fitness_func(ga_instance, solution, solution_idx):
    sum = 0
    for i in range(0, 1000):
        for j in range(len(solution)):
            output =numpy.sum(solution[j] * train_data.iloc[i][j+1])
        output = output + solution[0]
        sum += (output - train_data.iloc[i][10]) ** 2
    return 1/sum

def test_func(bestsolution):
    for i in range(1000):
        for j in range(10):
            output = numpy.sum(bestsolution[j + 1] * test_data.iloc[i][j])
    return output



if __name__ == "__main__":

    train_data, test_data = get_data()
    fitness_function = fitness_func


    num_generations = 80
    num_parents_mating = 4

    sol_per_pop = 8
    num_genes = 8

    init_range_low = -2
    init_range_high = 5

    parent_selection_type = "rws"
    keep_parents = 1

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=None,
                           mutation_percent_genes=mutation_percent_genes)

    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))



