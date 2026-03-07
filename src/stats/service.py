from datetime import date, timedelta

def calculate_streaks(dates: list[date]) -> dict:
    if not dates:
        return {"current_streak": 0, "max_streak": 0}
    
    dates = sorted(dates)

    max_streak = 1
    streak = 1

    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + timedelta(days=1):
            streak += 1
        else:
            streak = 1
        max_streak = max(max_streak, streak)
    
    current_streak = 1
    for i in range(len(dates) - 1, 0, -1):
        if dates[i] == dates[i - 1] + timedelta(days=1):
            current_streak += 1
        else:
            break

    return {"current_streak": current_streak, "max_streak": max_streak}