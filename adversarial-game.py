MOVES = 100
FLIP_BUDGET = 40


def swap(play):
    if play == "c":
        return "d"
    return "c"


def score(prisoners, flippers):
    prisoner_scores = [0 for _ in prisoners]
    flipper_scores = [0 for _ in flippers]
    for index1, prisoner1 in enumerate(prisoners):
        for index2, prisoner2 in enumerate(prisoners):
            for index_f, flipper in enumerate(flippers):
                p1_score = 0
                p1_state = []
                p1_plays = []
                p1_flipped = []

                p2_score = 0
                p2_state = []
                p2_plays = []
                p2_flipped = []

                f_score = 0
                f_state = []
                flips_remaining = FLIP_BUDGET
                for _ in range(MOVES):
                    p1_play = prisoner1(p1_plays, p2_flipped, p1_state)
                    p2_play = prisoner2(p2_plays, p1_flipped, p2_state)
                    p1_plays.append(p1_play)
                    p2_plays.append(p2_play)
                    f_play = 0
                    if flips_remaining > 0:
                        f_play = flipper(
                            p1_plays,
                            p1_flipped,
                            p2_plays,
                            p2_flipped,
                            flips_remaining,
                            f_state,
                        )
                    if f_play == 3 and flips_remaining == 1:
                        f_play = 1
                    if p1_play == "c":
                        p2_score += 2
                    else:
                        p1_score += 1
                        f_score += 1
                    if p2_play == "c":
                        p1_score += 2
                    else:
                        p2_score += 1
                        f_score += 1
                    p1_flip = p1_play if f_play % 2 == 0 else swap(p1_play)
                    p2_flip = p2_play if f_play < 2 else swap(p2_play)

                    p1_flipped.append(p1_flip)
                    p2_flipped.append(p2_flip)
                    flips_remaining -= (f_play + 1) // 2
                    assert flips_remaining >= 0
                if False:  # Debug information
                    print(prisoner1.__name__, prisoner2.__name__, flipper.__name__)
                    print(p1_score, p2_score, f_score, flips_remaining)
                prisoner_scores[index1] += p1_score
                prisoner_scores[index2] += p2_score
                flipper_scores[index_f] += f_score
    return (prisoner_scores, flipper_scores)


WIDTH = 30


def print_scores(scores, prisoners, flippers):
    prisoner_scores, flipper_scores = scores
    print("Prisoners:")
    sorted_scores = sorted(zip(prisoners, prisoner_scores), key=lambda p: -p[1])
    for prisoner, total_score in sorted_scores:
        average_score = total_score / (2 * len(prisoners) * len(flippers))
        name = prisoner.__name__
        if len(name) > WIDTH:
            name = name[: WIDTH - 3] + "..."
        print("{}: {}{:.6}".format(name, (WIDTH - len(name)) * " ", average_score))
    print("\nFlippers:")
    sorted_scores = sorted(zip(flippers, flipper_scores), key=lambda p: -p[1])
    for flipper, total_score in sorted_scores:
        average_score = total_score / (len(prisoners) ** 2)
        name = flipper.__name__
        if len(name) > WIDTH:
            name = name[: WIDTH - 3] + "..."
        print("{}: {}{:.6}".format(name, (WIDTH - len(name)) * " ", average_score))


if __name__ == "__main__":
    from basic import (
        basic_cooperate,
        basic_defect,
        basic_tit_for_tat,
        basic_tit_for_two_tats,
        basic_threshold,
        basic_steady_flipper,
        basic_random_flipper,
        basic_immediate_flipper,
        basic_non_flipper,
        basic_biased_flipper,
    )
    from submissions import (
        use_their_response_unless_they_are_foolish,
        holding_a_grudge,
        slightly_vindictive,
        detect_evil,
        paranoia_pattern,
        basic_evil_p1_flipper,
        advanced_evil_p1_flipper,
        tempting_trickster,
    )

    prisoners = [
        basic_cooperate,
        basic_defect,
        basic_tit_for_tat,
        basic_tit_for_two_tats,
        basic_threshold,
        use_their_response_unless_they_are_foolish,
        holding_a_grudge,
        slightly_vindictive,
        detect_evil,
    ]
    flippers = [
        basic_steady_flipper,
        basic_random_flipper,
        basic_immediate_flipper,
        basic_non_flipper,
        basic_biased_flipper,
        paranoia_pattern,
        basic_evil_p1_flipper,
        advanced_evil_p1_flipper,
        tempting_trickster,
    ]
    scores = score(prisoners, flippers)
    print_scores(scores, prisoners, flippers)
