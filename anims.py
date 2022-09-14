from random import randrange

import solarized
from util import *

scene_width = 14.2

class Intro(Scene):
    def construct(self):

        num_img = 26
        dalle_images = []
        for i in range(num_img):
            dalle_images.append(
                ImageMobject("img/dalle/p{}.jpg".format(i+1)).scale_to_fit_width(2).move_to(
                    random.choice([-4, -2, 0, 2, 4]) * RIGHT + random.choice([-2, 0, 2]) * UP
                )
            )

        anims = []
        for i in range(num_img):
            anims.append(
                Succession(
                    FadeIn(dalle_images[i]),
                    Wait(3),
                    FadeOut(dalle_images[i])
                )
            )

        self.play(
            AnimationGroup(
                *anims,
                lag_ratio = 0.1
            )
        )
        self.wait()

class Polylog(Scene):
    def construct(self):
        authors = Tex(
            r"\textbf{Václav Rozhoň, Vojtěch Rozhoň, Václav Volhejn}", 
            color=text_color,
            font_size = 40,
        ).shift(
            3*DOWN + 0*LEFT
        )

        channel_name = Tex(r"polylog", color=GRAY)
        channel_name[0][1].set_color(ORANGE)
        channel_name.scale(4).shift(1 * UP)


        self.wait()

        logo_dalle = ImageMobject("img/D2.png").scale(0.5).set_z_index(100)
        logo_solarized = ImageMobject("img/logo-solarized.png").scale(0.034).shift(0.3*UP+0.05*LEFT)
        prompt_dalle = Tex(
            r"DALL$\cdot$E 2 on prompt: A logo suitable for a youtube channel about computer science", 
            color = GRAY
        ).scale(0.3).next_to(logo_dalle, DOWN)

        self.play(
            FadeIn(logo_dalle),
            FadeIn(prompt_dalle)
        )
        self.wait()

        self.add(logo_solarized)

        self.play(
            FadeOut(logo_dalle),
            FadeOut(prompt_dalle),
        )

        self.play(
            logo_solarized.animate().move_to(2*LEFT + 1*UP + 0.55 * RIGHT),
            Write(authors),
            FadeIn(channel_name[0][0]),
            FadeIn(channel_name[0][2:])
        )
        return

        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()

class ProblemStatement(Scene):
    def construct(self):
        # The problem I’ll be solving is called Buds Re-hanging. In this problem, we are given a tree, so a bunch of nodes connected by edges such that no edges form a cycle. 

        statement = ImageMobject(
            "img/statement.png",
        ).scale_to_fit_width(scene_width/2.0).shift(scene_width/4 * LEFT + 8*DOWN)
        statement_caption = Tex("Buds Re-hanging (Codeforces 1566E)", color = GRAY).scale(0.8).move_to(statement.get_center()).next_to(statement, UP)

        self.play(
            FadeIn(statement),
            FadeIn(statement_caption)
        )
        self.wait()

        tree_scale = 3
        node_radius = 0.2

        example_tree = Tree(
            example_vertices,
            example_edges,
            layout="kamada_kawai",
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": WHITE}, # for debugging
            labels=True, # for debugging
            edge_config={"color": text_color}
        ).move_to(scene_width/4 * RIGHT)

        self.play(
            FadeIn(example_tree),
        )
        self.wait()



        #This tree is also rooted, so each node except the root has one parent node and possibly some children. The nodes that have no children are called leaves – let’s highlight them in green.

        highlight_box = Rectangle(
            width = scene_width/2 - 0.5,
            height = 0.8,
            color = RED,
        ).next_to(statement_caption, DOWN).shift(1.3*DOWN).set_z_index(100)

        self.play(
            FadeIn(highlight_box),
        )

        self.play(
            example_tree.animate().change_layout(rooted_position(pos_root = scene_width/4*RIGHT + 2*UP)),
            run_time=1
        )
        self.wait()

        example_vertex = example_tree.vertices[2]
        self.play(
            example_vertex.animate().set_color(RED)
        )
        self.wait()

        # parent
        example_parent = example_tree.vertices[1]
        edge_parent = Line(
            start = example_vertex.get_center(),
            end = example_parent.get_center(),
            color = RED,
        )
        self.play(
            Create(edge_parent),
        )
        self.play(
            Circumscribe(example_parent, shape = Circle, color = RED)
        )
        self.play(
            Uncreate(edge_parent)
        )
        self.wait()

        #children
        example_children = [
            example_tree.vertices[3],
            example_tree.vertices[4],
            example_tree.vertices[5],
        ]
        edge_children = [
            Line(
                start = example_vertex.get_center(),
                end = child.get_center(),
                color = RED,
            ) for child in example_children
        ]
        self.play(
            *[Create(e) for e in edge_children],
        )
        self.play(
            *[Circumscribe(child, shape = Circle, color = RED) for child in example_children]
        )
        self.play(
            *[Uncreate(e) for e in edge_children],
            example_vertex.animate().set_color(GRAY)
        )
        self.wait()    
        
        # leaves
        leaves = example_tree.get_leaves()
        self.play(
            *[example_tree.vertices[v].animate().set_color(GREEN) for v in leaves]
        )
        self.wait()

        # So far, these are standard terms. In this problem specifically, we also need the concept of a bud. A bud is a node that’s not a root, has at least one child, and all its children are leaves. In other words, buds are basically the nodes that have only leaves as children but are not leaves themselves. I highlighted all of these in blue. 

        highlight_box.generate_target()
        highlight_box.target = Rectangle(
            width = highlight_box.get_width(),
            height = 1.4,
            color = RED,
        ).next_to(highlight_box, DOWN, buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER/2.0)
        self.play(
            MoveToTarget(highlight_box),
        )
        self.wait()

        arrow = Arrow(
            start = ORIGIN,
            end = ORIGIN + LEFT/2,
            color = RED,
        ).scale(3).move_to(3*LEFT + 0*DOWN)

        self.play(
            Create(arrow)
        )
        self.wait()
        line_height = 0.2
        for _ in range(2):
            self.play(
                arrow.animate().shift(line_height * DOWN)
            )
            self.wait()
        self.play(
            Uncreate(arrow)
        )
        self.wait()

        #Now, we’re allowed to manipulate our tree it in the following way: we can take a bud and re-hang it and its children to another node of the tree. Notice that in this case, after we cut  this bud off the tree, this guy becomes a new bud, and after we put the bud back here, this guy stops being a leaf and also this is not a bud anymore. 

        highlight_box.generate_target()
        highlight_box.target = Rectangle(
            width = highlight_box.get_width(),
            height = 1.2,
            color = RED,
        ).next_to(highlight_box, DOWN, buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER/2.0)
        self.play(
            MoveToTarget(highlight_box),
        )
        self.wait()

        #And now the question is: You’re allowed to do these operations any number of times with any buds you choose. If you do the operations as cleverly as possible, what’s the lowest number of leaves the tree can have? For example, the number of leaves at the beginning is 7. You can see how it changes when we do the operations and the lowest we can get seems to be 5.

        highlight_box.generate_target()
        highlight_box.target = Rectangle(
            width = highlight_box.get_width(),
            height = 0.4,
            color = RED,
        ).next_to(highlight_box, DOWN, buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER/2.0)
        self.play(
            MoveToTarget(highlight_box),
        )
        self.wait()

        #TODO

        # Because this is a coding problem, it is also important how large the input data is. You can see that the tree can have around 10^5 nodes, which means that our algorithm for computing the answer needs to have close to linear time complexity. 

        self.play(
            Group(
                statement,
                statement_caption,
                highlight_box,
            ).animate().shift(6*UP)
        )
        self.wait()

        highlight_box.generate_target()
        highlight_box.target = Rectangle(
            width = highlight_box.get_width(),
            height = 1.4,
            color = RED,
        ).next_to(highlight_box, DOWN, buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER/2.0).shift(0.3*DOWN)
        self.play(
            MoveToTarget(highlight_box),
        )
        self.wait()


        # There are examples in the problem statement to make this clearer. Let’s look at the first one: the tree looks like this. It has four leaves. But if we rehang this bud here and this bud there, we get a tree with two leaves, which is the correct answer.

        highlight_box.generate_target()
        highlight_box.target = Rectangle(
            width = highlight_box.get_width(),
            height = 1.7,
            color = RED,
        ).next_to(highlight_box, DOWN, buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER/2.0).shift(2.5*DOWN)
        self.play(
            MoveToTarget(highlight_box),
        )
        self.wait()

        self.play(
            Uncreate(example_tree),
        )

        sample_tree = Tree(
            sample_vertices,
            sample_edges,
            layout="kamada_kawai",
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": WHITE}, # for debugging
            labels=True, # for debugging
            edge_config={"color": text_color}
        )#.move_to(scene_width/4 * RIGHT)

        H = 1.0 * DOWN
        W = 0.6 * RIGHT
        sample_tree.change_layout(
            {
                1: ORIGIN,
                2: H - W,
                3: H,
                4: H + W,
                5: 2*H - 3*W/2,
                6: 2*H - W/2,
                7: 2*H + W,
            }
        ).move_to(scene_width/4 * RIGHT + 1*UP)

        self.play(
            Create(sample_tree),
        )
        self.wait()

        self.play(
            Group(
                statement,
                statement_caption,
                highlight_box,
            ).animate().shift(4*UP)
        )
        highlight_box2 = Rectangle(
            width = highlight_box.get_width(),
            height = 0.3,
            color = RED,
        ).move_to(highlight_box.get_center()).shift(5.5*DOWN)
        self.play(
            Create(highlight_box2),
        )

        self.wait()



class Explore(Scene):
    def construct(self):
        tree_scale = 3
        node_radius = 0.2

        # colour_function = lambda x: forest.pretty_colour(solarized.BLUE, solarized.CYAN)

        example_tree = Tree(
            example_vertices,
            example_edges,
            layout="kamada_kawai",
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": WHITE},
            labels=True,
            root=1,
            edge_config={"color": text_color}
        )
        self.add(example_tree)

        self.wait(2)

        example_tree.pretty_colour()
        self.wait()

        self.add(example_tree)
        self.wait()

        subtree = example_tree.remove_subtree(self, 5)
        subtree.pretty_colour()
        subtree2 = example_tree.remove_subtree(self, 12)
        subtree2.pretty_colour()
        example_tree.pretty_colour()
        self.wait(1)

        self.play(
            subtree.animate().shift(2 * LEFT),
            subtree2.animate().shift(2 * RIGHT)
        )

        subtree3 = example_tree.remove_subtree(self, 9)
        subtree3.pretty_colour()
        subtree4 = example_tree.remove_subtree(self, 2)
        subtree4.pretty_colour()
        example_tree.pretty_colour()
        self.wait(1)

        self.play(
            subtree3.animate().shift(2*LEFT),
            subtree4.animate().shift(2*RIGHT)
        )

        example_tree.add_subtree(self, subtree, 1)
        example_tree.add_subtree(self, subtree2, 1)
        example_tree.add_subtree(self, subtree3, 8)
        example_tree.add_subtree(self, subtree4, 6)
        example_tree.change_colours()
        example_tree.pretty_colour()
        self.wait(3)

        return 


        forest = Forest(example_tree, solarized.BLUE, solarized.CYAN)

        example_tree.add_updater(colour_function)

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
        new_tree.add_updater(colour_function)

        new_tree2 = forest.remove_subtree_from_tree(0, 12)
        new_tree2.add_updater(colour_function)
        self.add(new_tree)
        self.add(new_tree2)
        self.remove(example_tree)
        self.add(example_tree)

        self.play(
            new_tree.animate().shift(2*LEFT),
            run_time=1
        )
        self.play(
            new_tree2.animate().shift(2 * RIGHT),
            run_time=1
        )
        new_tree3 = forest.remove_subtree_from_tree(0, 2)
        new_tree3.add_updater(colour_function)

        new_tree4 = forest.remove_subtree_from_tree(0, 9)
        new_tree4.add_updater(colour_function)
        self.add(new_tree3)
        self.add(new_tree4)
        self.remove(example_tree)
        self.add(example_tree)

        self.play(
            new_tree3.animate().shift(2 * LEFT),
            run_time=1
        )
        self.play(
            new_tree4.animate().shift(2 * RIGHT),
            run_time=1
        )
        self.wait(2)

        forest.remove_updaters(colour_function)


        self.play(
            new_tree4.animate().shift(2 * LEFT),
            run_time=1
        )
        self.play(
            new_tree3.animate().shift(2 * RIGHT),
            run_time=1
        )
        self.play(
            new_tree2.animate().shift(2 * LEFT),
            run_time=1
        )
        self.play(
            new_tree.animate().shift(2 * RIGHT),
            run_time=1
        )
        colours = {}
        leaves = forest.get_leaves()
        buds = forest.get_buds()
        for leaf in leaves:
            colours[leaf] = solarized.RED
        for bud in buds:
            colours[bud] = solarized.YELLOW

        forest.add_subtree_to_tree(3, 0, 1, 0)
        self.remove(new_tree3)
        forest.add_subtree_to_tree(0, 3, 2, 2)
        self.remove(new_tree)
        forest.add_subtree_to_tree(1, 2, 1, 1)
        self.remove(new_tree4)
        tr = forest.add_subtree_to_tree(0, 1, 11, 0)
        self.remove(new_tree2)
        self.remove(example_tree)
        self.add(tr)
        tr.set_colors(colours)
        forest.pretty_colour(solarized.BLUE, solarized.CYAN)
        self.play(
            tr.animate().change_layout(rooted_position()),
            run_time=1
        )
        self.wait(2)

        # example_tree.add_subtree(new_tree3, 1)
        # self.remove(new_tree3)
        # self.remove(example_tree)
        # self.add(example_tree)
        # example_tree.add_subtree(new_tree, 2)
        # self.remove(new_tree)
        # example_tree.add_subtree(new_tree4, 1)
        # self.remove(new_tree4)
        # example_tree.add_subtree(new_tree2, 11)
        # self.remove(new_tree2)
        # self.remove(example_tree)
        # self.add(example_tree)
        # example_tree.set_colors(colours)
        # forest.pretty_colour(solarized.BLUE, solarized.CYAN)
        # self.wait(2)

