import numpy as np
import math

class Node:
    def __init__(self, state, g_score, h_score):
        self.state = state
        self.g_score = g_score
        self.f_score = g_score + h_score
        
class NPuzzle:
    def __init__(self, n, puzzle): #puzzle is 2-d array and its our initial state
        self.n = n
        self.goal_state = np.arange(1, n)
        self.goal_state = np.append(self.goal_state, 0)
        self.goal_state = self.goal_state.reshape(int(math.sqrt(n)), int(math.sqrt(n)))
        
        h_score = 0
        
        for element in range(1, self.n):
            i_goal, j_goal = np.where(self.goal_state == element)
            i_goal, j_goal = int(i_goal), int(j_goal)
            
            i_current_node, j_current_node = np.where(puzzle == element)
            i_current_node, j_current_node = int(i_current_node), int(j_current_node)
            
            h_score += abs(i_goal - i_current_node)
            h_score += abs(j_goal - j_current_node)
        
        self.root = Node(puzzle, 0, h_score)     
        self.frontier = []
        self.explored = []
        self.frontier.append(self.root)

    def estimate_h_score(self, node):
        h_score = 0

        for element in range(1, self.n):
            i_goal, j_goal = np.where(self.goal_state == element)
            i_goal, j_goal = int(i_goal), int(j_goal)
            
            i_current_node, j_current_node = np.where(node == element)
            i_current_node, j_current_node = int(i_current_node), int(j_current_node)
            
            h_score += abs(i_goal - i_current_node)
            h_score += abs(j_goal - j_current_node)
        return h_score    
    
    def move_right(self, node):
        i, j = np.where(node == 0)
        i, j = int(i), int(j)
        
        if j != math.sqrt(self.n) - 1:
            node[i][j], node[i][j+1] = node[i][j+1], node[i][j]
            return node
        result = np.array([])
        return result     

    def move_left(self, node):
        i, j = np.where(node == 0)
        i, j = int(i), int(j)
        
        if j != 0:
            node[i][j], node[i][j-1] = node[i][j-1], node[i][j]
            return node
        result = np.array([])
        return result  

    def move_up(self, node):
        i, j = np.where(node == 0)
        i, j = int(i), int(j)
        
        if i != 0:
            node[i][j], node[i-1][j] = node[i-1][j], node[i][j]
            return node
        result = np.array([])    
        return result  

    def move_down(self, node):
        i, j = np.where(node == 0)
        i, j = int(i), int(j)
        
        if i != math.sqrt(self.n) - 1:
            node[i][j], node[i+1][j] = node[i+1][j], node[i][j]
            return node
        result = np.array([])    
        return result 

    def update_priority(self, state, p):
        for i in range(len(self.explored)):
            if (state == self.explored[i].state).all() and self.explored[i].f_score > p:
                self.explored[i].f_score = p
                return 
        return 

    def solve_using_a_star(self):
        while len(self.frontier) > 0:
            self.frontier.sort(key= lambda x: x.f_score) 
            node = self.frontier.pop(0)
            print(node.state)
            print('---------')
            
            comparison = node.state == self.goal_state                          
            
            if comparison.all():
                print(node.state)
                print("puzzle solved")
                return
            
            self.explored.append(node)
            
            moves = [self.move_down, self.move_up, self.move_left, self.move_right]
            state = np.copy(node.state)
    
            for move in moves:
                state = np.copy(node.state)
                child_state = move(state)
                if child_state.size == 0:
                    continue
                    
                child = Node(child_state, node.g_score + 1, self.estimate_h_score(child_state))
                if  not any((x.state == child.state).all() for x in self.frontier) and not any((x.state == child.state).all() for x in self.explored) :
                    self.frontier.append(child)
                    
                elif any((x.state == child.state).all() for x in self.explored):
                    self.update_priority(child.state, child.f_score)                   

idk = NPuzzle(16, np.array([[1, 2, 3, 0], [5, 6 , 7, 8], [9, 10, 11, 12], [13, 14, 15, 4]]))
idk.solve_using_a_star()



