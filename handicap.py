def calculate_differential(score, course_rating, slope_rating):

    differential = (113 / slope_rating) * (score - course_rating)

    return round(differential, 2)


def calculate_handicap(rounds):

    if len(rounds) < 3:
        return "N/A"

    differentials = [round[6] for round in rounds]

    differentials.sort()

    best = differentials[:8] if len(differentials) >= 8 else differentials

    handicap = sum(best) / len(best)

    return round(handicap, 1)


def handicap_progression(rounds):

    progression = []

    for i in range(len(rounds)):

        subset = rounds[:i + 1]

        if len(subset) < 3:
            progression.append(None)
            continue

        diffs = [r[6] for r in subset]

        diffs.sort()

        best = diffs[:8] if len(diffs) >= 8 else diffs

        handicap = sum(best) / len(best)

        progression.append(round(handicap, 1))

    return progression