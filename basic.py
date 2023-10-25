# Prisoners
def basic_tit_for_tat(my_plays, their_plays, state):
    if len(their_plays) == 0:
        return "c"
    return their_plays[-1]


def basic_tit_for_two_tats(my_plays, their_plays, state):
    if len(their_plays) < 2:
        return "c"
    if their_plays[-2:] == ["d", "d"]:
        return "d"
    return "c"


def basic_cooperate(my_plays, their_plays, state):
    return "c"


def basic_defect(my_plays, their_plays, state):
    return "d"


def basic_threshold(my_plays, their_flipped_plays, state):
    if len(their_flipped_plays) < 10:
        return "c"
    opp_c_freq = their_flipped_plays.count("c") / len(their_flipped_plays)
    if opp_c_freq > 0.6:
        return "c"
    else:
        return "d"


# Flippers
def basic_steady_flipper(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    turn = len(p1_flipped_moves)
    if turn % 5 == 0 and p1_moves[-1] == "c":
        return 1
    if turn % 5 == 2 and p2_moves[-1] == "c":
        return 2
    return 0


def basic_random_flipper(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    old_random = 1 if len(state) == 0 else state[0]
    # Xorshift 32
    new_random = old_random
    new_random ^= (new_random << 13) % 2**32
    new_random ^= new_random >> 17
    new_random ^= (new_random << 5) % 2**32
    if len(state) == 0:
        state.append(new_random)
    else:
        state[0] = new_random
    flip1 = new_random % 5 == 0
    flip2 = (new_random % 25) // 5 == 0
    out = 0
    if flip1:
        out += 1
    if flip2:
        out += 2
    return out


def basic_immediate_flipper(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    out = 0
    if p1_moves[-1] == "c":
        out += 1
    if p2_moves[-1] == "c":
        out += 2
    return out


def basic_non_flipper(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    return 0


def basic_biased_flipper(
    p1_moves, p1_flipped_moves, p2_moves, p2_flipped_moves, flips_left, state
):
    return 1
