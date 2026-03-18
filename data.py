# ゲームデータ格納用モジュール

# ユニット種別の定義例
UNIT_TYPES = {
    "歩兵(矛)": {"cost": 1, "attack": 1, "range": 1, "move": 3},
    "歩兵(戟)": {"cost": 1.2, "attack": 1, "range": 1, "move": 3},
    "弩兵": {"cost": 4, "attack": 0.6, "range": 5, "move": 2},
    "対騎陣": {"cost": 2, "attack": 2, "range": 1, "move": 2},  # 対騎兵特攻
    "軽騎兵": {"cost": 20, "attack": 1.5, "range": 1, "move": 6},
    "重騎兵": {"cost": 100, "attack": 3, "range": 1, "move": 4},
}

# シナリオデータ例
SCENARIOS = {
    "界橋の戦い": {
        "date": "192年1月",
        "player_army": [
            {"type": "対騎陣", "groups": 20, "commander": "麹義"},
            {"type": "弩兵", "groups": 7, "commander": "文醜"},
            {"type": "弩兵", "groups": 6, "commander": "顔良"},
            {"type": "歩兵(戟)", "groups": 400, "commander": "袁紹"},
        ],
        "enemy_army": [
            {"type": "歩兵(矛)", "groups": 750, "commander": "厳綱"},
            {"type": "軽騎兵", "groups": 60, "commander": "公孫瓚"},
            {"type": "軽騎兵", "groups": 60, "commander": "公孫範"},
        ],
    }
}
