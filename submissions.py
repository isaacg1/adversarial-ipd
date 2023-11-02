# Prisoners
def use_their_response_unless_they_are_foolish(my_plays, their_flipped_plays, state):
    # play "c" at beginning
    if not len(my_plays):
        return "c"
    # play "d" at last few turns
    if len(my_plays) > 96:
        return "d"
    # if op always answer "c", we can cheat on it
    if 60 < len(my_plays) < 1.8 * their_flipped_plays.count("c"):
        return "d"
    # otherwise, play 'c' they play 'c'
    if their_flipped_plays[-4:].count("c") >= 2:
        return "c"
    # or randomly select a response from their past behavior
    rand = their_flipped_plays * 5 + ["c", "d"]
    return rand[
        (int("0x" + "".join(their_flipped_plays), 16) ^ 17 ** len(my_plays)) % len(rand)
    ]


def holding_a_grudge(my_plays, their_flipped_plays, state):
    # First cooperate for 7 plays:
    if len(my_plays) < 7:
        return "c"

    # If 3 or more of their first 7 plays were defects,
    # hold a grudge for the entire round and keep defecting as well:
    amountOfDefects = their_flipped_plays[:7].count("d")
    if amountOfDefects >= 3:
        return "d"

    # If none of their first 7 plays were defects, always cooperate yourself:
    if amountOfDefects == 0:
        return "c"

    # Otherwise, cooperate 3/4th of the times:
    rand = (int("0x" + "".join(their_flipped_plays), 16) ^ 17 ** len(my_plays)) % 100
    if rand >= 25:
        return "c"
    return "d"


def slightly_vindictive(my_plays, their_flipped_plays, state):
    # play nice(-ish) if they've ever cooperated
    if "c" in their_flipped_plays:
        # defect twice when they defect once
        if "d" in their_flipped_plays[-2:]:
            return "d"
        return "c"
    # wait up to 10 turns for opponent to cooperate
    if len(my_plays) <= 10:
        return "c"
    return "d"


def detect_evil(my_plays, their_plays, state):
    turn = len(their_plays)
    # Batter through the flipper by sending more than 20 "c"s to start:
    if turn < 22:
        return "c"

    # Defect last few turns, just because
    if turn > 96:
        return "d"

    # See if it is plausible that they are always cooperating.  If so, cooperate:
    their_coop = their_plays.count("c")
    if their_coop + 20 >= turn:
        return "c"

    # seed possible returns to cooperation around the half-way point:
    if turn > 49 and ((turn % 7) == 0):
        return "c"

    # Try to return to cooperation state if they "c"'d last turn in response
    # or in coordination with my "c":
    if (their_plays[-1:] == ["c"]) and (my_plays[-2:].count("c") > 0):
        return "c"

    # Assume flipper flips 20 "c" to "d" on their side:
    their_defect = their_plays.count("d")
    their_defect_min = their_defect - 20
    their_defect_chance = their_defect_min / turn if (turn > 0) else 0

    # Assume flipper flips 20 "c" to "d" on my side:
    my_defect = my_plays.count("d")
    my_defect_max_count = my_defect + 20
    my_defect_chance = my_defect_max_count / turn if (turn > 0) else 0

    # Tit-tit-tit for tat, but only if they are probably defecting more than
    # they see me defecting:
    if their_plays[-3:].count("d") > 0:
        if my_defect_chance < their_defect_chance:
            return "d"

    # Otherwise, assume the best:
    return "c"


def masquerade(my_plays, their_flipped_plays, state):
    turn = len(my_plays)
    if turn == 0:
        return "c"
    elif turn == 2:
        return "d"
    elif turn < 7:
        return "c"

    self_patterns = [
        # basic_biased_flipper
        ["d", "d", "c", "d", "d", "d", "d"],
        # paranoia_pattern
        ["d", "c", "c", "c", "d", "c", "d"],
        ["d", "c", "d", "d", "c", "d", "c"],
    ]

    # self-detection
    if (
        their_flipped_plays[2] == "d"
        and their_flipped_plays[1:7].count("d") < 3
        and
        # avoid getting tricked by tempting_trickster
        not their_flipped_plays[:3] == ["d", "d", "d"]
    ) or their_flipped_plays[:7] in self_patterns:
        return "c"

    # defect for the last few turns
    if turn > 65:
        return "d"

    # if they often defect, defect as well
    if their_flipped_plays.count("d") > 0.3 * len(their_flipped_plays):
        return "d"

    # tit-tit for tat
    # inspired by slightly vindictive
    if "d" in their_flipped_plays[-2:]:
        return "d"

    return "c"


def tit_forty_tat(my_plays, their_plays, state):
    defects = their_plays.count("d")
    if defects > 40:
        return their_plays[-1]
    else:
        return "c"


def blind_rage(my_plays, their_plays, state):
    if not state:
        # Start in a good mood
        state.append(0)
        return "c"

    if state[0] >= 5:
        # Calming down...
        state[0] = 0
        return "c"

    if state[0]:
        # Rage mode
        state[0] += 1
        return "d"

    if their_plays[-1] == "d":
        # "You dare defect against me? I'll show you!"
        state[0] += 1
        return "d"

    # Normal course of operation.
    return "c"


def stuck_buttons(my_plays, their_plays, state):
    if not state:
        state.append(4)
        state.append(-1)
        return "c"

    if state[0]:
        state[0] -= 1
        return my_plays[-1]
    else:
        state[0] = 4
        state[1] += 1
        return their_plays[state[1]]


def string_prisoner(my_plays, their_plays, state):
    s = "zbemvqjmwqozghuxgymklypogluxxnfvdzcmcusncnsqnuktdhxesvaipgyphcpfgmirmmqlahnkofttkcshrbpvslqngmkjmspkrdzujs"
    if state:
        i = "cd".index(my_plays[-1])
        j = "cd".index(their_plays[-1])
    else:
        state.append(18)
        i, j = 1, 0
    h = state[-1]
    h = ord(s[4 * h + 2 * i + j]) - 97
    state[0] = h
    return "cd"[h % 2]


# Flippers
def paranoia_pattern(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    turn = len(p1_moves)
    match turn:
        case 1:
            # Don't let them get off on the right foot
            return 3

        case 2:
            # And don't let them get used to it
            return 0

        case _ if flips_left > 4:
            # Then alternate aggressively...
            return 1 << (turn % 2)

        case 65 | 66:
            # and finally throw them back off if they've gotten used to the break.
            return 3

        case _:
            return 0


def basic_evil_p1_flipper(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    out = 0
    if p1_moves[-1] == "c":
        out += 1
    return out


def advanced_evil_p1_flipper(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    out = 0
    if p1_moves[-1] == "c":
        out += 1
    turn = len(p1_flipped_moves)
    turns_left = 100 - turn
    p1_coop = p1_moves.count("c")
    p1_visible = p1_flipped_moves.count("c")
    p1_flips_used = p1_coop - p1_visible
    p1_coop_percent = p1_coop / turn if turn > 0 else p1_coop

    p2_coop = p2_moves.count("c")
    p2_visible = p2_flipped_moves.count("c")
    p2_flips_used = p2_coop - p2_visible

    flips_left = 40 - p1_flips_used - p2_flips_used

    if p2_coop <= 10 or (flips_left > (p1_coop_percent * turns_left)):
        if p2_moves[-1] == "c":
            out += 2

    return out


def tempting_trickster(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    # Tease them a bit
    target = "dc"[len(p1_moves) <= 3]

    move = p1_moves[-1] == target
    move |= (p2_moves[-1] == target) << 1
    return move


def basic_mod_4_flipper(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    return len(p1_flipped_moves) % 4


def string_flipper(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    s = "wvwyhbwyjplcvuowuuwyobcyunxypirmhisyxmsenxqypkcyomgqwnuaomrypzkyxnwblegqdssijkbhnjywnnmrpzwygxsepbwypfsysn"
    if state:
        i = "cd".index(p1_moves[-1])
        j = "cd".index(p2_moves[-1])
    else:
        state.append(13)
        i, j = 0, 1
    h = state[-1]
    h = ord(s[4 * h + 2 * i + j]) - 97
    state[0] = h
    return h % 4


# Shared pair: Neural Network
import math


def sigmoid(z):
    z = max(-60.0, min(60.0, 5.0 * z))
    return 1.0 / (1.0 + math.exp(-z))


def eval_nn(nn, inputs, output_size):
    values = {}
    for i, x in enumerate(inputs):
        values[~i] = x
    for v, bias, links in nn:
        val = bias
        for v2, w in links:
            val += values[v2] * w
        values[v] = sigmoid(val)
    return [values[i] for i in range(output_size)]


def flipper_nn(p1_plays, p1_flipped, p2_plays, p2_flipped, flips_remaining, f_state):
    flipper = [
        (
            2,
            1.1181821042173234,
            [
                (-4, 1.7400885547178728),
                (-5, -0.06813411778649736),
                (-1, 0.36820555967416463),
            ],
        ),
        (1413, 0.5463770972701019, [(-7, 1.2906662332985084)]),
        (1006, -0.7872435180237973, [(-1, 0.15812448989961483)]),
        (
            400,
            0.8765368123690065,
            [
                (-1, -0.5507089170354788),
                (-4, -2.6155008235530275),
                (-6, -0.13973123898832307),
                (1413, 0.611948590243875),
            ],
        ),
        (
            4,
            -0.7227321303517735,
            [
                (-5, 1.5683558624231078),
                (-6, -1.2370613914091573),
                (-4, 0.5237132563743849),
                (1006, -0.32865555879156394),
            ],
        ),
        (
            0,
            -0.8037738878771841,
            [
                (400, -1.539896544478685),
                (-6, -1.2406408935562372),
                (-2, 1.4008065675860095),
                (-5, 1.3368457316858942),
            ],
        ),
        (1241, 2.8053793783985843, [(400, -1.1720600247508444)]),
        (
            3,
            -0.6671763505247656,
            [
                (-7, 1.3637083521769713),
                (-2, 0.23978597611290645),
                (400, 0.07355299289323734),
                (-5, 1.4847572012033936),
            ],
        ),
        (
            5,
            1.3240920945810233,
            [
                (-3, 0.09279702179768222),
                (-4, -0.42695177997561584),
                (400, 0.01877521376790067),
            ],
        ),
        (
            1,
            1.4532564361954763,
            [
                (-4, -3.3511395309047542),
                (-6, 3.4483449908621946),
                (400, -0.30914255807222707),
                (-1, 4.416629240437298),
                (1241, -3.2869409990358784),
            ],
        ),
    ]
    if not f_state:
        f_state.append([0, 0, 0, 0])
    p1_play = 1 if p1_plays[-1] == "c" else -1
    p2_play = 1 if p2_plays[-1] == "c" else -1
    d1, d2, *f_state[0] = eval_nn(
        flipper, [p1_play, p2_play, flips_remaining, *f_state[0]], 6
    )
    return 2 * (d1 > 0.5) + (d2 > 0.5)


def prisoner_nn(p1_plays, p2_flipped, p1_state):
    prisoner = [
        (
            0,
            -2.2128141878495886,
            [
                (-2, 0.647135699564962),
                (-1, -3.819879756972317),
                (-6, -1.5898309666275279),
                (-5, -1.3569920659927621),
            ],
        ),
        (
            2,
            -0.026842109156755112,
            [
                (-6, 1.9088324301092459),
                (-1, -1.498237595085962),
                (-2, -1.3979942638308056),
            ],
        ),
        (
            3,
            -1.4642587337125894,
            [(-5, 0.027435320810760975), (-3, 0.8940799124862344)],
        ),
        (
            5,
            -1.5627901857506785,
            [
                (-7, -0.3885493442923349),
                (-4, -0.6468723685254656),
                (-6, 0.4827740033482678),
                (-1, 1.0907376062753547),
            ],
        ),
        (3655, -0.6335740926081981, [(-3, -1.131136914882346)]),
        (
            4,
            0.030539518044983505,
            [
                (-4, 0.6436349726871196),
                (-6, -0.7427970484374815),
                (3655, -0.23969124478552287),
            ],
        ),
        (1, 0, []),
    ]
    if not p1_state:
        p1_state.append([0, 0, 0, 0, 0])
    lastact = (1 if p2_flipped[-1] == "c" else -1) if p2_flipped else 0
    lastsact = (1 if p1_plays[-1] == "c" else -1) if p1_plays else 0
    act, *p1_state[0] = eval_nn(prisoner, [lastsact, lastact, *p1_state[0]], 6)
    return ["d", "c"][act > 0.5]


# Shared pair: Less-deterministic
def less_deterministic_prisoner(my_plays, their_plays, state):
    if not state:
        state.append(0xE1)  # Initial state
        state.append(8)  # Whether to collect more info for seed
        state.append(False)  # PRNG has been initialized?

        return "c"

    if state[1]:
        # Seed the PRNG with the data we get
        state[0] <<= 1
        state[0] |= their_plays[-1] == "d"
        state[1] -= 1

        return "c"

    if not state[2]:
        # XOR with some data for some good old security through obscurity.
        state[0] ^= 0x03
        state[2] = True

    # PRNG is properly seeded now!
    my_choice = (state[0] & 0x8000) >> 15

    tap16 = (state[0] & 0x8000) >> 15
    tap15 = (state[0] & 0x4000) >> 14
    tap13 = (state[0] & 0x1000) >> 12
    tap4 = (state[0] & 0x0008) >> 3

    feedback = tap16 ^ tap15 ^ tap13 ^ tap4

    state[0] <<= 1
    state[0] &= 0xFFFF
    state[0] |= feedback

    return "cd"[my_choice]


def less_deterministic_flipper(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    if not state:
        state.append(0x21)  # Initial state
        state.append(4)  # Whether to collect more info for seed
        state.append(False)  # PRNG has been initialized?

        return 0

    if state[1]:
        # Seed the PRNG with the data we get
        state[0] <<= 1
        state[0] |= p1_moves[-1] == "d"
        state[0] <<= 1
        state[0] |= p2_moves[-1] == "d"
        state[1] -= 1

        return 0

    if not state[2]:
        # XOR with some data for some good old security through obscurity.
        state[0] ^= 0x44
        state[2] = True

    # PRNG is properly seeded now!
    first_bit = (state[0] & 0x8000) >> 15

    tap16 = (state[0] & 0x8000) >> 15
    tap15 = (state[0] & 0x4000) >> 14
    tap13 = (state[0] & 0x1000) >> 12
    tap4 = (state[0] & 0x0008) >> 3

    feedback = tap16 ^ tap15 ^ tap13 ^ tap4

    state[0] <<= 1
    state[0] &= 0xFFFF
    state[0] |= feedback

    second_bit = (state[0] & 0x8000) >> 15

    tap16 = (state[0] & 0x8000) >> 15
    tap15 = (state[0] & 0x4000) >> 14
    tap13 = (state[0] & 0x1000) >> 12
    tap4 = (state[0] & 0x0008) >> 3

    feedback = tap16 ^ tap15 ^ tap13 ^ tap4

    state[0] <<= 1
    state[0] &= 0xFFFF
    state[0] |= feedback

    # Use the two bits to make a choice
    choice = first_bit << 1
    choice |= second_bit

    return choice
