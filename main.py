import tkinter
from tkinter import *
from tkinter.ttk import *


class AStar:

    def __init__(self, initial_puzzle, heuristic="H1"):
        #  initial_puzzle: Starting state
        self.num_expanded_nodes = 0
        self.solution = None

        self.start = initial_puzzle
        self.heuristic = heuristic

    @staticmethod
    def _calculate_new_heuristic(move, end_node):
        return move.heuristic_wrong_placed() - end_node.heuristic_wrong_placed()

    @staticmethod
    def _calculate_new_heuristic_manhattan(move, end_node):
        return move.heuristic_manhattan_distance() - end_node.heuristic_manhattan_distance()

    def __str__(self):
        if self.heuristic == "H2":
            return 'A Star (A*) using Manhattan Heuristic'
        else:
            return 'A Star (A*) using miss placed Heuristic'

    def run_algorithm(self):
        if self.heuristic == "H2":
            queue = [[self.start.heuristic_manhattan_distance(), self.start]]
        else:
            queue = [[self.start.heuristic_wrong_placed(), self.start]]
        expanded = []
        num_expanded_nodes = 0
        path = None

        while queue:
            i = 0
            for j in range(1, len(queue)):
                if queue[i][0] > queue[j][0]:  # minimum
                    i = j

            path = queue[i]
            queue = queue[:i] + queue[i + 1:]
            end_node = path[-1]

            if end_node.position == end_node.PUZZLE_END_POSITION:
                break
            if end_node.position in expanded:
                continue

            for move in end_node.get_moves():
                if move.position in expanded:
                    continue
                if self.heuristic == "H2":
                    new_path = [path[0] + self._calculate_new_heuristic_manhattan(move, end_node)] + path[1:] + [move]
                else:
                    new_path = [path[0] + self._calculate_new_heuristic(move, end_node)] + path[1:] + [move]
                queue.append(new_path)
                expanded.append(end_node.position)

            num_expanded_nodes = num_expanded_nodes + 1

        self.num_expanded_nodes = num_expanded_nodes
        self.solution = path[1:]


class BreadthFirst:

    def __init__(self, initial_puzzle):
        self.start = initial_puzzle
        self.num_expanded_nodes = 0
        self.solution = None

    def __str__(self):
        return 'Breadth First'

    def run_algorithm(self):

        queue = [[self.start]]
        expanded = []
        num_expanded_nodes = 0
        path = None

        while queue:
            path = queue[0]
            queue.pop(0)  # dequeue (FIFO)
            end_node = path[-1]

            if end_node.position in expanded:
                continue

            for move in end_node.get_moves():
                if move.position in expanded:
                    continue
                queue.append(path + [move])  # add new path at the end of the queue

            expanded.append(end_node.position)
            num_expanded_nodes += 1

            if end_node.position == end_node.PUZZLE_END_POSITION:
                break

        self.num_expanded_nodes = num_expanded_nodes
        self.solution = path


class Puzzle:
    def __init__(self, position):
        self.position = position  # puzzle matrix
        self.rows = len(position)
        self.columns = len(position[0])
        self.PUZZLE_END_POSITION = self.generate_goal_state()

    def __str__(self):
        """
        Print in console as a matrix
        """
        puzzle_string = '—' * 13 + '\n'
        for i in range(self.rows):
            for j in range(self.columns):
                puzzle_string += '│{0: >2}'.format(str(self.position[i][j]))
                if j == self.columns - 1:
                    puzzle_string += '│\n'

        puzzle_string += '—' * 13 + '\n'
        return puzzle_string

    def generate_goal_state(self):

        #  In 4x4 puzzle the Goal state will be like this :
        #  [ [1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0 ]]

        goal_matrix = []
        _row = []

        for i in range(0, self.rows * self.columns):
            _row.append(i + 1)
            if len(_row) == self.columns:
                goal_matrix.append(_row)
                _row = []

        goal_matrix[-1][-1] = 0
        return goal_matrix

    def swap(self, x1, y1, x2, y2):

        #  Swap the positions between two numbers
        puzzle_clone = [list(row) for row in self.position]  # copy the puzzle
        puzzle_clone[x1][y1], puzzle_clone[x2][y2] = puzzle_clone[x2][y2], puzzle_clone[x1][y1]

        return puzzle_clone

    def get_blank_space_row(self):
        blank_space_row, _ = self.get_coordinates(0)  # blank space
        return self.rows - blank_space_row

    def get_coordinates(self, number, matrix=None):
        # Returns  x, y coordinates for a given number
        if not matrix:
            matrix = self.position
        for x in range(self.rows):
            for y in range(self.columns):
                if matrix[x][y] == number:
                    return x, y
        print('Invalid number value')

    def heuristic_wrong_placed(self):
        #  Counts the number of misplaced tiles
        number_wrong_places = 0
        for x in range(self.rows):
            for y in range(self.columns):
                if self.position[x][y] != self.PUZZLE_END_POSITION[x][y]:
                    number_wrong_places = number_wrong_places + 1
        return number_wrong_places

    def heuristic_manhattan_distance(self):
        """
        Counts how much is a tile misplaced from the original position
        """
        distance = 0
        for i in range(self.rows):
            for j in range(self.columns):
                i1, j1 = self.get_coordinates(self.position[i][j], self.PUZZLE_END_POSITION)
                distance += abs(i - i1) + abs(j - j1)
        return distance

    def get_moves(self):

        #  Returns a list of all the possible moves
        moves = []
        x, y = self.get_coordinates(0)  # blank space

        if x > 0:
            moves.append(Puzzle(self.swap(x, y, x - 1, y)))  # move up

        if y < self.columns - 1:
            moves.append(Puzzle(self.swap(x, y, x, y + 1)))  # move right

        if y > 0:
            moves.append(Puzzle(self.swap(x, y, x, y - 1)))  # move left

        if x < self.rows - 1:
            moves.append(Puzzle(self.swap(x, y, x + 1, y)))  # move down

        return moves


class Main:
    def __init__(self, parent):
        self.parent = parent
        self.mainFrame = Frame(self.parent)
        self.board = Frame(self.parent)
        self.winFrame = Frame(self.parent)
        frame = Frame(self.mainFrame)
        self.
        #Label(self.mainFrame,text="15 Puzzle",font=("", 50)).pack(padx=10, pady=10)
        self.mainFrame.pack()



if __name__ == '__main__':
    # puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [10, 0, 11, 12], [9, 13, 14, 15]])
    puzzle = Puzzle([[1, 3, 6], [5, 7, 8], [2, 0, 4]])
    p = AStar(puzzle, "H2")
    # p = BreadthFirst(puzzle)
    p.run_algorithm()
    print('Solution:')
    for s in p.solution:
        print(s)
    print(f'{p} - Expanded Nodes: {p.num_expanded_nodes}')
    root = Tk()
    Main(root)
    root.mainloop()



