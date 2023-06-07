import random
import typing


class Individual:

    def __init__(self, data: dict, parents_individual_data_definition: typing.Union[typing.Tuple[typing.List[typing.List[str]]], None]) -> None:
        self._data = data
        self._individual_data = [
            self._return_new_random_flight(origin='LIS', destination='FCO'),
            self._return_new_random_flight(origin='FCO', destination='LIS'),

            self._return_new_random_flight(origin='MAD', destination='FCO'),
            self._return_new_random_flight(origin='FCO', destination='MAD'),

            self._return_new_random_flight(origin='CDG', destination='FCO'),
            self._return_new_random_flight(origin='FCO', destination='CDG'),
            
            self._return_new_random_flight(origin='DUB', destination='FCO'),
            self._return_new_random_flight(origin='FCO', destination='DUB'),

            self._return_new_random_flight(origin='BRU', destination='FCO'),
            self._return_new_random_flight(origin='FCO', destination='BRU'),

            self._return_new_random_flight(origin='LHR', destination='FCO'),
            self._return_new_random_flight(origin='FCO', destination='LHR')
        ] if not parents_individual_data_definition else [
            *parents_individual_data_definition[0],
            *parents_individual_data_definition[1]
        ]

    def _return_new_random_flight(self, origin: str, destination: str) -> list:
        start_time, end_time, price = random.choice(self._data[origin][destination])
        return [origin, start_time, end_time, price, destination]
    
    def individual_mutation(self) -> None:
        index_to_mutate = random.randint(0, 11)
        origin, _, _, _, destination = self._individual_data[index_to_mutate]

        self._individual_data[index_to_mutate] = self._return_new_random_flight(origin, destination)
        # self.update_fitness_value()

    def update_fitness_value(self) -> None:
        hours_to_minutes = lambda hour_str, minute_str : int(hour_str) * 60 + int(minute_str)

        self._individual_fitness_value = 0
        for flight in self._individual_data:
            origin, start_time, end_time, price, _ = flight

            # Hours to minutes
            start_time = hours_to_minutes(*start_time.split(':'))
            end_time = hours_to_minutes(*end_time.split(':'))

            # Price
            price = int(price)

            self._individual_fitness_value += start_time + price if origin == 'FCO' else end_time + price
    
    def return_fitness_value(self) -> int:
        return self._individual_fitness_value
    
    def return_a_piece_of_individual_data(self, start_index: int, end_index: int) -> typing.List[typing.List[str]]:
        return self._individual_data[start_index:end_index] if end_index != -1 else self._individual_data[start_index:]
    
    def return_individual_data(self) -> typing.List[typing.List[str]]:
        return self._individual_data

class GeneticAlgorithm:

    def __init__(self) -> None:
        self._define_parameters_and_attributes()
        self._generates_database()

    def _define_parameters_and_attributes(self) -> None:
        self._data = {}
        self._population = []

        self._number_of_generations = 100       #TODO low_number < N < high_number
        self._population_size = 100             #TODO low_number < N < high_number
        self._probability_of_crossover = 0.5    #TODO 0 < p < 1
        self._probability_of_mutation = 0.05    #TODO 0 < p < 1
        self._tournament_parameter_N = 5        #TODO N > 0
        self._tournament_parameter_K = 0.75     #TODO 0 <= K <= 1

    def _generates_database(self) -> None:
        with open('flights.txt', 'r') as file:
            for line in file.readlines():
                origin, destination, start_time, end_time, value = line.replace('\n', '').split(',')
            
                if origin not in self._data:
                    self._data[origin] = {}
                
                if destination not in self._data[origin]:
                    self._data[origin][destination] = []

                self._data[origin][destination].append((start_time, end_time, value))
        
    def _define_new_population(self) -> None:
        for _ in range(self._population_size):
            self._population.append(Individual(self._data, None))

    def _fitness_function_for_all_population(self) -> None:
        for individual in self._population:
            individual.update_fitness_value()

    def _tournament_selection(self) -> Individual:
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
        for individual in self._population:
            mutate = random.randint(0, 100) / 100 < self._probability_of_mutation

            if mutate:
                individual.individual_mutation()

    def _visualize_data(self, generation_number: int) -> None:
        print('---')
        print(f'Generation number: {generation_number}')

        # Sort population
        self._population.sort(
            key = lambda individual : individual.return_fitness_value()
        )

        print(f'Better Schedule: {self._population[0].return_individual_data()}')
        print(f'Fitness value: {self._population[0].return_fitness_value()}')

        #TODO save values to plot graphs

    def execute(self) -> None:
        self._define_new_population()
        for i in range(self._number_of_generations):
            
            self._fitness_function_for_all_population()
            self._visualize_data(
                generation_number = i
            )

            new_population = []
            while len(new_population) != self._population_size:
                first_individual = self._tournament_selection()
                second_individual = self._tournament_selection()

                crossover_return = self._crossover(
                    first_individual = first_individual,
                    second_individual = second_individual
                )

                if crossover_return:
                    new_population.append(crossover_return[0])
                    new_population.append(crossover_return[1])

            # Clears population list and defines a new population
            self._population.clear()
            self._population = new_population

            self._mutation()

        # Needs to update fitness values for last generation and after show results
        self._fitness_function_for_all_population() 
        self._visualize_data(
            generation_number = self._number_of_generations
        )


if __name__ == '__main__':
    genetic_algorithm = GeneticAlgorithm()
    genetic_algorithm.execute()
