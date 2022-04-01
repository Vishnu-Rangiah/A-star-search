from copy import deepcopy
from queue import PriorityQueue
from Point import Point
import math

'''AIModule Interface
createPath(map map_) -> list<points>: Adds points to a path'''
class AIModule:

	def createPath(self, map_):
		pass

'''
A sample AI that takes a very suboptimal path.
This is a sample AI that moves as far horizontally as necessary to reach
the target, then as far vertically as necessary to reach the target.
It is intended primarily as a demonstration of the various pieces of the
program.
'''
class StupidAI(AIModule):

	def createPath(self, map_):
		path = []
		explored = []
		# Get starting point
		path.append(map_.start)
		current_point = deepcopy(map_.start)

		# Keep moving horizontally until we match the target
		while(current_point.x != map_.goal.x):
			# If we are left of goal, move right
			if current_point.x < map_.goal.x:
				current_point.x += 1
			# If we are right of goal, move left
			else:
				current_point.x -= 1
			path.append(deepcopy(current_point))

		# Keep moving vertically until we match the target
		while(current_point.y != map_.goal.y):
			# If we are left of goal, move right
			if current_point.y < map_.goal.y:
				current_point.y += 1
			# If we are right of goal, move left
			else:
				current_point.y -= 1
			path.append(deepcopy(current_point))

		# We're done!
		return path

class Djikstras(AIModule):

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					neighbor.comparator = alt
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path

class AStarExp(AIModule):

	def hue(self, neighbor, map_):

		h0 = map_.getTile(neighbor.x, neighbor.y)
		h1 = map_.getTile(map_.getEndPoint().x, map_.getEndPoint().y)
		hdif = abs(h1 - h0)

		dx = abs(neighbor.x - map_.getEndPoint().x)
		dy = abs(neighbor.y - map_.getEndPoint().y)
		dist = max(dx, dy)

		if h0<h1:
			return 2*hdif + max(0, dist-hdif)
		elif h0>h1:
			return (2**(hdif/dist)) * dist
		else:
			return dist

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()

			# if explored[str(v.x)+','+str(v.y)]: #shows consistency
			# 	continue

			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:

				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					h = self.hue(neighbor, map_)
					neighbor.comparator = alt + .65*h
					#huersitic function f(n) = g(n) + h(n)
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path

class AStarDiv(AIModule):

	def hue(self, v, neighbor, map_):
		dx = abs(neighbor.x - map_.getEndPoint().x)
		dy = abs(neighbor.y - map_.getEndPoint().y)
		h0 = map_.getTile(neighbor.x,neighbor.y)
		if h0<1:
			h0 = 1
		lh = math.floor(math.log(h0,2))
		cd = max(dx,dy)
		h = max( (cd - lh) / 2, 0)
		return h

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i) + ',' + str(j)] = math.inf
				prev[str(i) + ',' + str(j)] = None
				explored[str(i) + ',' + str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x) + ',' + str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()

			# if explored[str(v.x)+','+str(v.y)]: #shows consistency
			# 	continue

			explored[str(v.x) + ',' + str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x) + ',' + str(v.y)]
				if alt < cost[str(neighbor.x) + ',' + str(
						neighbor.y)]:
					cost[str(neighbor.x) + ',' + str(neighbor.y)] = alt
					h = self.hue(v,neighbor, map_)
					neighbor.comparator = alt + h
					# huersitic function f(n) = g(n) + h(n)
					prev[str(neighbor.x) + ',' + str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not (v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x) + ',' + str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path

class AStarMSH(AIModule):

	def hue_c(self, v, neighbor, map_):
		dx = abs(neighbor.x - map_.getEndPoint().x)
		dy = abs(neighbor.y - map_.getEndPoint().y)
		h0 = map_.getTile(neighbor.x,neighbor.y)
		if h0<1:
			h0 = 1
		lh = math.floor(math.log(h0))
		cd = max(dx,dy)
		h = max((cd - lh) / 2, 0)
		return h

	def hue(self, v, neighbor, map_):
		h0 = map_.getTile(neighbor.x, neighbor.y)
		h1 = map_.getTile(map_.getEndPoint().x, map_.getEndPoint().y)
		hdif = abs(h1 - h0)

		dx = abs(neighbor.x - map_.getEndPoint().x)
		dy = abs(neighbor.y - map_.getEndPoint().y)
		dist = max(dx, dy)

		if h0 < h1:
			return 2 * hdif + max(0, dist - hdif)
		elif h0 > h1:
			return (2 ** (hdif / dist)) * dist
		else:
			return dist

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					h = self.hue(v,neighbor, map_)
					h2 = self.hue_c(v, neighbor, map_)
					w = 0.45
					neighbor.comparator = alt + w*max(h,h2)
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path















































