from PriorityQueue import PrioritiyQueue


class PathFinder(object):
    def __init__(self, graph):
        self.graph = graph

    def find_path(self, start, goal):
        paths = self.a_star_search(self, start, goal)
        path = self.reconstruct_path(self, paths, start, goal)

        return path

    def heuristic(self, a, b):
        return self.graph.distance(a, b)

    def a_star_search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for point in self.graph.neighbors(current):
                new_cost = cost_so_far[current] + self.graph.cost(current, point)
                if point not in cost_so_far or new_cost < cost_so_far[point]:
                    cost_so_far[point] = new_cost
                    priority = new_cost + heuristic(goal, point)
                    frontier.put(point, priority)
                    came_from[point] = current

        return came_from, cost_so_far

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.appent(current)
            current = came_from[current]
        path.appent(strat)  # optional
        path.reverse()  # optional
        return path
