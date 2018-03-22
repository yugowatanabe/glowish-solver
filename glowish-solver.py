#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# initialize graph of shapes and of states (global)
shapeG = nx.Graph()
stateG = nx.Graph()

def main():
    # fill in graph of shapes from user file, updates global var
    getShapeG("puzzleShapes.txt")

    # starting state, all values 0
    state = tuple([0] * shapeG.number_of_nodes())
    stateG.add_node(state)

    # explore all paths between possible states, build graph
    getStateG(state)

    # find shortest path in state graph from beginning to end state
    start = tuple([0] * shapeG.number_of_nodes())
    end   = tuple([1] * shapeG.number_of_nodes())
    statePath = nx.shortest_path(stateG, source=start, target=end)

    # get nodes that must be pressed to follow statePath
    shapePath = getShapePath(statePath)

    # print out more human-readable answer
    printAnswer(shapePath)

    # save_graph(shapeG)

    return 0

# add nodes and edges
def getShapeG(filename):
    f = open(filename)                  # open user input
    color = None
    shape = None
    blank = None

    # create nodes
    nodeId = 0
    while(1):
        color = f.read(1)               # read in color char
        if not color:
            break
        shape = f.read(1)               # read in shape char
        if not shape:
            break
        blank = f.read(1)
        if not shape:
            break

        shapeG.add_node(nodeId, color=color, shape=shape, value=0)
        nodeId += 1

    # add edges between nodes sharing attributes
    for node1, attributes1 in shapeG.nodes(data=True):
        for node2, attributes2 in shapeG.nodes(data=True):
            if node2 != node1 \
            and shapeG.has_edge(node1, node2) == 0\
            and (attributes2['shape'] == attributes1['shape'] \
            or   attributes2['color'] == attributes1['color']):
                shapeG.add_edge(node2, node1, weight=1)

    return 0

# Gets resulting state from pressing specific node when in specific state
def newState(prevState, node):
    newState = list(prevState)                          # mutable copy
    connectedTo = [n for n in shapeG.neighbors(node)]   # nodes pressed node connected to
    connectedTo.append(node)
    for n in connectedTo:
        newState[n] = 1 - prevState[n]                  # flip value

    return tuple(newState)

# get state-space and connection between states (as a graph)
def getStateG(state):
    # LIFO queue of states which still have state paths to analyze
    queue = list([state])
    q_len = 1
    statelen = len(state)

    db = 0
    # We exhaust all possible states when queue is empty
    while q_len != 0:
        state = queue.pop()                         # get last state into queue
        q_len -= 1
        for i in range(statelen):                   # for each node making up state
            newstate = newState(state, i)           # get new state from pressing it
            if newstate not in stateG.nodes:        # if state not seen before
                stateG.add_node(newstate)           # create node for it
                stateG.add_edge(state, newstate, weight=1, node=i)    # create edge from prev to new
                queue.append(newstate)              # add new state to queue
                q_len += 1
            else:   # if state seen before (is already in queue, perhaps already connected)
                if stateG.has_edge(state, newstate) == 0:   # if no edge connecting them
                    stateG.add_edge(state, newstate, weight=1, node=i)    # create an edge

    return 0

# get nodes path from state path
def getShapePath(statePath):
    shapePath = []
    for i in range(len(statePath)-1):
        shapePath.append(stateG.get_edge_data(statePath[i],statePath[i+1])['node'])

    return shapePath

# print out printAnswer
def printAnswer(shapePath):
    print("\nShortest sequence to solve puzzle:\n")

    for i in range(len(shapePath)):
        color = shapeG.nodes.data('color')[shapePath[i]]
        shape = shapeG.nodes.data('shape')[shapePath[i]]

        if color == "P":
            print("Purple", end=" ")
        elif color == "Y":
            print("Yellow", end=" ")
        elif color == "K":
            print("Pink", end=" ")
        elif color == "G":
            print("Green", end=" ")
        elif color == "B":
            print("Blue", end=" ")
        elif color == "R":
            print("Red", end=" ")

        if shape == "T":
            print("triangle")
        elif shape == "C":
            print("circle")
        elif shape == "S":
            print("square")

    return 0

# save a networkx graph as a .pdf
def save_graph(graph):
     print("Saving graph as PDF in current directory")

     plt.figure(num=None, figsize=(50, 50), dpi=80)
     plt.axis('off')
     fig = plt.figure(1)
     pos = nx.spring_layout(graph)
     nx.draw_networkx_nodes(graph,pos)
     nx.draw_networkx_edges(graph,pos)

     cut = 1.30
     xmax = cut * max(xx for xx, yy in pos.values())
     ymax = cut * max(yy for xx, yy in pos.values())
     plt.xlim(-xmax, xmax)
     plt.ylim(-ymax, ymax)

     plt.savefig("GlowStatesGraph.pdf",bbox_inches="tight")
     del fig

if __name__ == "__main__":
    main()
