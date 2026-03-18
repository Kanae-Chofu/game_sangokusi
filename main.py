from unit import Unit, Army
from battle import Battle


def main():
    # 袁紹軍（プレイヤー）
    player_units = [
        Unit("対騎陣", 20, "麹義"),
        Unit("弩兵", 7, "文醜"),
        Unit("弩兵", 6, "顔良"),
        Unit("歩兵(戟)", 400, "袁紹"),
    ]
    player_army = Army("袁紹軍", player_units)

    # 公孫瓚軍（敵）
    enemy_units = [
        Unit("歩兵(矛)", 750, "厳綱"),
        Unit("軽騎兵", 60, "公孫瓚"),
        Unit("軽騎兵", 60, "公孫範"),
    ]
    enemy_army = Army("公孫瓚軍", enemy_units)

    battle = Battle(player_army, enemy_army)
    battle.start()


if __name__ == "__main__":
    main()
