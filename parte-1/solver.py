"""This module contains the Solver Class for the CSP problem."""
from constraint import *

class CSPSolver:
    def __init__(self,data):
        # data with the information of the students
        self.data = data
        # list of the IDs of the students
        self.students = self.define_students()
        # problem creation
        self.problem = Problem()

        self.create_variables()

        # everyone has to have a different seat assigned
        self.problem.addConstraint(AllDifferentConstraint(),self.students)
        self.problem.addConstraint(self.everyoneSeated, self.students)

        # seat the students in their corresponding section
        self.assignateSection()
        for iD_A, data_A in self.data.items():
            if data_A[1] == "C":
                self.conflictivePartner(iD_A)
            if data_A[2] == 'R':
                self.reducedMobility(iD_A)

        self.solutions = self.problem.getSolutions()
    
    # ---------------- GET DATA AND CREATE VARIABLES ----------------

    def define_students(self):
        """ Write the students' data into a dictionary"""
        students = []
        for student in self.data:
            students.append(student)
        return students
    
    def create_variables(self):
        """Create the variables"""
        # variables are the students' IDs -> value is the assigned seat
        for i in self.students:
            self.problem.addVariable(str(i), range(1,33))
    
    # ------------------- FUNCTIONS FOR THE CONSTRAINTS -------------------
    def assignateSection(self):
        for iD in self.students:
            if self.data[iD][3] == '0': # no brothers
                self.assignateCycle(iD, self.data[iD][0])
            else: # with brothers
                movred = self.brothersWithReducedMobility(iD, self.data[iD][3])
                conflictive = self.conflictiveBrothers(iD, self.data[iD][3])
                # if no more restrictions are involved, seat them in their cycle
                if not movred and not conflictive:
                    self.seatBrothers(iD, self.data[iD][3])

    def conflictivePartner(self,student):
        """ Conflictive students can't be seated close to reduced mobility students unless they are brothers"""
        for iD, data in self.data.items():
            if (data[1] == "C" or data[2] == "R") and student != iD and self.data[student][3] != iD: # alejado de cualquier conf excepto si es su hermano, que estaría al lado
                self.problem.addConstraint(self.notClose,(str(student),str(iD)))

    # all the students have to be seated
    def everyoneSeated(self, *args):
        """ Seats of the students are in the domain"""
        return all(student in range(1,33) for student in args)
    
    # reduced mobility students will have special seats
    def reducedMobility(self,student):
        """Reduced mobility students are in their domain and no one seats next to them"""
        self.problem.addConstraint(self.reducedMobilityDomain,[student])
        for iD in self.students:
            self.problem.addConstraint(self.notTogether,[student,iD])

    def reducedMobilityDomain(self,student):
        """ Reduced mobility domain """
        return student in [1,2,3,4,13,14,15,16,17,18,19,20]
    
    def notTogether(self,a,b):
        """There is only one occupied seat between reduced mobility students"""
        if (a % 2 == 0 and a == b + 1) or (a % 2 != 0 and a == b - 1):
            return False
        return True

    def notClose(self,a,b):
        """ A student is not close to another one """
        # window even seats
        dom_vent_par = [4,8,12,16,20,24,28,32]
        # aisle even seats
        dom_pas_par = [2,6,10,14,18,22,26,30]
        # window odd seats
        dom_vent_impar = [1,5,9,13,17,21,25,29]
        # aisle odd seats
        dom_pas_impar = [3,7,11,15,19,23,27,31]

        # seats in front and behind
        if a == b + 4 or a == b - 4:
            return False

        # seats in the same row (the next three conditions )
        if a in dom_vent_par:
            if b + 1 == a or b - 3 == a or b + 5 == a:
                return False

        elif a in dom_vent_impar:
            if b - 1 == a or b - 5 == a or b + 3 == a:
                return False

        elif a in dom_pas_par or a in dom_pas_impar:
            if b + 1 == a or b - 1 == a or b - 3  == a or b - 5  == a or b + 3  == a or b + 5  == a:
                return False

        return True
    
    def seatBrothers(self, a, b):
        """ Seat brothers depending on the cycle they are in """
        if self.data[a][0] == self.data[b][0]: # mismo ciclo
            self.assignateCycle(a, self.data[a][0])
            self.assignateCycle(b, self.data[b][0])
            
            self.problem.addConstraint(self.sameCycle,[a,b])
            
        else:
            self.assignateCycle(a, '1')
            self.assignateCycle(b, '1')
            
            if self.data[a][0] == '2':
                self.problem.addConstraint(self.differentCycles, (str(a),str(b)))
            else:
                self.problem.addConstraint(self.differentCycles, (str(b),str(a)))

    def assignateCycle(self, student, cycle):
        """Add constraints to the students depending on their cycle"""
        if cycle == '1':
            self.problem.addConstraint(self.firstCycle,[student])
        if cycle == '2':
            self.problem.addConstraint(self.secondCycle,[student])
                
    def firstCycle(self,student):
        """ Domain for first cycle students"""
        return student in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

    def secondCycle(self,student):
        """ Domain for second cycle students"""
        return student in [17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    
    def sameCycle(self, a, b):
        """ They will seat together """
        if a % 2 == 0:
            return a == b + 1
        return a == b - 1

    def differentCycles(self, a, b):
        """ Bigger brother will be on the aisle """
        if ((b) % 4 == 0):
            return b == a + 1
        return (a % 2 == 0 and b == (a - 1))

    def brothersWithReducedMobility(self, a, b):
        # if only one of the brothers has reduced mobility
        if self.data[a][2] == 'R' and self.data[b][2] != 'R':
            self.assignateCycle(a, self.data[a][0])
            self.assignateCycle(b, self.data[a][0])
            return True
        elif self.data[b][2] == 'R' and self.data[a][2] != 'R':
            self.assignateCycle(a, self.data[b][0])
            self.assignateCycle(b, self.data[b][0])
            return True
        # if both have reduced mobility
        elif self.data[a][2] == 'R' and self.data[b][2] == 'R':
            if self.data[a][0] == self.data[b][0]:
                self.assignateCycle(a, self.data[a][0])
                self.assignateCycle(b, self.data[b][0])
            else:
                self.assignateCycle(a, '1')
                self.assignateCycle(b, '1')
            return True
        # none of them has reduced mobility
        else:
            return False
    
    def conflictiveBrothers(self, a, b):
        """ Conflictive brothers seat together """
        if self.data[a][1] == 'C' and self.data[b][1] == 'C':
            if self.data[a][0] == self.data[b][0]: # mismo ciclo
                self.assignateCycle(a, self.data[a][0])
                self.assignateCycle(b, self.data[b][0])
            else:
                self.assignateCycle(a, '1')
                self.assignateCycle(b, '1')
            self.problem.addConstraint(self.sameCycle, (a, b))
            return True
        return False

    # ------------------- RESULTS -------------------
    def returnResult(self):
        return self.solutions