from random import randrange
from unittest import skip

import solarized
from util import *

scene_width = 14.2
tree_scale = 3
node_radius = 0.2


def sugar(scene, tree, n1, n2, n_sh):
    tree.rehang_subtree(
        scene,
        n1,
        n2,
        tree.vertices[n2].get_center() + n_sh * sh +  H,
        2 * DOWN,
        2 * DOWN,
    )


class Intro(Scene):
    def construct(self):
        
        num_img = 26
        img_positions = []
        
        for n, l1, l2 in [
            (10, [-4, -2, 0, 2, 4], [-2, 0, 2]),
            (10, [-6, -4, -2], [-2, 0, 2]),
        ]:
            for _ in range(n):
                while(True):
                    new_pos = np.array(random.choice(l1) * RIGHT + random.choice(l2) * UP)
                    i = max(0, len(img_positions) - 6)
                    collision = False
                    for pos in img_positions[i:]:
                        if np.array_equal(pos, new_pos):
                            collision = True
                    if collision == True:
                        continue
                    else:
                        img_positions.append(new_pos)
                        break
        
        dalle_images = []
        for i in range(len(img_positions)):
            dalle_images.append(
<<<<<<< HEAD
                ImageMobject("img/dalle/p{}.jpg".format((i % num_img)+1)).scale_to_fit_width(2).move_to(
                    img_positions[i]
=======
                ImageMobject("img/dalle/p{}.jpg".format(i + 1)).scale_to_fit_width(2).move_to(
                    random.choice([-4, -2, 0, 2, 4]) * RIGHT + random.choice([-2, 0, 2]) * UP
>>>>>>> automatic colouting
                )
            )

        anims = []
        for i in range(len(img_positions)):
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
                lag_ratio=0.1
            )
        )
        self.wait()


class Polylog(Scene):
    def construct(self):
        authors = Tex(
            r"\textbf{Václav Rozhoň, Vojtěch Rozhoň, Václav Volhejn}",
            color=text_color,
            font_size=40,
        ).shift(
            3 * DOWN + 0 * LEFT
        )

        channel_name = Tex(r"polylog", color=GRAY)
        channel_name[0][1].set_color(ORANGE)
        channel_name.scale(4).shift(1 * UP)

        self.wait()

        logo_dalle = ImageMobject("img/D2.png").scale(0.5).set_z_index(100)
        logo_solarized = ImageMobject("img/logo-solarized.png").scale(0.034).shift(0.3 * UP + 0.05 * LEFT)
        prompt_dalle = Tex(
            r"DALL$\cdot$E 2 on prompt: A logo suitable for a youtube channel about computer science",
            color=GRAY
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
            logo_solarized.animate().move_to(2 * LEFT + 1 * UP + 0.55 * RIGHT),
            Write(authors),
            FadeIn(channel_name[0][0]),
            FadeIn(channel_name[0][2:])
        )
        return

        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()

class Statement(Scene):
    def construct(self):
        self.next_section(skip_animations=True)

        caption = Tex("The Problem", color = GRAY).scale(3)
        self.play(
            FadeIn(caption)
        )
        self.wait()
        self.play(
            FadeOut(caption)
        )

        # The problem I’ll be solving is called Buds Re-hanging. In this problem, we are given a tree, so a bunch of nodes connected by edges such that no edges form a cycle. 

        statement = ImageMobject(
            "img/statement.png",
        ).scale_to_fit_width(scene_width / 2.0).shift(scene_width / 4 * LEFT + 8 * DOWN)
        statement_caption = Tex("Buds Re-hanging (Codeforces 1566E)", color=GRAY).scale(0.8).move_to(
            statement.get_center()).next_to(statement, UP)

        self.play(
            FadeIn(statement),
            FadeIn(statement_caption)
        )
        self.wait()



        example_tree = Tree(
            example_vertices,
            example_edges,
            layout="kamada_kawai",
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": WHITE},  # for debugging
            labels=True,  # for debugging
            edge_config={"color": text_color},
            root=1
        ).move_to(scene_width / 4 * RIGHT)

        self.play(
            FadeIn(example_tree),
        )
        self.wait()

        # This tree is also rooted, so each node except the root has one parent node and possibly some children. The nodes that have no children are called leaves – let’s highlight them in green.

        highlight_box = Rectangle(
            width=scene_width / 2 - 0.5,
            height=0.8,
            color=RED,
        ).next_to(statement_caption, DOWN).shift(1.3 * DOWN).set_z_index(100)

        self.play(
            FadeIn(highlight_box),
        )

        self.play(
            example_tree.animate().change_layout(rooted_position(pos_root=scene_width / 4 * RIGHT + 2 * UP)),
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
            start=example_vertex.get_center(),
            end=example_parent.get_center(),
            color=RED,
        )
        self.play(
            Create(edge_parent),
        )
        self.play(
            Circumscribe(example_parent, shape=Circle, color=RED)
        )
        self.play(
            Uncreate(edge_parent)
        )
        self.wait()

        # children
        example_children = [
            example_tree.vertices[3],
            example_tree.vertices[4],
            example_tree.vertices[5],
        ]
        edge_children = [
            Line(
                start=example_vertex.get_center(),
                end=child.get_center(),
                color=RED,
            ) for child in example_children
        ]
        self.play(
            *[Create(e) for e in edge_children],
        )
        self.play(
            *[Circumscribe(child, shape=Circle, color=RED) for child in example_children]
        )
        self.play(
            *[Uncreate(e) for e in edge_children],
            example_vertex.animate().set_color(GRAY)
        )
        self.wait()

        # leaves
        leaves = example_tree.get_leaves()
        self.play(
<<<<<<< HEAD
            *[example_tree.vertices[v].animate().set_color(BLUE) for v in leaves]
=======
            example_tree.animate().pretty_colour()
>>>>>>> automatic colouting
        )
        self.wait()

        # So far, these are standard terms. In this problem specifically, we also need the concept of a bud. A bud is a node that’s not a root, has at least one child, and all its children are leaves. In other words, buds are basically the nodes that have only leaves as children but are not leaves themselves. I highlighted all of these in blue. 

        highlight_box.generate_target()
        highlight_box.target = Rectangle(
            width=highlight_box.get_width(),
            height=1.4,
            color=RED,
        ).next_to(highlight_box, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER / 2.0)
        self.play(
            MoveToTarget(highlight_box),
        )
        self.wait()

        arrow = Arrow(
            start=ORIGIN,
            end=ORIGIN + LEFT / 2,
            color=RED,
        ).scale(3).move_to(3 * LEFT + 0 * DOWN)

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

        # Now, we’re allowed to manipulate our tree it in the following way: we can take a bud and re-hang it and its children to another node of the tree. Notice that in this case, after we cut  this bud off the tree, this guy becomes a new bud, and after we put the bud back here, this guy stops being a leaf and also this is not a bud anymore.
        self.next_section(skip_animations=False)

        highlight_box.generate_target()
        highlight_box.target = Rectangle(
            width=highlight_box.get_width(),
            height=1.2,
            color=RED,
        ).next_to(highlight_box, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER / 2.0)
        self.play(
            MoveToTarget(highlight_box),
        )
        self.wait()

<<<<<<< HEAD
=======
        H = 1 * DOWN
>>>>>>> automatic colouting

        example_tree.rehang_subtree(
            self,
            5,
            10,
            example_tree.vertices[10].get_center() + H,
            1 * DOWN,
            1 * LEFT + 1 * DOWN,
        )

        example_tree.rehang_subtree(
            self,
            5,
            2,
            example_tree.vertices[10].get_center() + H,
            1*LEFT + 1 * DOWN,
            1 *DOWN,            
        )

        example_tree.rehang_subtree(
            self,
            5,
            10,
            example_tree.vertices[10].get_center() + H,
            1 *DOWN,
            1*LEFT + 1 * DOWN,
        )

        self.wait()
<<<<<<< HEAD
        
        #And now the question is: You’re allowed to do these operations any number of times with any buds you choose. If you do the operations as cleverly as possible, what’s the lowest number of leaves the tree can have? For example, the number of leaves at the beginning is 7. You can see how it changes when we do the operations and the lowest we can get seems to be 5.
=======
        return
        # And now the question is: You’re allowed to do these operations any number of times with any buds you choose. If you do the operations as cleverly as possible, what’s the lowest number of leaves the tree can have? For example, the number of leaves at the beginning is 7. You can see how it changes when we do the operations and the lowest we can get seems to be 5.
>>>>>>> automatic colouting

        highlight_box.generate_target()
        highlight_box.target = Rectangle(
            width=highlight_box.get_width(),
            height=0.4,
            color=RED,
        ).next_to(highlight_box, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER / 2.0)
        self.play(
            MoveToTarget(highlight_box),
        )
        self.wait()

<<<<<<< HEAD
        example_tree.rehang_subtree(
            self,
            5,
            10,
            example_tree.vertices[10].get_center() + H,
            1 *DOWN,
            1*LEFT + 1 * DOWN,
        )
=======
        # TODO
>>>>>>> automatic colouting

        example_tree.rehang_subtree(
            self,
            12,
            4,
            example_tree.vertices[4].get_center() + H,
            2 * DOWN,
            2 * DOWN,
        )

        example_tree.rehang_subtree(
            self,
            5,
            11,
            example_tree.vertices[11].get_center() + H,
            1 * DOWN,
            1 * DOWN,
        )

        self.wait()
        # Because this is a coding problem, it is also important how large the input data is. You can see that the tree can have around 10^5 nodes, which means that our algorithm for computing the answer needs to have close to linear time complexity. 

        self.play(
            Group(
                statement,
                statement_caption,
                highlight_box,
            ).animate().shift(6 * UP)
        )
        self.wait()

        highlight_box.generate_target()
        highlight_box.target = Rectangle(
            width=highlight_box.get_width(),
            height=1.4,
            color=RED,
        ).next_to(highlight_box, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER / 2.0).shift(0.3 * DOWN)
        self.play(
            MoveToTarget(highlight_box),
        )
        self.wait()

        # There are examples in the problem statement to make this clearer. Let’s look at the first one: the tree looks like this. It has four leaves. But if we rehang this bud here and this bud there, we get a tree with two leaves, which is the correct answer.

        highlight_box.generate_target()
        highlight_box.target = Rectangle(
            width=highlight_box.get_width(),
            height=1.7,
            color=RED,
        ).next_to(highlight_box, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER / 2.0).shift(2.5 * DOWN)
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
            vertex_config={"radius": node_radius, "color": WHITE},  # for debugging
            labels=True,  # for debugging
            edge_config={"color": text_color}
        )  # .move_to(scene_width/4 * RIGHT)

        H = 1.0 * DOWN
        W = 0.6 * RIGHT
        sample_tree.change_layout(
            {
                1: ORIGIN,
                2: H - W,
                3: H,
                4: H + W,
                5: 2 * H - 3 * W / 2,
                6: 2 * H - W / 2,
                7: 2 * H + W,
            }
        ).move_to(scene_width / 4 * RIGHT + 1 * UP)

        self.play(
            Create(sample_tree),
        )
        self.wait()

        self.play(
            Group(
                statement,
                statement_caption,
                highlight_box,
            ).animate().shift(4 * UP)
        )
        highlight_box2 = Rectangle(
            width=highlight_box.get_width(),
            height=0.3,
            color=RED,
        ).move_to(highlight_box.get_center()).shift(5.5 * DOWN)
        self.play(
            Create(highlight_box2),
        )

        self.wait()

class Solution(Scene):
    def construct(self):
        self.next_section(skip_animations=True)
        num_leaves = Tex(r"\# leaves: ", color = BLUE).move_to(6*LEFT)
        num_leaves_counter = Integer(7, color = BLUE).next_to(num_leaves, RIGHT)

        example_tree = Tree(
            example_vertices,
            example_edges,
            layout=rooted_position(pos_root = 3*UP),
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": WHITE}, # for debugging
            labels=True, # for debugging
            edge_config={"color": text_color},
            root = 1
        )

        self.play(
            FadeIn(example_tree),
            FadeIn(num_leaves),
            FadeIn(num_leaves_counter),
        )
        self.wait()

        # Then I tried to solve the problem manually for this tree. I noticed that if I take this bud [vrchol 5] and put it for example here, I get rid of one leaf, so that is good. 
        example_tree.rehang_subtree(
            self,
            5,
            10,
            example_tree.vertices[10].get_center() + H - sh,
            2 * DOWN,
            2 * DOWN,
        )
        self.play(
            Flash(
                example_tree.vertices[10],
                color = BLUE,
            )
        )
        self.wait()

        # Also, this guy now becomes a bud, so I can again hang it somewhere else and now the number of leaves drops down to 5. This turns out to be the smallest possible number, but at this point this was not clear at all.
        # self.play(
        #     Flash(
        #         example_tree.vertices[2],
        #         color = RED,
        #     )
        # )
        # self.wait()
        sugar(self, example_tree, 2, 6, 0)

        # So I continued playing with the tree and for quite some time I did not have much of an idea about what was happening until I realized the following thing. Let’s look for example at this bud and circle it and its leaves. And then do some random operations. You can see that the bud and its leaves always stay together, they never separate.

        sugar(self, example_tree, 2, 1, -2)

        sugar(self, example_tree, 5, 1, -5)

        sugar(self, example_tree, 12, 1, 5)

        sugar(self, example_tree, 12, 10, 0)


        sugar(self, example_tree, 5, 3, 0)

        sugar(self, example_tree, 5, 4, 0)

        sugar(self, example_tree, 5, 13, 0)

        sugar(self, example_tree, 2, 8, 0)

        sugar(self, example_tree, 2, 11, 0)

        sugar(self, example_tree, 5, 1, -2)

        # So I continued playing with the tree and for quite some time I did not have much of an idea about what was happening until I realized the following thing. Let’s look for example at this bud and circle it and its leaves. And then do some random operations. You can see that the bud and its leaves always stay together, they never separate.

        # TODO circle 5

        rel_pos_5 = 0.5*UP
        circle5 = CubicBezier(
            ORIGIN,
            1.4*(2*LEFT + 2*DOWN),
            1.4*(2*RIGHT + 2*DOWN),
            ORIGIN,
            color = BLACK
        ).move_to(
            example_tree.vertices[5].get_center()
        ).shift(rel_pos_5)

        # self.play(
        #     FadeIn(circle5)
        # )
        # circle5.add_updater(
        #     lambda m: m.move_to(
        #         example_tree.vertices[5].get_center()
        #     ).shift(
        #         rel_pos_5
        #     )
        # )

        sugar(self, example_tree, 12, 6, 0)

        sugar(self, example_tree, 2, 8, 0)

        sugar(self, example_tree, 12, 1, -5)

        sugar(self, example_tree, 2, 10, 0)

        sugar(self, example_tree, 5, 11, 0)

        sugar(self, example_tree, 12, 5, 2)

        #TODO more animations

        # return back
        sugar(self, example_tree, 2, 1, -2)


        sugar(self, example_tree, 12, 10, 0)

        sugar(self, example_tree, 5, 2, 1)

        sugar(self, example_tree, 12, 11, 0)
       


        # And that holds in general. I realized that I can imagine repeatedly cutting the buds from the tree in any order like this. 

        #TODO more animations
        self.next_section(skip_animations=False)
        
        sub5 = example_tree.remove_subtree(self, 5)
        self.play(
            sub5.animate().shift(2*DOWN)
        )

        sub2 = example_tree.remove_subtree(self, 2)
        self.play(
            sub2.animate().shift(1*DOWN)
        )

        sub12 = example_tree.remove_subtree(self, 12)
        self.play(
            sub12.animate().shift(1*DOWN)
        )

        sub9 = example_tree.remove_subtree(self, 9)
        self.play(
            sub9.animate().shift(1*DOWN)
        )
        self.wait()

        # Now I draw the circle around each bud and put them back. 
        
        self.play(
            sub9.animate().shift(1*UP)
        )
        example_tree.add_subtree(self, sub9, 1)

        self.play(
            sub12.animate().shift(-1*DOWN)
        )
        example_tree.add_subtree(self, sub12, 11)

        self.play(
            sub2.animate().shift(-1*DOWN)
        )
        example_tree.add_subtree(self, sub2, 1)

        self.play(
            sub5.animate().shift(-2*DOWN)
        )
        example_tree.add_subtree(self, sub5, 2)
        # If I now do some random bud-cutting operations, you see that the nodes in the same circle always stay together. 
        
        #TODO more animations

        self.play(
            *[
                Flash(example_tree.vertices[v], color = RED) for v in red_nodes
            ]
        )
        self.wait()
        
        self.play(
            *[
                Flash(example_tree.vertices[v], color = BLUE) for v in blue_nodes
            ]
        )
        self.wait()
        
        # Ok, now we understand what rehanging is doing quite well, so what is again the problem we actually want to solve? Right, we want as few leaves as possible. Hm, can we somehow use the fact that leaves are all blue nodes? 

        blue_nonleaves = [1, 11]
        blue_leaves = [x for x in blue_nodes if x not in blue_nonleaves]

        circles_leaves = [
            Circle(radius = 0.3, color = BLUE).move_to(example_tree.vertices[v])
            for v in blue_leaves
        ]
        circles_nonleaves = [
            Circle(radius = 0.3, color = BLUE).move_to(example_tree.vertices[v])
            for v in blue_nonleaves
        ]

        # Well, instead of minimizing the number of leaves we can maximize the number of blue nodes that are not leaves. That means we want as many as possible of these guys. 
        self.play(
            *[
                Create(c) for c in circles_leaves
            ]
        )
        self.wait()        

        
        self.play(
            *[
                Uncreate(c) for c in circles_leaves
            ],
            *[
                Create(c) for c in circles_nonleaves
            ]
        )
        self.wait()        
        self.play(
            *[
                Uncreate(c) for c in circles_nonleaves
            ],
        )
        self.wait()

        # These blue nodes are not leaves, because they have at least one red child that covers them. This child needs to be a red node. 

        self.wait(10)

class Explore(Scene):
    def construct(self):

        curve = CubicBezier(
            ORIGIN,
            3*(2*LEFT + 2*DOWN),
            3*(2*RIGHT + 2*DOWN),
            ORIGIN,
            color = BLACK
        )

        self.add(curve)

        return
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
        example_tree.change_layout(rooted_position(pos_root=2 * UP))
        self.add(example_tree)
        return

        H = 1 * DOWN
        example_tree.rehang_subtree(
            self,
            5,
            10,
            example_tree.vertices[10].get_center() + H,
            1 * DOWN,
            1 * LEFT + 1 * DOWN,
        )

        # v_from = 2
        # v_to = 9
        # new_pos = 2*LEFT
        # dir1 = 1*RIGHT
        # dir2 = 1*RIGHT
        # scene = self

        # curve = CubicBezier(
        #     example_tree.vertices[v_from].get_center(),
        #     example_tree.vertices[v_from].get_center() + dir1,
        #     new_pos + dir2,
        #     new_pos,
        # )
        # scene.add(curve)

        # subtree = example_tree.remove_subtree(scene, v_from)

        # scene.wait(4)

        # self.play(
        #     subtree.animate().shift(1*LEFT)
        # )

        # scene.play(
        #     MoveAlongPath(subtree, Line(UP, DOWN))
        # )
        return

        example_tree.add_subtree(scene, subtree, v_to)

        self.wait()

        return
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
            subtree3.animate().shift(2 * LEFT),
            subtree4.animate().shift(2 * RIGHT)
        )

        example_tree.add_subtree(self, subtree, 1)
        example_tree.add_subtree(self, subtree2, 1)
        example_tree.add_subtree(self, subtree3, 8)
        example_tree.add_subtree(self, subtree4, 6)
        example_tree.change_colours()
        example_tree.pretty_colour()
        self.wait(3)

        return