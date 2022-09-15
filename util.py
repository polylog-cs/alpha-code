import itertools
import random
import math
from manim import *
from typing import Set

import solarized
from solarized import *


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


example_vertices = list(range(1, 14))
example_edges = [
    (1, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (5, 6),
    (5, 7),
    (5, 8),
    (1, 9),
    (9, 10),
    (9, 11),
    (11, 12),
    (12, 13),
]
red_nodes = [2, 5, 9, 12]
blue_nodes = [x for x in range(1, 14) if x not in red_nodes]


sample_vertices = list(range(1, 8))
sample_edges = [
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 6),
    (4, 7),
]

H = 1*DOWN
sh = 0.5 * RIGHT

def rooted_position(pos_root=ORIGIN):
    SH = 2*sh
    positions = {}


    positions[1] = pos_root

    positions[2] = positions[1] - SH + H
    positions[9] = positions[1] + SH + H

    positions[3] = positions[2] - sh + H
    positions[4] = positions[2] + H
    positions[5] = positions[2] + sh + H
    positions[10] = positions[9] - sh + H
    positions[11] = positions[9] + sh + H

    positions[6] = positions[5] - sh + H
    positions[7] = positions[5] + H
    positions[8] = positions[5] + sh + H

    positions[12] = positions[11] + H
    positions[13] = positions[12] + H
    positions[14] = positions[13] + H

    return positions


###############


def flatten(lst):
    return [item for sublist in lst for item in sublist]


class Forest():
    def __init__(self, tree, bud_colour=solarized.RED, leaf_colour=solarized.GREEN):
        self.trees = []
        self.trees.append(tree)
        self.bud_colour = bud_colour
        self.leaf_colour = leaf_colour

    def add(self, tree):
        tree.change_layout(rooted_position())
        self.trees.append(tree)

    def remove(self, index: int):
        self.trees.pop(index)

    def get_leaves_cnt(self):
        return sum(tree.get_leaves_cnt() for tree in self.trees)

    def remove_subtree_from_tree(self, index: int, vertex: int):
        new_tree = self.trees[index].remove_subtree(vertex)
        self.trees.append(new_tree)
        new_tree.change_layout(rooted_position())
        return new_tree

    def add_subtree_to_tree(self, subtree_index: int, tree_index: int, vertex: int, position: int):
        tree = self.trees[tree_index].add_subtree(self.trees[subtree_index], vertex, position)
        if subtree_index < tree_index:
            self.trees.pop(tree_index)
            self.trees.pop(subtree_index)
        else:
            self.trees.pop(subtree_index)
            self.trees.pop(tree_index)
        self.add(tree)
        return tree

    def pretty_colour_with_gray_subtone(self, bud_colour=solarized.RED, leaf_colour=solarized.GREEN):
        for tree in self.trees:
            tree.pretty_colour_with_gray_subtone(bud_colour, leaf_colour)

    def remove_updaters(self, function):
        for tree in self.trees:
            tree.remove_updater(function)

    def get_buds(self):
        return [item for sublist in [tree.get_buds() for tree in self.trees] for item in sublist]

    def get_leaves(self):
        return [item for sublist in [tree.get_leaves() for tree in self.trees] for item in sublist]


class Tree(Graph):
    def __init__(self, *args, label_class=MathTex, root=None, **kwargs):
        # Hack to fix "labels=True" when TeX is not available
        # (uses `Text` instead of `MathTex`)
        if kwargs.get("labels"):
            # Assumes vertices are positional arg
            assert "vertices" not in kwargs
            labels = dict(
                (v, label_class(str(v), fill_color=BASE00).scale(0.7)) for v in args[0]
            )
            kwargs["labels"] = labels

        # self.root = root
        # if self.root != None:
        #     self.parents = self.compute_parents()

        super().__init__(*args, **kwargs)
        self.root = root
        self.parents = {root: None}
        if root != None:
            tmp = [root]
            while len(tmp) > 0:
                vertex = tmp.pop()
                for neighbour in self.get_adjacency_list()[vertex]:
                    if neighbour not in self.parents.keys():
                        self.parents[neighbour] = vertex
                        tmp.append(neighbour)

    def get_root(self) -> int:  # VR probably works now but rather have it as separate parameter
        return self.root

    def get_descendents(self, vertex: int) -> [int]:
        sons = self.sons(vertex)
        if len(sons) == 0:
            return [vertex]
        res = []
        for vertex in sons:
            for descendent in self.get_descendents(vertex):
                res.append(descendent)
        return res

    def sons(self, vertex: int) -> [int]:
        res = [v for v in self.get_adjacency_list()[vertex] if v != self.parents[vertex]]
        return res

    def parent(self, vertex: int) -> int:
        return self.parents[vertex]

    def get_largest_descendent(self, vertex: int) -> int:
        res = self.get_descendents()
        res.sort()
        return res[len(res) - 1]

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
            new_layout[u] = np.array(
                (pos_u[0] * math.cos(theta) + pos_u[1] * math.sin(theta),
                 pos_u[1] * math.cos(theta) - pos_u[0] * math.sin(theta), pos_u[2]))
            new_layout[u] += mid
        self.change_layout(new_layout)

    def bfs(self, start, condition=lambda x, y: True):
        adj = self.get_adjacency_list()

        res_vertices = [[start]]
        res_edges = [[]]
        res_parents = {start: None}
        seen = {start}

        while True:
            cur_vertices = []
            cur_edges = []

            for v1 in res_vertices[-1]:
                for v2 in adj[v1]:
                    if v2 not in seen and condition(v1, v2):
                        cur_vertices.append(v2)
                        seen.add(v2)
                        res_parents[v2] = v1
                        cur_edges.append((v1, v2))

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

    def update_vertexes(self, vertex: int, position: int, root: int, new_vertexes: [int], new_edges: [(int, int)]):
        res_vertexes = []
        res_edges = []
        all_vertexes = []

        max_value_before_root = vertex
        if position > 0:
            max_value_before_root = self.get_largest_descendent(self.sons(vertex)[position - 1])

        for v in self.vertices:
            if v > max_value_before_root:
                all_vertexes.append(v + len(new_vertexes))
            else:
                all_vertexes.append(v)

        for v in new_vertexes:
            all_vertexes.append(v + max_value_before_root - root + 1)

        all_vertexes.sort()

        map_new_vertexes = {}
        i = 0
        for v in all_vertexes:
            i += 1
            if v > max_value_before_root + len(new_vertexes):
                map_new_vertexes[v - len(new_vertexes)] = i
            elif v > max_value_before_root:
                map_new_vertexes[v - (max_value_before_root - root + 1)] = i
            else:
                map_new_vertexes[v] = i
            res_vertexes.append(i)

        for a, b in self.edges:
            res_edges.append((map_new_vertexes[a], map_new_vertexes[b]))

        res_edges.append((map_new_vertexes[vertex], map_new_vertexes[root]))

        for a, b in new_edges:
            res_edges.append((map_new_vertexes[a], map_new_vertexes[b]))

        return res_vertexes, res_edges

    def add_subtree(self, scene, subtree, vertex: int):

        subtree_layout = {}
        for v in subtree.vertices:
            subtree_layout[v] = subtree.vertices[v].get_center()

        self.add_vertices(
            *subtree.vertices,
            positions=subtree_layout
        )
        self.add_edges(
            *subtree.edges
        )
        self.set_colors(subtree.get_colours())

        parent_edge = Line(
            start=subtree.vertices[subtree.get_root()].get_center(),
            end=self.vertices[vertex].get_center(),
            color=GRAY,
        )
        scene.play(
            Create(parent_edge)
        )
        scene.remove(parent_edge)

        self.add_edges((vertex, subtree.get_root()))
        self.parents[subtree.get_root()] = vertex
        for k, v in self.get_colours().items():
            scene.play(
                self[k].animate().set_fill(v)
            )

        # nothing should happen on the scene
        scene.remove(self, subtree)
        scene.add(self)

    def remove_subtree(self, scene, vertex: int):
        vertices, edges, _ = self.bfs(vertex,
                                      lambda start, curr: curr != self.parent(start))  # VR I guess it works now?
        flatten_vertices = flatten(vertices)
        flatten_edges = flatten(edges)

        parent_edge = Line(
            start=self.vertices[vertex].get_center(),
            end=self.vertices[self.parent(vertex)].get_center(),
            color=GRAY,
        )

        subtree_layout = {}
        for v in flatten_vertices:
            subtree_layout[v] = self.vertices[v].get_center()

        subtree = Tree(
            flatten_vertices,
            flatten_edges,
            layout=subtree_layout,
            layout_scale=3,  # !
            vertex_config={"radius": 0.2, "color": text_color},
            labels=True,
            root=vertex,
            edge_config={"color": text_color}
        )

        # nothing should happen on the scene
        self.remove_vertices(*flatten_vertices)
        scene.remove(self)
        scene.add(self, subtree, parent_edge)
        subtree.pretty_colour()

        # delete the parent edge
        scene.play(
            Uncreate(parent_edge),
        )
        for k, v in self.get_colours().items():
            scene.play(
                self[k].animate().set_fill(v)
            )
        return subtree

    def rehang_subtree(self, scene, v_from, v_to, new_pos, dir1, dir2):
        root_pos = self.vertices[v_from].get_center()

        scene.play(
            Flash(self.vertices[v_from], color=RED)
        )

        subtree = self.remove_subtree(scene, v_from)

        curve = CubicBezier(
            root_pos,
            root_pos + dir1,
            new_pos + dir2,
            new_pos,
        )
        scene.add(curve)
        curve.shift(subtree.get_center() - root_pos)

        scene.play(
            MoveAlongPath(subtree, curve)
        )

        self.add_subtree(scene, subtree, v_to)
        scene.remove(curve)
        scene.wait()

    def get_leaves(self) -> Set[int]:
        res = set()
        for vertex in self.vertices:
            if len(self.sons(vertex)) == 0:
                res.add(vertex)
        return res

    def get_buds(self) -> Set[int]:
        adj = self.get_adjacency_list()
        leaves = self.get_leaves()
        res = set()

        for vertex in self.vertices:
            if vertex not in leaves and all(
                    neighbour in leaves or neighbour == self.parent(vertex) for neighbour in adj[vertex]):
                res.add(vertex)
        return res

    def get_leaves_cnt(self):
        return len(self.get_leaves())

    def get_buds_cnt(self):
        return len(self.get_buds())

    def get_colours(self, bud_colour=solarized.CYAN, leaf_colour=solarized.GREEN):
        colours = {}
        leaves = self.get_leaves()
        buds = self.get_buds()
        for vertex in self.vertices:
            if self[vertex].get_color().__str__() != solarized.GRAY.__str__() and vertex not in buds and vertex not in leaves:
                colours[vertex] = solarized.GRAY
        for vertex in leaves:
            if self[vertex].get_color().__str__() != leaf_colour.__str__():
                colours[vertex] = leaf_colour
        for vertex in buds:
            print(vertex, self[vertex].get_color().__str__(), bud_colour.__str__())
            if self[vertex].get_color().__str__() != bud_colour.__str__():
                colours[vertex] = bud_colour
        return colours

    def pretty_colour(self, bud_colour=solarized.CYAN, leaf_colour=solarized.GREEN):
        self.set_colors(self.get_colours(bud_colour, leaf_colour), None)

    def change_colours(self, bud_colour=solarized.CYAN, leaf_colour=solarized.GREEN):
        colours = {}
        leaves = self.get_leaves()
        buds = self.get_buds()
        for leaf in leaves:
            colours[leaf] = leaf_colour
        for bud in buds:
            colours[bud] = bud_colour
        self.set_colors(colours, None)
