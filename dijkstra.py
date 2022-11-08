#!/usr/bin/env python3
import math


class Path:
    def __init__(self,node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def display(self):
        if self.weight != math.inf:
            return "{name1},{name2},{weight}".format(name1= self.node1,name2=self.node2,weight=self.weight)

    def get_weight(self,name):
        if name == self.node1:
            return (self.node2,self.weight)
        if name == self.node2:
            return (self.node1,self.weight)
        return ()

class Node:
    def __init__(self, name, neighTable=None, routingTable=None):
        if routingTable is None:
            routingTable = {}
        if neighTable is None:
            neighTable = {}
        self.name = name
        self.neighTable = neighTable
        self.routingTable = routingTable

    def display_neigh(self):
        # display
        print("\n%s Neighbour Table:"%self.name)
        strings = []
        for key in self.neighTable:
            if self.neighTable[key] != math.inf:
                strings.append("{key},{value}".format(key=key,value=self.neighTable[key]))
        strings.sort()
        for s in strings:
            print(s)

    def display_route(self):
        print("\n%s Routing Table:"%self.name)
        strings = []
        for key in self.routingTable:
            if self.routingTable[key][1] != math.inf:
                strings.append("{key},{value},{num}".format(key=key,value=self.routingTable[key][0],num=self.routingTable[key][1]))
        strings.sort()
        for s in strings:
            print(s)

def init_nodes(nodes,names):
    # In initial state, all nodes are disconnected
    for node in nodes:
        for name in names:
            if node.name != name:
                node.routingTable[name] = ["",math.inf]
    return nodes

def display_LSDB(LSDB,name):
    tmp = LSDB.copy()
    names = {name}
    accessable = []
    flag = True
    while flag:
        flag = False
        for record in tmp:
            if record.node1 in names or record.node2 in names:
                accessable.append(record)
                names.add(record.node1)
                names.add(record.node2)
                flag = True
                tmp.remove(record)

    strings = []
    for record in accessable:
        strings.append(record.display())
    strings = [i for i in strings if i]
    strings.sort()
    for s in strings:
        if s != None:
            print(s)

def convert_to_matrix(LSDB,names):
    n = len(names)
    matrix = [[math.inf for x in range(n)] for y in range(n)]
    for record in LSDB:
        matrix[names.index(record.node1)][names.index(record.node2)] = record.weight
        matrix[names.index(record.node2)][names.index(record.node1)] = record.weight
    return matrix


def startwith(start: int, mgraph: list):
    dic = {}
    passed = [start]
    nopass = [x for x in range(len(mgraph)) if x != start]
    dis = mgraph[start]

    while len(nopass):
        idx = nopass[0]
        for i in nopass:
            if dis[i] < dis[idx]:
                idx = i

        nopass.remove(idx)
        passed.append(idx)

        for i in nopass:
            if dis[idx] + mgraph[idx][i] < dis[i]:
                dis[i] = dis[idx] + mgraph[idx][i]
                dic[i] = idx
    return (dis,dic)

def update_neigh(nodes,record):
    for node in nodes:
        if node.name == record.node1:
            node.neighTable[record.node2] = record.weight
        if node.name == record.node2:
            node.neighTable[record.node1] = record.weight
    return nodes

def update_routing_table_from_matrix(matrix,nodes,names):
    for i in range(len(nodes)):
        vec = matrix[i]
        node = nodes[i]
        for key in node.routingTable:
            weight = vec[names.index(key)]
            nodes[i].routingTable[key] = weight
    return nodes

def update_route(nodes,LSDB,names):
    # update neigh
    for node in nodes:
        for key in node.neighTable:
            if node.neighTable[key] < node.routingTable[key][1]:
                node.routingTable[key][1] = node.neighTable[key]
                node.routingTable[key][0] = key
    matrix = convert_to_matrix(LSDB,names)

    for i in range(len(names)):
        tup = startwith(i,matrix)
        if len(tup) == 0:
            continue
        else:
            for key in tup[1].keys():
                value = tup[0][key]
                through = tup[1].get(key)
                nodes[i].routingTable[names[key]] = [names[through],value]
    return nodes

def update_nodes(nodes,LSDB,names,newRecord):
    nodes = update_neigh(nodes,newRecord)
    # if any connection is cut
    if newRecord.weight == math.inf:
        for node in nodes:
            for key in node.routingTable:
                if node.routingTable[key][0] == newRecord.node1 or node.routingTable[key][0] == newRecord.node2:
                    node.routingTable[key] = ["",math.inf]
    nodes = update_route(nodes,LSDB,names)
    return nodes

def remove_duplicated_LSDB(LSDB):
    if len(LSDB) > 1:
        new = LSDB[-1]
        for i in range(len(LSDB)-1):
            if LSDB[i].node1 == new.node1 and LSDB[i].node2 == new.node2:
                LSDB[i].weight = new.weight
                return LSDB[:-1]
            elif LSDB[i].node1 == new.node2 and LSDB[i].node2 == new.node1:
                LSDB[i].weight = new.weight
                return LSDB[:-1]
    return LSDB
    
# Read the topology from standard input
def read_topology():
    LSDB = []
    nodes = []
    names = []

    # NAME
    name = input()
    while name != "LINKSTATE":
        if name != "":
            nodes.append(Node(name))
            names.append(name)
            name = input()
    nodes = init_nodes(nodes,names)
    link = input()

    # LINKSTATE
    while link != "UPDATE":
        # process link sentence
        l = link.split(' ')
        optional = []
        if len(l) > 3:
            optional = l[-1].split(',')
        # append to LSDB
        if int(l[2]) == -1:
            LSDB.append(Path(l[0],l[1],math.inf))
            newRecord = Path(l[0],l[1],math.inf)
        else:
            LSDB.append(Path(l[0],l[1],int(l[2])))
            newRecord = Path(l[0], l[1], int(l[2]))
        # remove duplicated items from LSDB
        LSDB = remove_duplicated_LSDB(LSDB)
        # update node
        nodes = update_nodes(nodes,LSDB,names,newRecord)
        # display optional nodes
        if len(optional) > 0:
            for node in nodes:
                if node.name in optional:
                    node.display_neigh()
                    print("\n%s LSDB:" % node.name)
                    display_LSDB(LSDB,node.name)
                    node.display_route()
        link = input()

    # UPDATE
    update_line = input()
    while update_line != "END":
        # process update line
        l = update_line.split(' ')
        optional = []
        if len(l) > 3:
            optional = l[-1].split(',')

        # if new nodes are added
        if l[0] not in names:
            names.append(l[0])
            nodes.append(Node(l[0]))
            # init routing tables
            for node in nodes:
                if node.name == l[0]:
                    # for the new node
                    for name in names:
                        if name != l[0]:
                            node.routingTable[name] = ["",math.inf]
                else:
                    # for other nodes
                    node.routingTable[l[0]] = ["", math.inf]
        if l[1] not in names:
            names.append(l[1])
            nodes.append(Node(l[1]))
            # init routing tables
            # init routing tables
            for node in nodes:
                if node.name == l[1]:
                    # for the new node
                    for name in names:
                        if name != l[1]:
                            node.routingTable[name] = ["", math.inf]
                else:
                    # for other nodes
                    node.routingTable[l[1]] = ["", math.inf]

        # append to LSDB
        if int(l[2]) == -1:
            LSDB.append(Path(l[0], l[1], math.inf))
            newRecord = Path(l[0],l[1],math.inf)
        else:
            LSDB.append(Path(l[0], l[1], int(l[2])))
            newRecord = Path(l[0], l[1], int(l[2]))
        # remove duplicated items from LSDB
        LSDB = remove_duplicated_LSDB(LSDB)
        # update node
        nodes = update_nodes(nodes, LSDB, names, newRecord)
        # display optional nodes
        if len(optional) > 0:
            for node in nodes:
                if node.name in optional:
                    node.display_neigh()
                    print("\n%s LSDB:" % node.name)
                    display_LSDB(LSDB,node.name)
                    node.display_route()
        update_line = input()
    return nodes

nodes = read_topology()
