import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk


class BattleUI:
    def __init__(self, battle):
        self.battle = battle
        self.player_army = battle.player_army
        self.enemy_army = battle.enemy_army
        self.selected_player_unit_idx = 0
        self.selected_enemy_unit_idx = 0

        self.window = tk.Tk()
        self.window.title("袁譚RPG バトル - 複数ユニット")
        self.window.geometry("1000x600")

        # フレーム分割
        self.top_frame = tk.Frame(self.window)
        self.top_frame.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

        self.middle_frame = tk.Frame(self.window)
        self.middle_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

        # 上部：軍全体の状態
        self.create_status_area()

        # 中央：ユニット情報
        self.create_units_display()

        # 下部：操作パネル
        self.create_control_panel()

    def create_status_area(self):
        """軍全体の状態を表示"""
        left = tk.Frame(self.top_frame)
        left.pack(side=tk.LEFT, fill=tk.X, expand=True)

        right = tk.Frame(self.top_frame)
        right.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        tk.Label(left, text=self.player_army.name, font=("Arial", 14, "bold")).pack(anchor="w")
        self.player_status_label = tk.Label(left, text="", font=("Arial", 10))
        self.player_status_label.pack(anchor="w")

        tk.Label(right, text=self.enemy_army.name, font=("Arial", 14, "bold")).pack(anchor="e")
        self.enemy_status_label = tk.Label(right, text="", font=("Arial", 10))
        self.enemy_status_label.pack(anchor="e")

    def create_units_display(self):
        """ユニット詳細情報を表示"""
        # 左側：プレイヤー部隊
        left_frame = tk.LabelFrame(self.middle_frame, text="プレイヤー軍ユニット（選択）", font=("Arial", 10, "bold"))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.player_units_frame = tk.Frame(left_frame)
        self.player_units_frame.pack(fill=tk.BOTH, expand=True)

        self.player_unit_buttons = []
        for idx, unit in enumerate(self.player_army.units):
            btn = tk.Button(
                self.player_units_frame,
                text=self.format_unit_display(unit),
                wraplength=200,
                justify=tk.LEFT,
                bg="lightblue" if idx == self.selected_player_unit_idx else "white",
                command=lambda i=idx: self.select_player_unit(i)
            )
            btn.pack(fill=tk.BOTH, expand=True, pady=2)
            self.player_unit_buttons.append(btn)

        # 右側：敵部隊
        right_frame = tk.LabelFrame(self.middle_frame, text="敵軍ユニット（攻撃対象を選択）", font=("Arial", 10, "bold"))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.enemy_units_frame = tk.Frame(right_frame)
        self.enemy_units_frame.pack(fill=tk.BOTH, expand=True)

        self.enemy_unit_buttons = []
        for idx, unit in enumerate(self.enemy_army.units):
            btn = tk.Button(
                self.enemy_units_frame,
                text=self.format_unit_display(unit),
                wraplength=200,
                justify=tk.LEFT,
                bg="lightgreen" if idx == self.selected_enemy_unit_idx else "lightyellow",
                command=lambda i=idx: self.select_enemy_unit(i)
            )
            btn.pack(fill=tk.BOTH, expand=True, pady=2)
            self.enemy_unit_buttons.append(btn)

        # ログエリア
        log_frame = tk.LabelFrame(self.middle_frame, text="戦闘ログ", font=("Arial", 10, "bold"))
        log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, before=left_frame)

        self.log_text = tk.Text(log_frame, height=5, state="disabled")
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def create_control_panel(self):
        """操作パネル"""
        self.attack_button = tk.Button(
            self.bottom_frame,
            text="攻撃",
            command=self.on_attack,
            font=("Arial", 12),
            bg="green",
            fg="white"
        )
        self.attack_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.info_label = tk.Label(self.bottom_frame, text="", font=("Arial", 10))
        self.info_label.pack(side=tk.LEFT, padx=20)

    def run(self):
        self.update_all()
        self.window.mainloop()

    def select_player_unit(self, idx: int):
        """プレイヤー部隊を選択"""
        self.selected_player_unit_idx = idx
        for i, btn in enumerate(self.player_unit_buttons):
            btn.config(bg="lightblue" if i == idx else "white")

    def select_enemy_unit(self, idx: int):
        """敵部隊を選択（攻撃対象）"""
        self.selected_enemy_unit_idx = idx
        for i, btn in enumerate(self.enemy_unit_buttons):
            btn.config(bg="lightgreen" if i == idx else "lightyellow")

    def on_attack(self):
        """プレイヤーの攻撃"""
        player_unit = self.player_army.units[self.selected_player_unit_idx]
        
        # 有効なユニットか確認
        if not player_unit.is_alive():
            messagebox.showwarning("選択エラー", "選択したユニットは既に撃破されています")
            return
        
        enemy_unit = self.enemy_army.units[self.selected_enemy_unit_idx]
        if not enemy_unit.is_alive():
            messagebox.showwarning("選択エラー", "選択した敵ユニットは既に撃破されています")
            return
        
        # 攻撃を実行
        damage = player_unit.calc_attack_damage()
        enemy_unit.take_damage(damage)
        msg = f"{player_unit.commander}({player_unit.unit_type}) が {enemy_unit.commander} に {damage} ダメージ！"
        self.log(msg)
        self.battle.log_messages.append(msg)

        self.update_all()

        if self.battle.is_over():
            self.show_result()
            return

        # 敵が反撃
        self.window.after(500, self.enemy_turn)

    def enemy_turn(self):
        """敵の攻撃"""
        msg = self.battle.enemy_attack()
        if msg:
            self.log(msg)

        self.update_all()

        if self.battle.is_over():
            self.show_result()
            return

    def update_all(self):
        """全表示を更新"""
        # 軍の状態を更新
        player_alive = len(self.player_army.get_alive_units())
        player_info = f"{player_alive}/{len(self.player_army.units)} ユニット生存"
        self.player_status_label.config(text=player_info)

        enemy_alive = len(self.enemy_army.get_alive_units())
        enemy_info = f"{enemy_alive}/{len(self.enemy_army.units)} ユニット生存"
        self.enemy_status_label.config(text=enemy_info)

        # プレイヤーユニットを更新
        for idx, (btn, unit) in enumerate(zip(self.player_unit_buttons, self.player_army.units)):
            color = "lightgray" if not unit.is_alive() else ("lightblue" if idx == self.selected_player_unit_idx else "white")
            btn.config(text=self.format_unit_display(unit), bg=color)

        # 敵ユニットを更新
        for idx, (btn, unit) in enumerate(zip(self.enemy_unit_buttons, self.enemy_army.units)):
            color = "darkred" if not unit.is_alive() else ("lightgreen" if idx == self.selected_enemy_unit_idx else "lightyellow")
            btn.config(text=self.format_unit_display(unit), bg=color)

    def format_unit_display(self, unit) -> str:
        """ユニット情報をフォーマット"""
        status = "撃破" if not unit.is_alive() else "生存"
        return (f"{unit.commander}\n"
                f"種別: {unit.unit_type}\n"
                f"兵: {unit.get_remaining_groups()}組 / HP: {unit.hp}\n"
                f"状態: {status}")

    def log(self, text: str):
        """ログに追加"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def show_result(self):
        """結果画面"""
        winner = self.battle.get_winner()
        if winner == "player":
            messagebox.showinfo("戦闘結果", f"{self.player_army.name} の勝利！")
        else:
            messagebox.showinfo("戦闘結果", f"{self.enemy_army.name} の勝利…")
        self.window.destroy()
