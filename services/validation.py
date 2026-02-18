def validate_prediction_inputs(form):
    rules = {
        "studytime": (1, 4),
        "failures": (0, 10),
        "absences": (0, 100),
        "health": (1, 5),
        "G1": (0, 20),
        "G2": (0, 20)
    }

    values = []

    for field, (min_v, max_v) in rules.items():
        if field not in form:
            raise ValueError(f"Missing field: {field}")

        try:
            value = int(form[field])
        except:
            raise ValueError(f"{field} must be a number")

        if value < min_v or value > max_v:
            raise ValueError(f"{field} must be between {min_v} and {max_v}")

        values.append(value)

    return values
