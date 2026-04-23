def calculate_differential(score, course_rating, slope_rating):

    # Calculate the score differential from score, course rating, and slope rating
    differential = (113 / slope_rating) * (score - course_rating)

    return round(differential, 2)


def calculate_handicap(rounds):

    # Return no handicap if fewer than 3 rounds have been recorded
    if len(rounds) < 3:
        return "N/A"

    # Extract all round differentials for handicap calculation
    differentials = [round[6] for round in rounds]

    # Sort differentials from lowest to highest
    differentials.sort()

    # Use the best 8 differentials or all available if fewer than 8 exist
    best = differentials[:8] if len(differentials) >= 8 else differentials

    # Calculate the average of the selected best differentials
    handicap = sum(best) / len(best)

    return round(handicap, 1)


def handicap_progression(rounds):

    # Store the handicap value after each round is added
    progression = []

    # Recalculate handicap step by step across the round history
    for i in range(len(rounds)):

        subset = rounds[:i + 1]

        # Add no handicap value until at least 3 rounds exist
        if len(subset) < 3:
            progression.append(None)
            continue

        # Extract and sort differentials for the current subset of rounds
        diffs = [r[6] for r in subset]

        diffs.sort()

        # Use the best 8 differentials or all available if fewer than 8 exist
        best = diffs[:8] if len(diffs) >= 8 else diffs

        # Calculate the handicap for the current stage of progression
        handicap = sum(best) / len(best)

        progression.append(round(handicap, 1))

    return progression