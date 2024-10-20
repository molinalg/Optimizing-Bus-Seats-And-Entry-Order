"""This module contains the solver for parte2."""

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

class A_Star:
    def __init__(self, data, heuristic):
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.data = data
        self.heuristic = heuristic
        self.adjc_nodes = {}
        self.total_cost = 0
        self.expanded_nodes = 0
        self.length_initial_state = 0

    # ----------------------------------------------------
    # ------------------- ALGORITHM ----------------------
    # ----------------------------------------------------

    def a_star_algorithm(self, start, goal):
        """ A* algorithm """
        self.open_list.append(start)
        current = start
        self.length_initial_state = len(current.state)
        success = False
        
        while not success and self.open_list != []:
            current = self.get_cheapest_node(len(current.state))
            if current.state == goal.state or current.state == "":
                success = True
            else:
                self.generate_adjacents(current)
                self.closed_list.append(current)

        if success:
            self.define_path(current)
        else:
            self.path = []
    
    def get_cheapest_node(self, level):
        """ Sorts the open list by cost and returns the first available element """
        # sort the open list by cost
        self.open_list.sort(key=lambda x: x.f, reverse=False)
        
        # get the first available element
        for node in self.open_list:
            if len(node.state) <= level: # if the node is on the same level or lower than the current node
                self.open_list.remove(node)
                self.expanded_nodes += 1
                return node
            else: # remove the nodes that we are not going to use anymore
                self.open_list.remove(node)



    # ----------------------------------------------------
    # ------------------- HEURISTICS ---------------------
    # ----------------------------------------------------


    def h(self, node):
        if self.heuristic == "1":
            return self.h1(node)
        elif self.heuristic == "2":
            return  self.h2(node)

    def h1(self, node):
        """"""
        diff = self.difference_states(node.parent, node)
        h = 0.2
        if diff[1] == "C":
            h = node.state.count("C")*0.5
        if diff[2] == "R":
            h = node.state.count("R")*0.1
        return h*(node.state.count("-") + 1)

    def h2(self, node):
        """"""
        return (node.state.count("C")*0.2 + node.state.count("R")*0.1)*(node.state.count("-") + 1)

    # ----------------------------------------------------
    # --------------- AUXILIARY METHODS ------------------
    # ----------------------------------------------------

    def is_movred(self, state):
        return state[-1] == "R"

    def is_conflict(self, state):
        return state[-1] == "C"


    # ----------------GENERATE CHILDREN ------------------


    def generate_adjacents(self, node):
        students = node.state.split("-")
        self.adjc_nodes[node.state] = []

        for i in range(len(students)):
            new_state = ""
            if self.is_movred(students[i]) and len(students) > 1:
                if node.parent:
                    if not self.is_movred(self.difference_states(node.parent, node)): # only add MOVRED if there is more than one student and the previous one is not MOVRED
                        new_state = self.next_state(node, i)
                else:
                    new_state = self.next_state(node, i)
                if new_state != "not_possible":
                    self.add_child(node, new_state)
            elif not self.is_movred(students[i]):
                new_state = self.next_state(node, i)
                if new_state != "not_possible":
                    self.add_child(node, new_state)

    def next_state(self, state, index):
        students = state.state.split("-")
        new_state = ""
        for i in range(len(students)):
            if i != index:
                new_state += students[i] + "-"
        if len(new_state[:-1]) == 3 and self.is_movred(new_state[2]):
            return "not_possible"
        if new_state == "":
            return ""
        return new_state[:-1]

    def add_child(self, node, new_state):
        child = Node(new_state, node)
        self.set_cost(child)
        child.h = self.h(child)
        child.f = child.g + child.h

        self.adjc_nodes[node.state].append(child)
        if child not in self.open_list and child not in self.closed_list:
            self.open_list.append(child)
        for n in self.open_list:
            if n.state == child.state and n.f > child.f:
                self.open_list.remove(n)
                self.open_list.append(child)


    # -------------- PICKED STUDENT ----------------------


    def difference_states(self, state1, state2):
        """ Returns the student that has been already asignated between two states """
        old = state1.state.split("-")
        new = state2.state.split("-")
        i = 0
        while i in range(len(old)):
            # if there is an extra student or old and new differ, that is the selected student
            if i not in range(len(new)) or old[i] != new[i]:
                return old[i]
            i += 1
        return ""

    # ----------------- COSTS ----------------------------

    def set_cost(self, node):
        # reduced mobility students
        cost = self.mov_red_student(node)
        # previous student is conflictive
        if self.after_conflictive_student(node):
            cost *= 2
        # if seat of student is after a conflictive student, cost *= 2
        cost *= self.seat_after_conflictive(node)
        node.g = cost

    def mov_red_student(self, node):
        diff = self.difference_states(node.parent, node)
        if node.parent.parent:
            diff_p_p = self.difference_states(node.parent.parent, node.parent)
            # if student is helping a movred, cost = 0
            if self.is_movred(diff_p_p): 
                # the second student will never be movred, so we return the cost
                return 0
        # if student is movred, cost = 3
        if self.is_movred(diff):
            return 3
        return 1

    def after_conflictive_student(self, node):
        if node.parent.parent:
            diff_p_p = self.difference_states(node.parent.parent, node.parent)
            if self.is_conflict(diff_p_p):
                return True
        return False

    def seat_after_conflictive(self, node):
        cost = 1 # factor to multiply the cost of the student
        aux = node
        diff = self.difference_states(node.parent, node)
        while aux:
            if aux.parent:
                diff_aux = self.difference_states(aux.parent, aux)
                if diff_aux != "":
                    if self.is_conflict(diff_aux[1]) and self.data[diff_aux] < self.data[diff]: # if another student is conflictive and our student has a seat after him
                        cost *= 2
            aux = aux.parent
        return cost

    def conflictive_student(self, node):
        diff = self.difference_states(node.parent, node)
        if self.is_conflict(diff):
            node.parent.g *= 2 # we double the cost of the previous student
            # in case the previous student was helping a MOVRED, we double the cost of the MOVRED
            if node.parent.parent and node.parent.parent.parent:
                diff2 = self.difference_states(node.parent.parent.parent, node.parent.parent)
                if self.is_movred(diff2):
                    node.parent.parent.g *= 2


    # ----------------------------------------------------
    # ---------------- DEFINE THE PATH -------------------
    # ----------------------------------------------------


    def define_path(self, node):
        """Returns the path"""
        nodes = []
        while node.parent:
            nodes.append(node)
            self.conflictive_student(node)
            node = node.parent
        nodes.append(node)
        self.path = nodes[::-1]
        return self.path
    
    def print_path(self):
        """Returns a list with the order of the queue of our problem"""
        node = self.path[-1]
        to_print = []
        result = {}
        while node in self.path:
            if node.parent:
                to_print.append(self.difference_states(node.parent, node))
                self.total_cost += node.g
            node = node.parent
        to_print = to_print[::-1]
        for i in to_print:
            result[i] = self.data[i]
        return result