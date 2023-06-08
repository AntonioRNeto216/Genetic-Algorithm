'''
File to define the Individual Class 
'''

# Python Imports
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

    def __str__(self) -> str:
        return_str = '---\n'
        for origin, start_time, end_time, price, destination in self._individual_data:
            return_str += f'FROM {origin} TO {destination} | START TIME: {start_time} | END TIME: {end_time} | PRICE: {price}\n'
        return_str += f'--> FITNESS: {self._individual_fitness_value}\n---\n'
        
        return return_str

    def _return_new_random_flight(self, origin: str, destination: str) -> list:
        start_time, end_time, price = random.choice(self._data[origin][destination])
        return [origin, start_time, end_time, price, destination]
    
    def individual_mutation(self) -> None:
        index_to_mutate = random.randint(0, 11)
        origin, _, _, _, destination = self._individual_data[index_to_mutate]

        self._individual_data[index_to_mutate] = self._return_new_random_flight(origin, destination)

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
