from PriorityQueue import PriorityQueue


class PathFinder(object):
    def __init__(self, graph):
        self.graph = graph

    def find_path(self, start, goal):
        paths = self.a_star_search(start, goal)
        path = self.reconstruct_path(paths, start, goal)

        return path

    def heuristic(self, a, b):
        return self.graph.distance(a, b)

    def a_star_search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start.get_key()] = None
        cost_so_far[start.get_key()] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for point in self.graph.neighbors(current):
                move_cost = self.graph.cost(current, point)
                new_cost = cost_so_far[current.get_key()] + move_cost
                if point is None:
                    continue
                if point.get_key() not in cost_so_far or new_cost < cost_so_far[point.get_key()]:
                    cost_so_far[point.get_key()] = new_cost
                    priority = new_cost + self.heuristic(goal, point)
                    frontier.put(point, priority)
                    came_from[point.get_key()] = current

        #return came_from, cost_so_far
        return came_from

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from.get(current.get_key())
        path.append(start)  # optional
        path.reverse()  # optional
        return path
