from ui import BattleUI
import random


class Battle:
    """複数ユニット対応バトルシステム"""
    def __init__(self, player_army, enemy_army):
        self.player_army = player_army
        self.enemy_army = enemy_army
        self.turn = 0
        self.log_messages = []
        self.ui = BattleUI(self)

    def start(self):
        self.ui.run()

    def player_attack(self, player_unit_idx: int):
        """プレイヤー軍のユニットが敵を攻撃"""
        player_unit = self.player_army.units[player_unit_idx]
        if not player_unit.is_alive():
            return None
        
        # 敵ユニットをランダムに選択
        alive_enemies = self.enemy_army.get_alive_units()
        if not alive_enemies:
            return None
        
        target = random.choice(alive_enemies)
        damage = player_unit.calc_attack_damage()
        target.take_damage(damage)
        
        msg = f"{player_unit.commander}({player_unit.unit_type}) が {target.commander} に {damage} ダメージ！"
        self.log_messages.append(msg)
        return msg

    def enemy_attack(self):
        """敵軍が攻撃"""
        alive_enemies = self.enemy_army.get_alive_units()
        if not alive_enemies:
            return None
        
        attacker = random.choice(alive_enemies)
        alive_players = self.player_army.get_alive_units()
        if not alive_players:
            return None
        
        target = random.choice(alive_players)
        damage = attacker.calc_attack_damage()
        target.take_damage(damage)
        
        msg = f"{attacker.commander}({attacker.unit_type}) が {target.commander} に {damage} ダメージ！"
        self.log_messages.append(msg)
        return msg

    def is_over(self) -> bool:
        """バトル終了判定"""
        return self.player_army.is_defeated() or self.enemy_army.is_defeated()

    def get_winner(self):
        """勝者を返す"""
        if self.enemy_army.is_defeated():
            return "player"
        elif self.player_army.is_defeated():
            return "enemy"
        return None
