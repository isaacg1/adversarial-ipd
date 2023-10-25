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
