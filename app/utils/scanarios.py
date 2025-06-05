from utils.JSON import change_json_value, get_value_from_json

def user_win():
    # Обновляем общее количество игр и побед
    total_games = int(get_value_from_json("stats.json", "total_games")) + 1
    change_json_value("stats.json", "total_games", str(total_games))
    total_wins = int(get_value_from_json("stats.json", "total_wins")) + 1
    change_json_value("stats.json", "total_wins", str(total_wins))

    # Получаем текущий уровень сложности
    level = get_value_from_json("app/settings.json", "Settings.Difficulty Level")

    # Обновляем статистику по текущему уровню
    games_played = int(get_value_from_json("app/settings.json", f"difficulty_levels.{level}.games_played")) + 1
    change_json_value("app/settings.json", f"difficulty_levels.{level}.games_played", str(games_played))
    wins = int(get_value_from_json("app/settings.json", f"difficulty_levels.{level}.wins")) + 1
    change_json_value("app/settings.json", f"difficulty_levels.{level}.wins", str(wins))


def user_loss():
    # Обновляем общее количество игр и поражений
    total_games = int(get_value_from_json("app/stats.json", "total_games")) + 1
    change_json_value("app/stats.json", "total_games", str(total_games))
    total_losses = int(get_value_from_json("app/stats.json", "total_losses")) + 1
    change_json_value("app/stats.json", "total_losses", str(total_losses))

    # Получаем текущий уровень сложности
    level = get_value_from_json("app/settings.json", "Settings.Difficulty Level")

    # Обновляем статистику по текущему уровню
    games_played = int(get_value_from_json("app/stats.json", f"difficulty_levels.{level}.games_played")) + 1
    change_json_value("app/stats.json", f"difficulty_levels.{level}.games_played", str(games_played))
    losses = int(get_value_from_json("app/stats.json", f"difficulty_levels.{level}.losses")) + 1
    change_json_value("app/stats.json", f"difficulty_levels.{level}.losses", str(losses))