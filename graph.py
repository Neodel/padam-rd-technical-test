from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

import logging

class Graph:
    def __init__(self, vertices: list[tuple], edges: list[tuple]):
        """
        Parameters
        ----------
        vertices : list[tuple]
            list of vertices coordinates.
        edges : list[tuple]
            list of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
        """
        self.vertices = vertices
        self.edges = edges

        #Logger configuration
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.info("Graph initialized with %d vertices and %d edges.", len(vertices), len(edges))

    def plot(self):
        """
        Plot the graph.
        """
        weights = list(set(edge[2] for edge in self.edges))
        colors = plt.cm.get_cmap("viridis", len(weights))
        _, ax = plt.subplots()
        for i, weight in enumerate(weights):
            lines = [[edge[-2][::-1], edge[-1][::-1]] for edge in self.edges if edge[2] == weight]
            ax.add_collection(LineCollection(lines, colors=colors(i), alpha=0.7, label=f"weight {weight}"))
        ax.plot()
        ax.legend()
        plt.title(f"#E={len(self.edges)}, #V={len(self.vertices)}")
        plt.show()

    def silly_path(self):
        """
        Create a path in the simplest and most straightforward way.

        Returns
        -------
        list[list[tuple]]
            List of lists of edges, one list for each connected component.
        """
        self.logger.info("Entering silly_path.")

        if not self.edges:
            return []

        edges_to_visit = self.edges[:]       # edges to visit list
        path = []                            # crossed edges list

        current_edge = edges_to_visit.pop(0) # Visit the first edge in the list
        path.append(current_edge)

        v1, v2, weight, coord1, coord2 = current_edge
        self.logger.debug(
            "Starting with edge: from vertex %d to vertex %d with weight %.2f: Coordinates (%f, %f) -> (%f, %f)",
            v1, v2, weight, coord1[0], coord1[1], coord2[0], coord2[1])

        current_vertex = v1  # Start from the first vertex of the first edge

        # Continue until all edges are visited
        while edges_to_visit:
            for i, edge in enumerate(edges_to_visit):
                vertex1, vertex2, _, _, _ = edge
                # We traverse an edge if one of its vertices matches the current vertex
                if vertex1 == current_vertex:
                    path.append(edge)
                    current_vertex = vertex2
                    edges_to_visit.pop(i)
                    #logging
                    v1, v2, weight, coord1, coord2 = edge
                    self.logger.debug("New edge : from vertex %d to vertex %d with weight %.2f: Coordinates (%f, %f) -> (%f, %f)",
                                v1, v2, weight, coord1[0], coord1[1], coord2[0], coord2[1])
                    break
                elif vertex2 == current_vertex:
                    path.append(edge)
                    current_vertex = vertex1
                    edges_to_visit.pop(i)
                    #logging
                    v1, v2, weight, coord1, coord2 = edge
                    self.logger.debug(
                        "New edge : from vertex %d to vertex %d with weight %.2f: Coordinates (%f, %f) -> (%f, %f)",
                        v1, v2, weight, coord1[0], coord1[1], coord2[0], coord2[1])
                    break
            else:
                # Si aucune arête connectée n'est trouvée, il n'y a plus d'arêtes à explorer
                self.logger.info("All edges have been traversed.")
                break

        return path