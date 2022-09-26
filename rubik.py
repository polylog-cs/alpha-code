import random
from manim import *

# Use our fork of manim_rubikscube!
from cube import *

# This also replaces the default colors
import solarized

from util_cube import *
from util import *
import itertools

class Rubik(RubikScene):
    def construct(self):
        # By the way, using the simple tree as an intermediary is an instance of a more general trick that is sometimes useful in math or competitive programming. For example, let’s say I ask you to come up with a sequence of moves that brings this scramble of Rubik’s cube to that one. Well, if you can work out how to solve both the first cube and the second cube, you can simply revert the second solution, bring them together and you are done. 


        cube_distance = 13
        cubie_size = 0.25
        down_shift = 2*DOWN
        cube_from = RubiksCube(cubie_size=cubie_size, rotate_nicely=True).shift(
            LEFT * cube_distance / 2 + down_shift
        )
        cube_to = RubiksCube(cubie_size=cubie_size, rotate_nicely=True).shift(
            RIGHT * cube_distance / 2 + down_shift
        )
        cube_mid = RubiksCube(cubie_size=cubie_size, rotate_nicely=True).shift( + down_shift)

        scramble(cube_from, unscramble1)
        scramble(cube_to, unscramble2)

        self.play(
            FadeIn(cube_from)
        )
        self.wait()
        self.play(
            FadeIn(cube_to)
        )
        self.wait()
        self.play(
            FadeIn(cube_mid)
        )
        self.wait()

        cubes = [cube_from]
        arrows = []
        cur_cube = cube_from
        ar_shift = 1*DOWN

        for i in range(len(scramble1)):
            new_cube = cur_cube.copy()
            self.add(new_cube)
            a = Arrow(
                cur_cube.get_center() + ar_shift,
                cur_cube.get_center() + ar_shift + (cube_mid.get_center() - cube_from.get_center())/(len(scramble1)),
                buff = 0.2,
                color = RED
            )
            self.add_sound(random_rubik_file(), time_offset = 0.0)
            self.play(
                CubeMove(new_cube, scramble1[i], 
                    (
                        cube_mid.get_center() * i * 1.0 /len(scramble1) 
                    + cube_from.get_center() * (len(scramble1) - 1.0 - i)/len(scramble1)
                    )[0]*RIGHT + cube_mid.get_center()[1]*UP
                ),
                Create(a),
                run_time=1 / 3,
            )
            cubes.append(new_cube)
            arrows.append(a)
            cur_cube = new_cube      

        self.wait()

        cur_cube = cube_to
        for i in range(len(scramble2)):
            new_cube = cur_cube.copy()
            self.add(new_cube)
            a = Arrow(
                cur_cube.get_center() + ar_shift,
                cur_cube.get_center() + ar_shift + (cube_mid.get_center() - cube_to.get_center())/(len(scramble1)),
                buff = 0.2,                
                color = BLUE
            )            
            self.add_sound(random_rubik_file(), time_offset = 0.0)
            self.play(
                CubeMove(new_cube, scramble2[i], 
                (cube_mid.get_center()*i/(len(scramble2)) + cube_to.get_center()*(len(scramble2) - 1.0 - i)/(len(scramble2)))[0]*RIGHT + cube_mid.get_center()[1]*UP),
                Create(a),
                run_time=1 / 3,
            )

            cubes.append(new_cube)
            arrows.append(a)            
            cur_cube = new_cube      

        self.wait()

        anims = []
        for a in arrows[-len(scramble2):]:
            anims.append(
                Transform(
                    a,
                    Arrow(
                        a.get_left(),
                        a.get_right(),
                        buff = 0.0,                        
                        color = RED
                    )
                )
            )
        self.play(
            *anims
        )
        self.wait()

        # In general, if you want to transform one complicated object into another complicated object using some operations, it sometimes suffices to come up with a simple intermediate object and only work out how to transform complicated objects to the simple one. 

        self.play(
            Circumscribe(cube_mid, color = RED)
        )
        self.wait()

        self.play(
            Circumscribe(cube_from, color = RED),
            Circumscribe(cube_to, color = RED)
        )
        self.wait()
