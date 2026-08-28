# ============================================
# HYBRID LANDSLIDE EARLY WARNING ENGINE
# ============================================


def calculate_warning(
    ml_probability,
    rainfall_next_24h,
    rain_probability
):

    score = 0


    # ========================================
    # 1. ML LANDSLIDE PROBABILITY
    # ========================================

    if ml_probability >= 75:

        score += 4

    elif ml_probability >= 50:

        score += 3

    elif ml_probability >= 25:

        score += 2

    else:

        score += 1


    # ========================================
    # 2. 24-HOUR RAINFALL
    # ========================================

    if rainfall_next_24h >= 100:

        score += 4

    elif rainfall_next_24h >= 50:

        score += 3

    elif rainfall_next_24h >= 20:

        score += 2

    else:

        score += 1


    # ========================================
    # 3. RAIN PROBABILITY
    # ========================================

    if rain_probability >= 80:

        score += 3

    elif rain_probability >= 60:

        score += 2

    else:

        score += 1


    # ========================================
    # FINAL WARNING LEVEL
    # ========================================

    if score >= 9:

        warning = "VERY HIGH"

    elif score >= 7:

        warning = "HIGH"

    elif score >= 5:

        warning = "MODERATE"

    else:

        warning = "LOW"


    return {
        "score": score,
        "warning": warning
    }


# ============================================
# TEST
# ============================================

if __name__ == "__main__":

    result = calculate_warning(
        ml_probability=10,
        rainfall_next_24h=5,
        rain_probability=20
    )


    print()
    print("HYBRID EARLY WARNING")
    print("============================")

    print(
        "ML Probability:",
        75,
        "%"
    )

    print(
        "Rainfall next 24h:",
        82,
        "mm"
    )

    print(
        "Rain probability:",
        95,
        "%"
    )

    print(
        "Warning score:",
        result["score"]
    )

    print(
        "FINAL WARNING:",
        result["warning"]
    )