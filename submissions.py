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
