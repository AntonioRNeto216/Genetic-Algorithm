'''
File to define the GeneticAlgorithm Class 
'''

# Python Imports
import random
import typing

# Src Imports
from src.individual import Individual
from src.data_visualizer import DataVisualizer


class GeneticAlgorithm:
    '''
    Holds all process and data to generate an answer for the problem.

    Attributes:
    - ``self._data``: holds all information from flights.txt
    - ``self._population``: a list that holds 'population_size' Individuals
    - ``self._data_visualizer``: class to manage visualization
    - ``self._number_of_generations``: low_number < N < high_number
    - ``self._population_size``: low_number < N < high_number
    - ``self._probability_of_crossover``: 0 < p < 1
    - ``self._probability_of_mutation``: 0 < p < 1
    - ``self._tournament_parameter_N``: N > 0
    - ``self._tournament_parameter_K``: 0 <= K <= 1
    '''

    def __init__(self) -> None:
        '''
        Defines parameters and attribute. In addition, it generates a database.
        '''
        self._define_parameters_and_attributes()
        self._generates_database()

    def _define_parameters_and_attributes(self) -> None:
        '''
        Defines the basic data.
        '''
        self._data = {}
        self._population = []

        self._data_visualizer = DataVisualizer()

        self._number_of_generations = 100   
        self._population_size = 100         
        self._probability_of_crossover = 0.5
        self._probability_of_mutation = 0.05
        self._tournament_parameter_N = 5    
        self._tournament_parameter_K = 0.75 

    def _generates_database(self) -> None:
        '''
        Generates a dictionary to hold all data from flights.txt.

        The structure is: 
        ```
        {
            'origin1': {
                'destination11': [ 
                    [start_time1, end_time1, price1],
                    [start_time2, end_time2, price2],
                    ...
                ],
                ...
            },
            'origin2': {
                'destination21': [ 
                    [start_time1, end_time1, price1],
                    [start_time2, end_time2, price2],
                    ...
                ],
                ...
            },
        }
        ```
        '''
        with open('data/flights.txt', 'r') as file:
            for line in file.readlines():
                origin, destination, start_time, end_time, value = line.replace('\n', '').split(',')
            
                if origin not in self._data:
                    self._data[origin] = {}
                
                if destination not in self._data[origin]:
                    self._data[origin][destination] = []

                self._data[origin][destination].append((start_time, end_time, value))
        
    def _define_new_population(self) -> None:
        '''
        Generates 'population_size' individuals and append all of them to the population list.

        This method generates the first set of individuals, but after it isn't called anymore.
        '''
        for _ in range(self._population_size):
            self._population.append(Individual(self._data, None))

    def _fitness_function_for_all_population(self) -> None:
        '''
        Updates fitness from all population. 
        '''
        for individual in self._population:
            individual.update_fitness_value()

    def _tournament_selection(self) -> Individual:
        '''
        Selects the fittest or lower fit individual from the tournament and returns it.

        Returns:
        The fittest or lower fit individual from the tournament
        '''
        selected_individuals = random.choices(
            population = self._population,
            k = self._tournament_parameter_N
        )

        selected_individuals.sort(
            key = lambda individual : individual.return_fitness_value()
        )

        parameter_r = random.randint(0, 100) / 100 
        select_fittest = parameter_r < self._tournament_parameter_K

        return selected_individuals[0 if select_fittest else -1]

    def _crossover(self, first_individual: Individual, second_individual: Individual) -> typing.Union[typing.Tuple[Individual], None]:
        '''
        If the crossover happens, two individuals are generate from the cross and both of them are returned.
        Otherwise,  a None value is returned.

        Parameters:
        - ``first_individual``: the first individual 
        - ``second_individual``: the second individual

        Returns:
        A tuple holding the children or None if the crossover didn't happen
        '''
        generate_descendant = random.randint(0, 100) / 100 < self._probability_of_crossover

        if not generate_descendant:
            return None
        
        position_to_cross = random.randint(1, 11)

        first_new_individual_data = (first_individual.return_a_piece_of_individual_data(0, position_to_cross), second_individual.return_a_piece_of_individual_data(position_to_cross, -1))
        first_new_individual = Individual(
            data = self._data,
            parents_individual_data_definition = first_new_individual_data
        )

        second_new_individual_data = (second_individual.return_a_piece_of_individual_data(0, position_to_cross), first_individual.return_a_piece_of_individual_data(position_to_cross, -1))
        second_new_individual = Individual(
            data = self._data,
            parents_individual_data_definition = second_new_individual_data
        )

        new_pair = (first_new_individual, second_new_individual)

        return new_pair

    def _mutation(self) -> None:
        '''
        Iterates over all population and applies mutation if the probability occurs.
        '''
        for individual in self._population:
            mutate = random.randint(0, 100) / 100 < self._probability_of_mutation

            if mutate:
                individual.individual_mutation()

    def execute(self) -> None:
        '''
        Executes all process to define the answer.
        '''
        self._define_new_population()
        for i in range(self._number_of_generations):
            
            self._fitness_function_for_all_population()

            # Sort population
            self._population.sort(
                key = lambda individual : individual.return_fitness_value()
            )

            self._data_visualizer.new_generation_data(
                generation_number = i + 1,
                population = self._population
            )

            if i == self._number_of_generations - 1:
                continue

            new_population = []
            while len(new_population) != self._population_size - 2:
                first_individual = self._tournament_selection()
                second_individual = self._tournament_selection()

                crossover_return = self._crossover(
                    first_individual = first_individual,
                    second_individual = second_individual
                )

                if crossover_return:
                    new_population.append(crossover_return[0])
                    new_population.append(crossover_return[1])

            # Saves to elitism
            fittest_from_last_generation = self._population[0]
            mutated_fittest_from_last_generation = self._population[0]
            mutated_fittest_from_last_generation.individual_mutation()

            # Clears population list and defines a new population
            self._population.clear()
            self._population = new_population

            self._mutation()

            # Elitism includes the fittest from last generation and a mutation version of it
            new_population.append(fittest_from_last_generation)
            new_population.append(mutated_fittest_from_last_generation)

        self._data_visualizer.generate_files(
            number_of_generations = self._number_of_generations,
            population_size = self._population_size,
            probability_of_crossover = self._probability_of_crossover,
            probability_of_mutation = self._probability_of_mutation,
            tournament_parameter_N = self._tournament_parameter_N,
            tournament_parameter_K = self._tournament_parameter_K
        )