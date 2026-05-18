from datetime import date, timedelta
from skills.schemas import Skills


def calculate_streak(skill: Skills, today: date) -> dict:
    current_streak = skill["current_streak"]
    max_streak = skill["max_streak"]
    last_date = skill["last_log_date"]

    if last_date:
        last_date = date.fromisoformat(last_date)
        if last_date == today:
            return None
        elif last_date == today - timedelta(days=1):
            current_streak += 1
        else:
            current_streak = 1
    else:
        current_streak = 1

    max_streak = max(max_streak, current_streak)

    return {"current_streak": current_streak, "max_streak": max_streak}

def calculate_xp(skill_xp: int) -> int:
    return skill_xp + 1