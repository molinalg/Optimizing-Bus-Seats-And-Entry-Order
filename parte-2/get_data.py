"""This module contains the function to get the data from the input file."""
import json
# read the file line by line and get the data into a dictionary
class DataExtractor:
    def __init__(self, input_file):
        self.data = self.read_file(input_file)
    def read_file(self, input_file):
        data = {}
        with open(input_file) as file:
            # for each line, get the data separated by commas and store it in the dictionary
            data_read = file.read()
            # replace ' by " to make it a valid json
            data_read = data_read.replace("'", '"')
            data = json.loads(data_read)
        file.close()
        return data
