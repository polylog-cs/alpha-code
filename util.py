import random
import math
import numpy as np
from manim import *
from solarized import *
from functools import cmp_to_key
import copy
import itertools
import string

############### GENERATING SOUNDS

def random_click_file():
	return f"audio/click/click_{random.randint(0, 3)}.wav"


def random_pop_file():
	return f"audio/pop/pop_{random.randint(0, 6)}.wav"


def random_whoosh_file():
	return f"audio/whoosh/whoosh_{random.randint(0, 3)}.wav"
whoosh_gain = -8
# use as: 
# self.add_sound(random_whoosh_file(), time_offset = 0.15, gain = whoosh_gain)


############### 


example_vertices = list(range(1, 15))
example_edges = [
    (1,2),
    (2,3),
    (2,4),
    (2,5),
    (5,6),
    (5,7),
    (5,8),
    (1,9),
    (9,10),
    (9,11),
    (11,12),
    (12,13),
    (13,14)
]


def rooted_position(pos_root = ORIGIN, sh = 0.5*RIGHT, SH = 1*RIGHT, H = 1*DOWN):

    positions = {}

    positions[1] = pos_root

    positions[2] = positions[1] - SH    + H
    positions[9] = positions[1] + SH    + H


    positions[3] = positions[2] - sh    + H
    positions[4] = positions[2] + H
    positions[5] = positions[2] + sh    + H
    positions[10]= positions[9] - sh    + H
    positions[11]= positions[9] + sh    + H

    positions[6] = positions[5] - sh    + H
    positions[7] = positions[5] + H
    positions[8] = positions[5] + sh    + H

    positions[12]= positions[11] + H
    positions[13]= positions[12] + H
    positions[14]= positions[13] + H

    return positions

############### 


class Tree(Graph):
    def __init__(self, *args, label_class=MathTex, **kwargs):
        # Hack to fix "labels=True" when TeX is not available
        # (uses `Text` instead of `MathTex`)
        if kwargs.get("labels") == True: #sorryjako
            # Assumes vertices are positional arg
            assert "vertices" not in kwargs
            labels = dict(
                (v, label_class(str(v), fill_color=BASE00).scale(0.7)) for v in args[0]
            )
            kwargs["labels"] = labels

        super().__init__(*args, **kwargs)

    def get_adjacency_list(self):
        adj = dict([(v, []) for v in self.vertices])
        for v1, v2 in self.edges:
            adj[v1].append(v2)
            adj[v2].append(v1)

        return adj

    def rot(self, mid, theta):
        new_layout = {}
        for u in self.vertices:
            pos_u = self[u].get_center()
            pos_u -= mid
            new_layout[u] = np.array( \
                (pos_u[0] * math.cos(theta) + pos_u[1] * math.sin(theta), \
                pos_u[1] * math.cos(theta) - pos_u[0] * math.sin(theta), \
                pos_u[2]))
            new_layout[u] += mid
        self.change_layout(new_layout)

    def bfs(self, start):
        adj = self.get_adjacency_list()

        res_vertices = [[start]]
        res_edges = [[]]
        res_parents = {start: None}
        seen = set([start])

        while True:
            cur_vertices = []
            cur_edges = []

            for v1 in res_vertices[-1]:
                for v2 in adj[v1]:
                    if v2 not in seen:
                        cur_vertices.append(v2)
                        seen.add(v2)
                        cur_edges.append((v1, v2))
                        res_parents[v2] = v1

            if cur_vertices:
                res_vertices.append(cur_vertices)
                res_edges.append(cur_edges)
            else:
                break

        return res_vertices, res_edges, res_parents

    def get_path(self, start, end):
        _, _, parents = self.bfs(end)
        path = [start]

        while path[-1] != end:
            path.append(parents[path[-1]])

        return path

    def set_colors_all(self, color=BASE00):
        for v in self.vertices:
            self[v].set_color(color)

        for e in self.edges:
            self.edges[e].set_color(color)

        return self

    def set_colors(self, vertex_colors=None, edge_colors=None):
        if vertex_colors is not None:
            for v, c in vertex_colors.items():
                self[v].set_fill(c)

        if edge_colors is not None:
            for e, c in edge_colors.items():
                if e not in self.edges:
                    e = e[1], e[0]

                self.edges[e].set_color(c)

        return self

    def set_colors_and_enlarge(self, vertex_colors=None, edge_colors=None, sc=1):
        if vertex_colors is not None:
            for v, c in vertex_colors.items():
                self[v].set_fill(c)
                self[v].scale(sc)

        if edge_colors is not None:
            for e, c in edge_colors.items():
                if e not in self.edges:
                    e = e[1], e[0]

                self.edges[e].set_color(c)

        return self

    def set_path_color(self, start, end, color=RED):
        path = self.get_path(start, end)
        vertex_colors = dict((v, color) for v in path)
        edge_colors = dict(((a, b), color) for a, b in zip(path, path[1:]))

        return self.set_colors(vertex_colors, edge_colors)

