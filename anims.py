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
        tree.vertices[n2].get_center() + n_sh * sh + H,
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
                while (True):
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
                ImageMobject("img/dalle/p{}.jpg".format(i + 1)).scale_to_fit_width(2).move_to(
                    random.choice([-4, -2, 0, 2, 4]) * RIGHT + random.choice([-2, 0, 2]) * UP
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
        self.next_section(skip_animations=False)

        caption = Tex("The Problem", color=GRAY).scale(3)
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
            example_tree.animate().change_layout(rooted_position(pos_root=scene_width / 4 * RIGHT + 3 * UP)),
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
            example_tree.animate().pretty_colour()
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

        # Now, we’re allowed to manipulate our tree it in the following way: we can take a bud and re-hang it and its children to another node of the tree. 
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

        H = 1 * DOWN
        
        sugar(self, example_tree, 5, 13, 0)
        self.wait()

        # Notice that in this case, after we cut  this bud off the tree, this guy becomes a new bud, and after we put the bud back here, this guy stops being a leaf and also this is not a bud anymore.

        ar = Arrow(
            start = ORIGIN,
            end = (1*RIGHT + 1*DOWN)/1.0,
            color = RED,
        ).move_to(
            example_tree.vertices[2].get_center() + (1*LEFT + 1*UP)/2.0
        )

        self.play(
            #Flash(example_tree.vertices[2], color = RED),
            FadeIn(ar),
        )
        self.wait()

        self.play(FadeOut(ar))
        self.wait()

        ar = Arrow(
            start = ORIGIN,
            end = (1*LEFT + 1*DOWN)/1.0,
            color = RED,
        ).move_to(example_tree.vertices[12].get_center() + (1*RIGHT + 1*UP)/2.0)

        self.play(
            #Flash(example_tree.vertices[12], color = RED),
            FadeIn(ar),
        )
        self.wait()

        self.play(
            #Flash(example_tree.vertices[13], color = RED),
            ar.animate().shift(H),
        )
        self.wait()

        self.play(
            FadeOut(ar)
        )
        self.wait()

        
        # And now the question is: You’re allowed to do these operations any number of times with any buds you choose. If you do the operations as cleverly as possible, what’s the lowest number of leaves the tree can have? For example, the number of leaves at the beginning is 7. You can see how it changes when we do the operations and the lowest we can get seems to be 5.

        self.next_section(skip_animations=False)

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

        sugar(self, example_tree, 2, 10, 0)
        sugar(self, example_tree, 5, 1, -2)
        sugar(self, example_tree, 2, 13, 0)
        sugar(self, example_tree, 5, 10, 0)
        sugar(self, example_tree, 2, 1, -2)
        sugar(self, example_tree, 5, 2, 1)

        self.wait()

        num_leaves = Tex(r"\# leaves: ", color = BLUE).move_to(1*RIGHT + 3*DOWN)
        num_leaves_counter = Integer(7, color = BLUE).next_to(num_leaves, RIGHT)

        self.play(
            FadeIn(num_leaves),
            FadeIn(num_leaves_counter)
        )
        self.wait()

        sugar(self, example_tree, 5, 1, -5)
        sugar(self, example_tree, 12, 1, 5)
        sugar(self, example_tree, 12, 10, 0)
        sugar(self, example_tree, 5, 3, 0)
        sugar(self, example_tree, 5, 4, 0)
        sugar(self, example_tree, 5, 13, 0)
        sugar(self, example_tree, 2, 11, 0)
        sugar(self, example_tree, 5, 3, 0)


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

        W = 2*sh
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
        self.next_section(skip_animations=False)
        num_leaves = Tex(r"\# leaves: ", color = BLUE).move_to(6*LEFT)
        num_leaves_counter = Integer(7, color = BLUE).next_to(num_leaves, RIGHT)

        example_tree = Tree(
            example_vertices,
            example_edges,
            layout=rooted_position(),
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": WHITE},  # for debugging
            labels=True,  # for debugging
            edge_config={"color": text_color},
            root=1
        ).shift(3*UP)

        num_leaves_counter.add_updater(lambda x: x.set_value(Forest.get_leaves_cnt()))

        self.play(
            FadeIn(example_tree),
            FadeIn(num_leaves),
            FadeIn(num_leaves_counter),
        )
        self.wait(2)
        # Then I tried to solve the problem manually for this tree. I noticed that if I take this bud [vrchol 5] and put it for example here, I get rid of one leaf, so that is good. 
        sugar(self, example_tree, 5, 10, -1)
        self.play(
            Flash(
                example_tree.vertices[10],
                color=BLUE,
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
        return
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

        rel_pos_5 = 0.5 * UP
        circle5 = CubicBezier(
            ORIGIN,
            1.4 * (2 * LEFT + 2 * DOWN),
            1.4 * (2 * RIGHT + 2 * DOWN),
            ORIGIN,
            color=BLACK
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

        # return back
        sugar(self, example_tree, 2, 1, -2)
        sugar(self, example_tree, 12, 10, 0)
        sugar(self, example_tree, 5, 2, 1)
        sugar(self, example_tree, 12, 11, 0)

        # And that holds in general. I realized that I can imagine repeatedly cutting the buds from the tree in any order like this.

        # TODO more animations
        self.next_section(skip_animations=False)
        self.wait(2)

        sub5 = example_tree.remove_subtree(self, 5)
        self.play(
            sub5.animate().shift(2 * DOWN)
        )

        sub2 = example_tree.remove_subtree(self, 2)
        self.play(
            sub2.animate().shift(1 * DOWN)
        )

        sub12 = example_tree.remove_subtree(self, 12)
        self.play(
            sub12.animate().shift(1 * DOWN)
        )

        sub9 = example_tree.remove_subtree(self, 9)
        self.play(
            sub9.animate().shift(1 * DOWN)
        )
        self.wait()

        # Now I draw the circle around each bud and put them back.

        self.play(
            sub9.animate().shift(1 * UP)
        )
        example_tree.add_subtree(self, sub9, 1)

        self.play(
            sub12.animate().shift(-1 * DOWN)
        )
        example_tree.add_subtree(self, sub12, 11)

        self.play(
            sub2.animate().shift(-1 * DOWN)
        )
        example_tree.add_subtree(self, sub2, 1)

        self.play(
            sub5.animate().shift(-2 * DOWN)
        )
        example_tree.add_subtree(self, sub5, 2)
        # If I now do some random bud-cutting operations, you see that the nodes in the same circle always stay together.

        # TODO more animations

        # Notice that I also colored all of these nodes with a shade of red, because those are the potential buds. By that I think that whenever you see a bud after doing some rehanging operations, it definitely has to be a red node. On the other hand, not all the red nodes are buds, only those that are currently at the bottom of the tree and have the bright red color. I also colored the rest of the nodes blue, because those are the potential leaves. Again, not all blue nodes are leaves, but whenever you see a leaf, it has to be blue. I again give a bright blue color to the actual leaves and otherwise the node gets an opaque blue color.  
        
        #TODO rethink
        self.play(
            *[
                Flash(example_tree.vertices[v], color=RED) for v in red_nodes
            ]
        )
        self.wait()

        self.play(
            *[
                Flash(example_tree.vertices[v], color=BLUE) for v in blue_nodes
            ]
        )
        self.wait()
        
        # Ok, now we understand what rehanging is doing quite well, so what is again the problem we actually want to solve? Right, we want as few leaves as possible. Hm, can we somehow use the fact that leaves are all blue nodes? 
        self.next_section(skip_animations=False)
        blue_nonleaves = [1, 11]
        blue_leaves = [x for x in blue_nodes if x not in blue_nonleaves]

        circles_leaves = [
            Circle(radius=0.3, color=BLUE).move_to(example_tree.vertices[v])
            for v in blue_leaves
        ]
        circles_nonleaves = [
            Circle(radius=0.3, color=BLUE).move_to(example_tree.vertices[v])
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
            ]
        )
        self.wait()

        self.play(
            *[
                Create(c) for c in circles_nonleaves
            ]
        )
        self.wait()

        # These blue nodes are not leaves, because they have at least one red child that covers them. This child needs to be a red node.

        arrows = [
            Arrow(start=example_tree.vertices[1], end=example_tree.vertices[2], color=RED, buff=0.1),
            Arrow(start=example_tree.vertices[1], end=example_tree.vertices[9], color=RED, buff=0.1),
            Arrow(start=example_tree.vertices[11], end=example_tree.vertices[12], color=RED, buff=0.1),
        ]

        self.play(
            *[Create(ar) for ar in arrows]
        )
        self.wait()
        self.play(
            *[Flash(example_tree.vertices[v], color=RED) for v in [2, 9, 12]]
        )
        self.play(
            *[Uncreate(ar) for ar in arrows],
            *[
                Uncreate(c) for c in circles_nonleaves
            ],
        )
        self.wait()

        # At this point I finally realized what was happening when I was trying to solve the problem manually. I started by rehanging this bud, which decreased the number of leaves by one. The reason this worked is that this bud was hung below a red node, which is kind of wasteful. So after I took the bud off, the number of leaves did not increase. 
        
        sugar(self, example_tree, 5, 10, 0)

        ar = Arrow(
            start = ORIGIN,
            end = (1*RIGHT + 1*DOWN)/1.0,
            color = RED,
        ).move_to(
            example_tree.vertices[2].get_center() + (1*LEFT + 1*UP)/2.0
        )
        self.play(
            FadeIn(ar),
        )
        self.wait()

        # Then I used my red node to cover one blue leaf and that decreased the number of leaves by one. 
        
        self.play(
            ar.animate().shift(
                example_tree.vertices[10].get_center()
                - example_tree.vertices[2].get_center()
            )
        )
        self.wait()

        # But there was also this blue node with two red children, which is again kind of wasteful. So when I took this new bud off, I again did not create any new leaf. So I could use my bud to cover one more leaf. 

        self.play(
            ar.animate().shift(
                example_tree.vertices[1].get_center()
                - example_tree.vertices[10].get_center()
            )
        )
        self.wait()
        self.play(
            FadeOut(ar)
        )
        self.wait()

        sugar(self, example_tree, 2, 6, 0)

        # And now it is clear that there is no better solution than having five leaves. That’s because in total we have 9 blue nodes but only four red nodes. These four nodes can cover at most four different blue nodes [šipky z červených do zelených], hence the smallest number of leaves we can hope for is 9-4 which is 5. 

        label_blue = Tex(r"\# blue nodes $= 9$", color = BLUE).move_to(
            4*LEFT + 1*DOWN
        )
        label_red = Tex(r"\# blue nodes $= 4$", color = RED).next_to(label_blue, DOWN)

        self.play(
            *[
                Flash(example_tree.vertices[v], color = BLUE) for v in blue_nodes
            ],
            FadeIn(label_blue)
        )
        self.wait()
        
        self.play(
            *[
                Flash(example_tree.vertices[v], color = RED) for v in red_nodes
            ],
            FadeIn(label_red)
        )
        self.wait()
        
        arrows = [
            Arrow(start = example_tree.vertices[2], end = example_tree.vertices[6], color = RED, buff = 0.1),
            Arrow(start = example_tree.vertices[9], end = example_tree.vertices[1], color = RED, buff = 0.1),
            Arrow(start = example_tree.vertices[12], end = example_tree.vertices[11], color = RED, buff = 0.1),
            Arrow(start = example_tree.vertices[5], end = example_tree.vertices[10], color = RED, buff = 0.1),
        ]
        self.play(
            *[Create(ar) for ar in arrows]
        )
        self.wait()
        self.play(
            *[Uncreate(ar) for ar in arrows]
        )
        self.wait()

        label_dif = Tex(r"\# leaves $\ge 9 - 4 = 5$", color = GRAY).next_to(label_red, DOWN)
        pos9 = 8
        pos4 = pos9 + 2
        
        label_dif[0][10].set_color(RED)

        self.play(
            FadeOut(label_blue[0][:-1]),
            FadeOut(label_red[0][:-1]),
        )
        self.play(
            Succession(
                Write(label_dif[0][0:pos9]),
                label_blue[0][-1].animate().move_to(label_dif[0][pos9].get_center()),
                Write(label_dif[0][pos9+1:pos4]),
                label_red[0][-1].animate().move_to(label_dif[0][pos4].get_center()),
                Write(label_dif[0][pos4+1:]),                
            )
        )

        # Great! So can we always achieve this state where all the red nodes are fully utilized which makes the answer to be the number of blue nodes minus the number of red nodes? 
        # It took me a while to figure it out but turns out we can! [tohle řešení se tam už někdy před tím objeví v random tazích] The solution I came up with was to start by disassembling the whole tree so that all buds are hanging below the root. 
        
        sugar(self, example_tree, 2, 1, -2)
        sugar(self, example_tree, 5, 1, -5)
        sugar(self, example_tree, 12, 1, 5)
               
        # Then, we can just stack them on top of each other like this. This way, every red node is covering a different blue node, so we achieve the best possible bound. 

        sugar(self, example_tree, 9, 13, 0)
        sugar(self, example_tree, 2, 11, 0)
        sugar(self, example_tree, 5, 4, 0)


class Code(Scene):
    def construct(self):
        # Nice! So we have a solution. We simply code a program that first colors the nodes blue and red so that the colors correspond to cutting the buds from our tree one by one. Then we return the number of blue nodes - the number of red nodes as the answer.        

        code = ImageMobject("img/code.png").scale_to_fit_height(8).align_to(Dot().move_to(7.1*LEFT), LEFT)


        dfs_brace = Brace(Line(ORIGIN, 2*DOWN), RIGHT, color = GRAY).move_to(0.5*RIGHT + 2.5*UP)
        input_brace = Brace(Line(ORIGIN, 1.5*DOWN), RIGHT, color = GRAY).next_to(dfs_brace, DOWN)
        run_brace = Brace(Line(ORIGIN, 0.3*DOWN), RIGHT, color = GRAY).next_to(input_brace, DOWN)
        ans_brace = Brace(Line(ORIGIN, 1.0*DOWN), RIGHT, color = GRAY).next_to(run_brace, DOWN)
        testcase_brace = Brace(Line(ORIGIN, 1.0*DOWN), RIGHT, color = GRAY).next_to(ans_brace, DOWN).shift(0.3*DOWN)
        
        dfs_text = Group(
            Tex(r"Compute blue and red nodes; ", color = GRAY).scale(0.5),
            Tex(r"a node is blue if and only if all children are red. ", color = GRAY).scale(0.5)
        ).arrange(DOWN).next_to(dfs_brace, RIGHT)
        dfs_text[0].align_to(dfs_text[1], LEFT)
        input_text = Tex(r"Read the input. ", color = GRAY).scale(0.5).next_to(input_brace, RIGHT)
        run_text = Tex(r"Run the blue/red computation.  ", color = GRAY).scale(0.5).next_to(run_brace, RIGHT)
        ans_text = Tex(r"Compute the number of blue - red nodes. ", color = GRAY).scale(0.5).next_to(ans_brace, RIGHT)
        testcase_text = Tex(r"Solve all testcases. ", color = GRAY).scale(0.5).next_to(testcase_brace, RIGHT)
       

        self.add(
            code,
            dfs_brace,
            input_brace,
            run_brace,
            ans_brace,
            testcase_brace,
            dfs_text,
            input_text,
            run_text,
            ans_text,
            testcase_text,
        )

        self.wait()

        self.remove(*self.mobjects)
        self.add(code)
        

        sample_tree = Tree(
            sample_vertices,
            sample_edges,
            layout=            {
                1: ORIGIN,
                2: H - 2 * sh,
                3: H,
                4: H + 2 * sh,
                5: 2 * H - 3 * 2 * sh / 2,
                6: 2 * H - 2 * sh / 2,
                7: 2 * H + 2 * sh,
            },
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": WHITE},  # for debugging
            labels=True,  # for debugging
            edge_config={"color": text_color},
            root = 1,
        ).move_to(scene_width / 4 * RIGHT + 2 * UP)

        self.play(
            Create(sample_tree),
        )
        self.wait()
        sample_tree.pretty_colour()
        self.wait()

        comp = Tex(r"{{\# blue nodes}}{{ $-$ }}{{ \# red nodes }}", color = GRAY).move_to(sample_tree.get_center() + 4.7*DOWN)
        comp[0].set_color(BLUE)
        comp[2].set_color(RED)
        self.play(FadeIn(comp))
        self.play(
            Transform(comp[0], Tex(r"4", color = BLUE).next_to(comp[1], LEFT)),
        )
        self.play(
            Transform(comp[2], Tex(r"3", color = RED).next_to(comp[1], RIGHT)),
        )

        comp2 = Tex(r"$= 1$", color = GRAY).next_to(comp, RIGHT)
        self.play(FadeIn(comp2))
        self.wait()
        comp3 = Tex(r"Answer = 2", color = GRAY).next_to(Group(comp, comp2), DOWN)
        self.play(FadeIn(comp3))
        self.wait()

        sugar(self, sample_tree, 4, 3, 0)
        sugar(self, sample_tree, 2, 7, 0)
        self.wait()

        ar = Arrow(
            start = ORIGIN,
            end = (1*RIGHT)/1.0,
            color = RED,
        ).move_to(
            sample_tree.vertices[1].get_center() + (1*LEFT)/2.0
        )
        self.play(
            FadeIn(ar)
        )
        self.wait()
        self.play(FadeOut(ar))
        self.wait()

        ar = Arrow(
            start = ORIGIN,
            end = (1*LEFT)/1.0,
            color = RED,
        ).move_to(
            2*DOWN + 0.5 * RIGHT
        )

        self.play(
            FadeIn(ar)
        )
        self.wait()
        self.play(FadeOut(ar))
        self.wait()


        self.wait(10)


class Explore(Scene):
    def construct(self):
        curve = CubicBezier(
            ORIGIN,
            3 * (2 * LEFT + 2 * DOWN),
            3 * (2 * RIGHT + 2 * DOWN),
            ORIGIN,
            color=BLACK
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
