from util import *


class Explore(Scene):
    def construct(self):
        tree_scale = 3
        node_radius = 0.2

        example_tree = Tree(
            example_vertices,
            example_edges,
            layout="kamada_kawai",
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": text_color},
            labels=False,
            edge_config={"color": text_color}
        )

        # rooted version
        self.add(example_tree)

        self.play(
            example_tree.animate().change_layout(rooted_position()),
            run_time=1
        )
        self.wait(2)

        new_tree = example_tree.remove_subtree(5)
        self.add(new_tree)
        new_tree.change_layout(rooted_position())
        self.remove(example_tree)
        self.add(example_tree)

        self.play(
            new_tree.animate().shift(2*LEFT),
            run_time=1
        )
        self.wait(2)

        self.remove(new_tree)
        example_tree.add_subtree(new_tree, 10)
        self.remove(example_tree)

        self.play(
            example_tree.animate().shift(2 * UP),
            run_time=1
        )
        self.wait(2)

