def calculate_score(result):
    base_score = 10.0
    time_score = 10.0

    actual_time = round(float(result["total_run_time"].split()[0]), 2)

    time_score = max(0, time_score - actual_time)

    total_score = base_score + time_score
    return round(min(20, max(0, total_score)), 2)
