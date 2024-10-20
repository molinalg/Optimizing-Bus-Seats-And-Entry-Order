"""This module contains the code to execute parte2 from the terminal."""
import sys
from get_data import DataExtractor
from solver import A_Star, Node
import time

if __name__ == "__main__":
    
    # get the input file
    if len(sys.argv) != 3:
        raise Exception("Please provide an input file with the data of the students and specify the heuristic function to be used.")
    input_file = sys.argv[1]
    heuristic = sys.argv[2]

    # extract the data
    data_extractor = DataExtractor(input_file)
    data = data_extractor.data
    
    # check the input parameters
    if data == {}:
        raise Exception("The input file is empty.")
    if heuristic not in ["1", "2", "3"]:
        raise Exception("The heuristic function must be 1, 2 or 3.")

    # prepare nodes START and END
    initial_state = ""
    for student in data.keys():
        initial_state += student + "-"
    start = Node(initial_state[:-1])
    start.g = 0
    end = Node("")
    
    # perform the solution
    solver = A_Star(data, heuristic)
    
    timer_start = time.time()
    solver.a_star_algorithm(start, end)
    timer_end = time.time()
    
    total_time = str((timer_end - timer_start) * 1000)
    # 5 decimals
    total_time = total_time[:total_time.find(".")+6]
    total_time += " ms"

    # get the solution in form of dictionary[student] = seat
    order = solver.print_path()
    if len(order) != len(data):
        order = "No solution found."
        
    # write the solution in the output file
    name = input_file.split(".")
    result = "." + name[1] + "-" + heuristic + ".output"
    with open(result, "w") as f:
        f.write("INICIAL: " + str(data) + "\nFINAL: " + str(order))
    f.close()
    
    # write statistics of the execution
    stat = "." + name[1] + "-" + heuristic + ".stat"
    with open(stat, "w") as file:
        file.write("Tiempo total: " + str(total_time) + "\nCoste total: " + str(solver.total_cost) + "\nLongitud del plan: " + str(len(order)) + "\nNodos expandidos: " + str(solver.expanded_nodes))
    file.close()