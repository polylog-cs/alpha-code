from util import *

class Intro(Scene):
    def construct(self):
        dalle_images = [
            ImageMobject(path).scale(0.3)
            for path in ["img/D4.png", "img/D3.png", "img/D1.png", "img/D2.png"]
        ]
        dalle_prompts = [
            Tex(txt, color = GRAY).scale(0.3)
            for txt in [
                "A plate with pasta that form a brain as a 1960s poster",
                "A programmer desperately trying to create a funny picture using artificial intelligence",
                "A person standing next to a large tree with many leaves and buds in a vaporwave style",
                "A logo suitable for a youtube channel about computer science",
            ]
        ]

        Group(*dalle_images).arrange_in_grid(
            rows = 2,
            buff = 1
        ).move_to(2*RIGHT)
        for i in range(4):
            dalle_prompts[i].next_to(dalle_images[i], DOWN)

        self.add(
            *dalle_images,
            *dalle_prompts
        )


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
        logo_solarized = ImageMobject("img/logo-solarized.png").scale(0.17).shift(0.3*UP+0.05*LEFT)
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

        forest = Forest(example_tree, solarized.BLUE, solarized.CYAN)

        example_tree.add_updater(lambda x: forest.pretty_colour(solarized.BLUE, solarized.CYAN))

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

        new_tree = forest.remove_subtree_from_tree(0, 3)
        new_tree.add_updater(lambda x: forest.pretty_colour(solarized.BLUE, solarized.CYAN))
        self.add(new_tree)
        self.remove(example_tree)
        self.add(example_tree)

        self.play(
            new_tree.animate().shift(2*LEFT),
            run_time=1
        )
        self.wait(2)

        tr = forest.add_subtree_to_tree(1, 0, 2)
        tr.add_updater(lambda x: forest.pretty_colour(solarized.BLUE, solarized.CYAN))
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

