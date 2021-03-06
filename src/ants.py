import math
import random

class Ant():
    def __init__(self, ID, start_node, colony):
        self.ID = ID
        self.start_node = start_node
        self.grouping = colony
        self.curr_node = self.start_node
        self.graph = self.grouping.graph
        self.path_vec = []
        self.path_vec.append(self.start_node)
        self.path_cost = 0
        self.Beta = 1.0
        self.Q0 = 0.5
        self.Rho = 0.99
        self.UnexploredNodes = {}
        for i in range(0, self.graph.numNodes):
            if i != self.start_node:
                self.UnexploredNodes[i] = i
        self.path_mat = []
        for i in range(0, self.graph.numNodes):
            self.path_mat.append([0] * self.graph.numNodes)

    def run(self):
        graph = self.grouping.graph
        while not self.end():
            new_node = self.state_transition_rule(self.curr_node)
            self.path_cost += graph.delta(self.curr_node, new_node)
            self.path_vec.append(new_node)
            self.path_mat[self.curr_node][new_node] = 1 
            self.local_updating_rule(self.curr_node, new_node)
            self.curr_node = new_node
        self.path_cost += graph.delta(self.path_vec[-1], self.path_vec[0])
        self.grouping.update(self)
        self.__init__(self.ID, self.start_node, self.grouping)

    def end(self):
        return not self.UnexploredNodes

    def state_transition_rule(self, curr_node):
        graph = self.grouping.graph
        q = random.random()
        max_node = -1
        if q < self.Q0:
            max_val = -1
            val = None
            for node in self.UnexploredNodes.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")
                val = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if val > max_val:
                    max_val = val
                    max_node = node
        else:
            sum = 0
            node = -1
            for node in self.UnexploredNodes.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")
                sum += graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
            if sum == 0:
                raise Exception("sum = 0")
            avg = sum / len(self.UnexploredNodes)
            for node in self.UnexploredNodes.values():
                p = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if p > avg:
                    max_node = node
            if max_node == -1:
                max_node = node
        if max_node < 0:
            raise Exception("The next node could not be found. Please check that tau * etha^beta is a positive number and try again")
        del self.UnexploredNodes[max_node]
        return max_node

    def local_updating_rule(self, curr_node, next_node):
        # Update the pheromones on the tau matrix to represent transitions of the ants
        graph = self.grouping.graph
        val = (1 - self.Rho) * graph.tau(curr_node, next_node) + (self.Rho * graph.tau0)
        graph.update_tau(curr_node, next_node, val)