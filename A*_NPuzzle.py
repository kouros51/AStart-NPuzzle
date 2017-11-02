#!/usr/bin/python
# -*- coding:latin1 -*-
import copy
import sys
import pdb


class Node:
    """Node definition"""

    def __init__(self, state, weight, child, parent):
        """Initiate the node default value"""
        self.state = state
        self.weight = weight
        self.child = child
        self.parent = parent

    def getNode(self):
        for i in range(len(self.state)):
            print("")
            for j in range(len(self.state)):
                if self.state[i][j] >= 10 or self.state[i][j] < 0:
                    print "|", self.state[i][j], "|",
                else:
                    print "| ", self.state[i][j], "|",
                pass
            pass
        pass
        print
        ""

    def manhattanDist(self):
        dist = []
        heuristic = 0
        for i in range(len(goal)):
            for j in range(len(goal)):
                if goal[i][j] < 0:
                    continue
                    pass
                for k in range(len(self.state)):
                    for l in range(len(self.state)):
                        if goal[i][j] == self.state[k][l]:
                            distance = abs(i - k) + abs(j - l)
                            dist.append(distance)
                            heuristic += distance
                            pass
                        pass
                    pass
                pass
            pass
        return heuristic

    def calculF(self):
        return self.weight + self.manhattanDist()

    def serachAdjNode(self):
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if self.state[i][j] == 0:
                    if i == 0:
                        if j == 0:
                            self.child = [[i, j + 1], [i + 1, j]]
                        elif j == len(self.state) - 1:
                            self.child = [[i, j - 1], [i + 1, j]]
                        else:
                            self.child = [[i, j - 1], [i + 1, j], [i, j + 1]]
                    elif i == len(self.state) - 1:
                        if j == 0:
                            self.child = [[i - 1, j], [i, j + 1]]
                        elif j == len(self.state) - 1:
                            self.child = [[i - 1, j], [i, j - 1]]
                        else:
                            self.child = [[i - 1, j], [i, j - 1], [i, j + 1]]
                    else:
                        if j == 0:
                            self.child = [[i - 1, j], [i, j + 1], [i + 1, j]]
                        elif j == len(self.state) - 1:
                            self.child = [[i - 1, j], [i, j - 1], [i + 1, j]]
                        else:
                            self.child = [[i - 1, j], [i, j - 1], [i, j + 1], [i + 1, j]]
                    pass
                    k = 0
                    while k < len(self.child):
                        if self.state[self.child[k][0]][self.child[k][1]] == -1:
                            self.child.remove(self.child[k])
                        else:
                            k += 1
                        pass
                    pass
                    return self.child
                pass
            pass
        pass

    def searchZero(self):
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if self.state[i][j] == 0:
                    return i, j

    def expandAdjNode(self):
        temp = []
        for i in range(len(self.child)):
            x, y = self.searchZero()
            temp.append(copy.deepcopy(self))
            temp[i].child = None
            temp[i].state[x][y] += temp[i].state[self.child[i][0]][self.child[i][1]]
            temp[i].state[self.child[i][0]][self.child[i][1]] -= temp[i].state[self.child[i][0]][self.child[i][1]]
            temp[i].parent = self
            temp[i].parent.child[i] = temp[i]
            temp[i].cout = self.weight + 1
        pass
        i = 0
        while i < len(temp):
            if temp[i].parent.parent != None and temp[i].parent.parent.state == temp[i].state:
                temp.remove(temp[i])
            i += 1
        pass
        return temp


class Solver:
    """This class impelement the searching process of the A* algorithm"""

    def __init__(self, goal):
        self.goal = goal
        self.openlst = []
        self.closedlst = []
        self.counter = 0
        self.backtrack = 0

    def addOpenLst(self, node):
        self.openlst.append(node)

    def addClosedLst(self, node):
        self.closedlst.append(node)

    def getOpenLst(self):
        print "Open list contain:"
        for i in range(len(self.openlst)):
            self.openlst[i].getNode()

    def getClosedLst(self):
        print "Closed set contain:"
        for i in range(len(self.closedlst) - 1):
            self.closedlst[i].getNode()
            if self.closedlst[i].calculF() > self.closedlst[i + 1].calculF() and self.closedlst[i].cout > \
                    self.closedlst[i + 1].cout:
                j = i
                while self.closedlst[j] != self.closedlst[i + 1].parent:
                    j -= 1
                    self.closedlst[j].getNode()
                pass
                self.backtrack += 1

        self.closedlst[len(self.closedlst) - 1].getNode()

    def removeFromOpenLst(self, node):
        self.openlst.remove(node)

    def removeFromClosedLst(self, node):
        self.closedlst.remove(node)

    def reorderOpenLst(self):
        self.openlst = sorted(self.openlst, key=lambda f: (f.calculF() - f.cout, -f.cout))

    def solve(self, puzzle):
        self.addOpenLst(puzzle)
        # pdb.set_trace()
        while self.openlst:
            condidat = self.openlst[0]
            self.counter += 1
            self.addClosedLst(condidat)
            condidat.serachAdjNode()
            expanded = condidat.expandAdjNode()
            expanded = sorted(expanded, key=lambda f: (f.calculF()))
            for each in expanded:
                inopen = 0
                inclosed = 0
                for openel in self.openlst:
                    if each.state == openel.state:
                        if each.cout < openel.cout:
                            openel = each
                        pass
                        inopen = 1
                    pass
                pass
                for closedel in self.closedlst:
                    if each.state == closedel.state:
                        self.addOpenLst(each)
                        self.removeFromClosedLst(closedel)
                        inclosed = 1
                    pass
                pass
                if inopen == 0 and inclosed == 0:
                    self.addOpenLst(each)
                pass
            pass
            self.removeFromOpenLst(self.openlst[0])
            self.reorderOpenLst()

            if self.closedlst[-1].state == goal:
                print "############################################"
                print "            Resolution Succeeded            "
                print "############################################"
                self.getClosedLst()
                print ""
                print "Nombre of moves ", self.counter
                print "Number of explored states", len(self.openlst) + len(self.closedlst)
                print "Backtracking move", self.backtrack
                print ""
                print "Sixth step since it starts"
                self.closedlst[6].getNode()
                print ""
                print "Sixth step before resolution"
                self.closedlst[len(self.closedlst) - 7 - self.backtrack].getNode()
                sys.exit(0)
            pass
        print "failure", sys.exit(1)


initial = [[2, 3, 7, 4, 5],
           [1, -1, 11, -1, 8],
           [6, 10, 0, 12, 15],
           [9, -1, 14, -1, 20],
           [13, 16, 17, 18, 19]]
goal = [[1, 2, 3, 4, 5],
        [6, -1, 7, -1, 8],
        [9, 10, 0, 11, 12],
        [13, -1, 14, -1, 15],
        [16, 17, 18, 19, 20]]


def main():
    print "N-puzzle Solver Using A*"
    print "###############################################"
    print ""
    puzzle = Node(initial, 0, None, None)
    print "Resolving the puzzle:"
    puzzle.getNode()
    print "Empty cell coordinate", puzzle.searchZero()
    print ""
    print "###############################################"
    print ""
    print ""

    solver = Solver(goal)
    solver.solve(puzzle)
    print ""


if __name__ == '__main__':
    main()
