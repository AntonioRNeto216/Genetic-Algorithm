'''
This file defines DataVisualizer Class
'''

# Python Imports
import os
import typing
import statistics
import matplotlib.pyplot as plt

# Src Imports
from src.individual import Individual


class DataVisualizer:

    def __init__(self) -> None:
        self._fittests_log = []

        self._higher_fitnesses = []
        self._medium_fitnesses = []
        self._lower_fitnesses = []

        self._standard_deviations = []
        self._mean = []
        self._variance = []

        self._setup_executions_path()

    def _setup_executions_path(self) -> None:
        executions_folder_path = f'{os.getcwd()}/data/executions' 
        if not os.path.exists(executions_folder_path):
            os.mkdir(executions_folder_path)

        self._output_path = f'{executions_folder_path}/{len(os.listdir(executions_folder_path)) + 1}'
        os.mkdir(self._output_path)

    def new_generation_data(self, generation_number: int, population: typing.List[Individual]) -> None:
        
        # Sort population
        sorted_population = sorted(
            population,
            key = lambda individual : individual.return_fitness_value()
        )

        fittest = sorted_population[0]
        medium_fit = sorted_population[int(len(sorted_population) / 2) - 1]
        less_fit = sorted_population[-1]

        # Update Convergence Data
        self._higher_fitnesses.append(fittest.return_fitness_value())
        self._medium_fitnesses.append(medium_fit.return_fitness_value())
        self._lower_fitnesses.append(less_fit.return_fitness_value())

        # Update Statistics Data
        all_fitness_from_population = [individual.return_fitness_value() for individual in sorted_population]
        self._standard_deviations.append(statistics.stdev(all_fitness_from_population))
        self._mean.append(statistics.mean(all_fitness_from_population))
        self._variance.append(statistics.variance(all_fitness_from_population))

        fittest_log_content = f'Fittest of Generation ({generation_number})\n{str(fittest)}'
        self._fittests_log.append(fittest_log_content)

        print(fittest_log_content)

    def generate_files(
            self, 
            number_of_generations: int, 
            population_size: int, 
            probability_of_crossover: float, 
            probability_of_mutation: float, 
            tournament_parameter_N: int,
            tournament_parameter_K: float
        ) -> None:
        
        # Generates Fittest Log
        with open(f'{self._output_path}/fittest_of_all_generations.txt', 'w') as file:

            file.write('++++ Network Parameters ++++\n')
            file.write(f'Number of Generation: {number_of_generations}\n')
            file.write(f'Population Size: {population_size}\n')
            file.write(f'Probability of Crossover: {probability_of_crossover}\n')
            file.write(f'Probability of Mutation: {probability_of_mutation}\n')
            file.write(f'Tournament Parameter N: {tournament_parameter_N}\n')
            file.write(f'Tournament Parameter K: {tournament_parameter_K}\n\n')

            file.write('++++ Fittest Individuals ++++\n\n')
            file.writelines(self._fittests_log)

        # Manipulating Graph Data
        _, (graphs) = plt.subplots(2,2)
        x_axis = [i for i in range(number_of_generations)]

        # Generates Convergence Graph
        graphs[0, 0].plot(x_axis, self._higher_fitnesses, label='Fittest Individual')
        graphs[0, 0].plot(x_axis, self._medium_fitnesses, label='Average Individual')
        graphs[0, 0].plot(x_axis, self._lower_fitnesses, label='Lower Individual')
        graphs[0, 0].set_xlabel('Number of Generations')
        graphs[0, 0].set_ylabel('Fitness')
        graphs[0, 0].set_title('Convergence Graph')
        graphs[0, 0].legend(fontsize='7')

        # Generates Statistics Graphs
        graphs[0, 1].plot(x_axis, self._standard_deviations)
        graphs[0, 1].set_xlabel('Number of Generations')
        graphs[0, 1].set_ylabel('Value')
        graphs[0, 1].set_title('Standard Deviation')

        graphs[1, 0].plot(x_axis, self._mean)
        graphs[1, 0].set_xlabel('Number of Generations')
        graphs[1, 0].set_ylabel('Value')
        graphs[1, 0].set_title('Mean')

        graphs[1, 1].plot(x_axis, self._variance)
        graphs[1, 1].set_xlabel('Number of Generations')
        graphs[1, 1].set_ylabel('Value')
        graphs[1, 1].set_title('Variance')

        plt.tight_layout()
        plt.savefig(f'{self._output_path}/convergence_and_statistics_graphs.png')
        plt.show()

        print(f'All data saved at: {self._output_path}')
