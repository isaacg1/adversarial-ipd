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
