# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#	 if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#	 (shortest path length).
#	 (If you don't know what we mean by best-first search, refer to
#	  http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#	 heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#	 with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#	 to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.


def bfs(graph, start, goal):
	agenda= [[start]]	#a list of paths stored as lists
	extended_set= set()	#set of nodes that have been extended
	result_path= []		#the search result

	while agenda:
		new_agenda= agenda[:]
		for path in agenda:
			new_agenda.remove(path)
			extended_set.add(path[-1])
			if path[-1]==goal:
				result_path= path
				break
			all_extensions= (path + [neighbour] for neighbour in graph.get_connected_nodes(path[-1]))
			for extension in all_extensions:
				if extension[-1] not in extended_set:
					new_agenda.append(extension)
		else:
			agenda= new_agenda
		if not result_path==[]:
			break

	return result_path

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
	agenda= [[start]]	#a list of paths stored as lists
	extended_set= set()	#set of nodes that have been extended
	result_path= []		#the search result

	while agenda:
		path= agenda[0]
		agenda.remove(path)
		extended_set.add(path[-1])
		if path[-1]==goal:
			result_path= path
			break
		all_extensions= (path + [neighbour] for neighbour in graph.get_connected_nodes(path[-1]))
		for extension in all_extensions:
			if extension[-1] not in extended_set:
				agenda.insert(0, extension)

	return result_path


## Now we're going to add some heuristics into the search.
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
	agenda= [[start]]	#a list of paths stored as lists
	result_path= []		#the search result

	while agenda:
		path= agenda[0]
		agenda.remove(path)

		if path[-1]==goal:
			result_path= path
			break

		sublevel_sorted= []
		all_extensions= (path + [neighbour] for neighbour in graph.get_connected_nodes(path[-1]))
		for extension in all_extensions:
			if extension[-1] not in extension[:-1]:
				sublevel_sorted.append(extension)
		sublevel_sorted= sorted(sublevel_sorted, key= lambda path: graph.get_heuristic(path[-1], goal))

		sublevel_sorted.extend(agenda)
		agenda= sublevel_sorted

	return result_path

'''
from graphs import NEWGRAPH1
import pdb
pdb.set_trace()
hill_climbing(NEWGRAPH1, 'F', 'G')
'''


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.	Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
	agenda= [[start]]	#a list of paths stored as lists
	result_path= []		#the search result

	while agenda:
		new_agenda= agenda[:]
		for path in agenda:
			new_agenda.remove(path)

			if path[-1]==goal:
				result_path= path
				break

			all_extensions= (path + [neighbour] for neighbour in graph.get_connected_nodes(path[-1]))
			for extension in all_extensions:
				if extension[-1] not in extension[:-1]:
					new_agenda.append(extension)
		else:
			new_agenda= sorted(new_agenda, key= lambda path: graph.get_heuristic(path[-1], goal))
			agenda= new_agenda[:beam_width]

		if not result_path==[]:
			break

	return result_path


## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
	distance= 0
	for node1,node2 in zip(node_names[:-1], node_names[1:]):
		distance+=(graph.get_edge(node1, node2)).length
	return distance


def branch_and_bound(graph, start, goal):
	agenda= [[start]]	#a list of paths stored as lists
	result_path= []		#the search result

	while agenda:
		path= min(agenda, key= lambda possible_path: path_length(graph, possible_path))
		agenda.remove(path)

		if path[-1]==goal:
			result_path= path
			break

		all_extensions= (path + [neighbour] for neighbour in graph.get_connected_nodes(path[-1]))
		for extension in all_extensions:
			if extension[-1] not in extension[:-1]:
				agenda.append(extension)

	return result_path


def a_star(graph, start, goal):
	agenda= [[start]]	#a list of paths stored as lists
	result_path= []		#the search result
	extended_set= set()	#set of nodes that have been extended

	while agenda:
		path= min(agenda, key= lambda possible_path: path_length(graph, possible_path) +
													 graph.get_heuristic(possible_path[-1], goal))
		agenda.remove(path)
		extended_set.add(path[-1])

		if path[-1]==goal:
			result_path= path
			break

		all_extensions= (path + [neighbour] for neighbour in graph.get_connected_nodes(path[-1]))
		for extension in all_extensions:
			if extension[-1] not in extended_set:
				agenda.append(extension)

	return result_path



## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.	Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
	for node in graph.nodes:
		if 

def is_consistent(graph, goal):
	raise NotImplementedError

HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
