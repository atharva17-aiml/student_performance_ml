def validate_prediction_inputs(form):
    required_fields = ["studytime", "failures", "absences", "health", "G1", "G2"]

    for field in required_fields:
        if field not in form or form[field].strip() == "":
            raise ValueError(f"{field} is required")

    try:
        studytime = int(form["studytime"])
        failures  = int(form["failures"])
        absences  = int(form["absences"])
        health    = int(form["health"])
        G1        = int(form["G1"])
        G2        = int(form["G2"])
    except ValueError:
        raise ValueError("Inputs must be numbers")

    if not (1 <= studytime <= 5):
        raise ValueError("Study time must be 1–5")

    if not (0 <= failures <= 3):
        raise ValueError("Failures must be 0–3")

    if not (0 <= absences <= 30):
        raise ValueError("Absences must be 0–30")

    if not (1 <= health <= 5):
        raise ValueError("Health must be 1–5")

    if not (0 <= G1 <= 20):
        raise ValueError("G1 must be 0–20")

    if not (0 <= G2 <= 20):
        raise ValueError("G2 must be 0–20")

    # ✅ RETURN LIST (FIX)
    return [studytime, failures, absences, health, G1, G2]
