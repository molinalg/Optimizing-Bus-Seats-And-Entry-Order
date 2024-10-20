"""This module contains the code to execute the program from the terminal."""
import sys
from get_data import DataExtractor
from solver import CSPSolver
import random
# from parte1.problem_solver import solve_problem

def sort_dictionary(dictionary):
    """"""
    return dict(sorted(dictionary.items(), key = lambda x: x[1]))

if __name__ == "__main__":
    # prepare the input parameters
    if sys.argv[1] == "":
        raise Exception("Please provide an input file with the data of the students.")
    input_file = sys.argv[1]
    # read the file
    data_extractor = DataExtractor(input_file)
    data = data_extractor.data
    
    # solve the problem
    solver = CSPSolver(data)
    solutions = solver.returnResult()
    
    # get all the solutions into a list
    sols = []
    for dic in solutions:
        sols.append(sort_dictionary(dic))

    # get the keys (student identifications)
    keys = []
    for student in sols[0].keys():
        keys.append(student)
    
    # create a dictionary with the proper format for the solution
    resultados = []
    for element in sols:
        for student in keys:
            est = student + data[student][1] + data[student][2]
            valor = element[student]
            element[est] = valor
            element.pop(student)
        resultados.append(element)
    
    # write the solution to a file
    with open(input_file + ".output", "w") as f:
        f.write("Número de soluciones: " + str(len(sols)) + "\n")
        for i in range (1, 4):
            f.write(str(sols[random.randint(0,len(sols))]))
            f.write("\n")