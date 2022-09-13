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

        forest = Forest(example_tree)

        example_tree.add_updater(lambda x: x.pretty_colour(solarized.BLUE, solarized.CYAN))

        budCounter = Integer(0, color=RED).shift(3*UP)
        budCounter.add_updater(lambda x: x.set_value(forest.get_leaves_cnt()))

        self.add(budCounter)

        # rooted version
        self.add(example_tree)

        self.play(
            example_tree.animate().change_layout(rooted_position()),
            run_time=1
        )
        self.wait(2)

        new_tree = forest.remove_subtree_from_tree(0, 5)
        new_tree.add_updater(lambda x: x.pretty_colour(solarized.BLUE, solarized.CYAN))
        self.add(new_tree)
        self.remove(example_tree)
        self.add(example_tree)

        self.play(
            new_tree.animate().shift(2*LEFT),
            run_time=1
        )
        self.wait(2)

        tr = forest.add_subtree_to_tree(1, 0, 9)
        tr.add_updater(lambda x: x.pretty_colour(solarized.BLUE, solarized.CYAN))
        self.remove(example_tree)
        self.remove(new_tree)
        self.add(tr)
        self.play(
            tr.animate().change_layout(rooted_position()),
            run_time=1
        )
        self.wait(2)

        self.play(
            tr.animate().shift(2 * UP),
            run_time=1
        )
        self.wait(2)

