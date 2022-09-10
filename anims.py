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
            # labels=True
        )


        # rooted version
        self.add(example_tree)

        self.play(
            example_tree.animate().change_layout(rooted_position()),
            run_time = 1
        )

        self.wait(5)
            