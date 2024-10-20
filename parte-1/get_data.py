"""This module contains the function to get the data from the input file."""

# read the file line by line and get the data into a dictionary
class DataExtractor:
    def __init__(self, input_file):
        self.data = self.read_file(input_file)
    # data = {"id": [ciclo, conflicto, movilidad, idhermano]}
    def read_file(self, input_file):
        data = {}
        with open(input_file) as file:
            # for each line, get the data separated by commas and store it in the dictionary
            for line in file:
                # split the line into a list of strings
                line = line.split(',')
                # get the data and store it in the dictionary
                data[line[0]] = [line[1], line[2], line[3], line[4].rstrip('\n')]
        return data
