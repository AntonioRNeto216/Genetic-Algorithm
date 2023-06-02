import random


class Individual:

    def __init__(self, data: dict) -> None:
        self._data = data
        self._individual_fitness_value = 0
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
        ]

    def _return_new_random_flight(self, origin: str, destination: str) -> list:
        start_time, end_time, price = random.choice(self._data[origin][destination])
        return [origin, start_time, end_time, price, destination]
    
    def individual_mutation(self) -> None:
        index_to_mutate = random.randint(0, 11)
        origin, _, _, _, destination = self._individual_data[index_to_mutate]

        self._individual_data[index_to_mutate] = self._return_new_random_flight(origin, destination)
        self.update_fitness_value()

    def update_fitness_value(self) -> None:
        self._individual_fitness_value = 0
        for flight in self._individual_data:
            origin, start_time, end_time, price, _ = flight
            self._individual_fitness_value += start_time + price if origin == 'FCO' else end_time + price
    

class GeneticAlgorithm:

    def __init__(self) -> None:
        self._define_parameters_and_attributes()
        self._generates_database()

    def _define_parameters_and_attributes(self) -> None:
        self._data = {}
        self._population = []

        self._number_of_generations = 100       #TODO low_number < N < high_number
        self._population_size = 10              #TODO low_number < N < high_number
        self._probability_of_crossover = 0.5    #TODO 0 < p < 1
        self._probability_of_mutation = 0.05    #TODO 0 < p < 1
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
            self._population.append(Individual(self._data))

    def _fitness_function(self) -> None:
        for individual in self._population:
            individual.update_fitness_value()

    def _tournament_selection(self) -> None:
        pass

    def _crossover(self) -> None:
        pass

    def _mutation(self) -> None:
        for individual in self._population:
            mutate = random.randint(0, 100) / 100 < self._probability_of_mutation

            if mutate:
                individual.individual_mutation()

    def execute(self) -> None:
        self._define_new_population()
        for i in range(self._number_of_generations):

            print(f'Generation number: {i}')


if __name__ == '__main__':
    genetic_algorithm = GeneticAlgorithm()
    genetic_algorithm.execute()
