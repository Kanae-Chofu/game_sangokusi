import pygame
import math
import random

# --- 基本設定 ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 1000
FPS = 60
HEX_RADIUS = 20
GRID_COLS, GRID_ROWS = 20, 24

# 色設定
COLORS = {
    "司": (160, 185, 220), "豫": (215, 200, 225), "冀": (255, 245, 140),
    "兗": (235, 175, 140), "徐": (215, 235, 210), "青": (190, 210, 235),
    "荊": (205, 235, 245), "揚": (245, 215, 195), "益": (210, 230, 150),
    "涼": (195, 180, 145), "幷": (185, 140, 180), "幽": (245, 200, 135),
    "交": (240, 205, 215), "・": (52, 50, 49),   "海": (20, 30, 90), 
    "N": (40, 40, 40)
}

FORCE_COLORS = {
    "袁紹": (240, 210, 0), "袁譚": (255, 230, 100), "公孫瓚": (245, 245, 245),
    "董卓": (20, 20, 20),  "劉備": (40, 160, 60),  "田楷": (150, 200, 150),
    "孔融": (100, 100, 255), "袁術": (255, 120, 180), "陶謙": (180, 240, 180),
    "劉表": (50, 140, 70),  "劉焉": (160, 220, 80), "馬騰": (145, 120, 80),
    "未所属": (180, 180, 180)
}

HISTORICAL_DATA = {
    "幽": (2040000, 396000), "冀": (5930000, 908000), "幷": (690000, 115000),
    "涼": (420000, 102000),  "司": (3100000, 616000), "青": (3710000, 635000),
    "徐": (2790000, 476000), "兗": (4050000, 727000), "豫": (6180000, 1142000),
    "揚": (4340000, 1021000), "荊": (6260000, 1399000), "益": (7240000, 1325000),
    "交": (1110000, 270000)
}

CAPITALS_DATA = {
    (9,8): "洛陽", (10, 9): "許昌", (12, 6): "鄴", (17, 5): "北海",
    (17, 8): "下邳", (10, 13): "襄陽", (4, 14): "成都", (16,13): "建業",
    (3, 5): "武威", (13, 21): "交趾", (13,2): "薊",
    (12,8): "濮陽", (14,12): "汝南", (10,4): "晋陽", (6,8): "長安"
}

FORCE_LAYOUT = {
    "公孫瓚": [(11,1),(12,1),(11,2),(12,2),(13,2), (13,3),(14,3),(14,4),(15,4)],
    "田楷":   [(17,4),(16,5)], "孔融":   [(18,4),(18,5)], "劉備":   [(16,4)],
    "袁譚":   [(16,6)], "袁紹":   [(12,6),(11,3),(12,3),(12,4),(13,4),(12,5),(13,5),(13,6)],
    "張燕":   [(11,4),(11,5)], "董卓":   [(6,8)], "陶謙":   [(17,8)], "劉表":   [(10,13)],
    "劉焉":   [(4,14)], "馬騰":   [(3,5)], "袁術":   [(14,12)],
}

RAW_LAYOUT = [
    "・・・・・・・・・・・・・・・幽幽幽幽幽", "涼涼・・・・・・・・・幽幽幽幽幽海海幽幽",
    "涼涼涼・・・幷幷幷幷幷幽幽幽海海海海海幽", "涼涼・・・・・幷幷幷幷冀冀冀冀海海海海海",
    "・涼涼涼涼涼涼幷幷幷幷冀冀冀冀冀青青青青", "・・涼涼涼涼涼幷幷幷幷冀冀冀冀冀青青青青",
    "・・涼涼涼涼涼幷司司司司冀冀兗兗青青海海", "・・涼涼司司司司司司司兗兗兗兗兗徐徐海海",
    "・・・涼涼司司司司司豫兗兗兗兗豫徐徐海海", "・・・涼涼司司司司司豫豫兗兗豫豫徐徐海海",
    "・・・涼涼益益益荊荊荊豫豫豫豫豫徐徐徐海", "・・涼涼益益益益益荊荊荊豫豫豫豫徐徐徐海",
    "・・・益益益益益益益荊荊荊豫豫豫揚揚揚海", "・・・益益益益益益荊荊荊荊荊揚揚揚揚揚海",
    "・・・益益益益益益荊荊荊荊荊荊揚揚揚揚揚", "・・・益益益益益益荊荊荊荊荊揚揚揚揚揚揚",
    "・・・益益益益益益荊荊荊荊荊揚揚揚揚揚揚", "・・益益益益益益荊荊荊荊荊揚揚揚揚揚揚海",
    "・・益益益益益益荊荊荊荊荊揚揚揚揚揚海海", "益益益益益益益益荊荊荊荊荊揚揚揚揚揚海海",
    "益益益益益益益交交交交交荊揚揚揚揚揚海海", "益益益益益益交交交交交交交交交交交海海海",
    "・益益益益交交交交交交交交交交交海海海海", "・・・・・・・・交交交交海海海海海海海海"
]

# --- グローバル変数 ---
hex_map = {}
diplomacy = {f: "なし" for f in FORCE_COLORS}
selected_hex = None
show_ranking = False
game_year = 191
game_month = 11
player_gold = 3000
player_rice = 30000
player_soldier = 5000  # プレイヤー兵士数
last_event_msg = "なし"
game_active = True
extinction_msg = ""
extinction_timer = 0
flash_timer = 0
action_done = False

def grid_to_pixel(q, r, radius):
    w = math.sqrt(3) * radius
    return (w * (q + 0.5 * (r & 1)) + 50, 2 * radius * r * 0.75 + 50)

def get_neighbors(q, r):
    dirs = [[(1,0),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)],[(1,0),(1,-1),(0,-1),(-1,0),(0,1),(1,1)]]
    return [(q + dq, r + dr) for dq, dr in dirs[r % 2]]

def get_hex_under_mouse(mouse_pos):
    mx, my = mouse_pos
    for coord, data in hex_map.items():
        if math.hypot(mx - data["center"][0], my - data["center"][1]) < HEX_RADIUS:
            return coord
    return None

def setup_map_data():
    province_counts = {}
    temp_grid = {}
    for r in range(GRID_ROWS):
        row_str = RAW_LAYOUT[r]
        for q in range(GRID_COLS):
            char = row_str[q] if q < len(row_str) else "・"
            temp_grid[(q, r)] = char
            if char in HISTORICAL_DATA:
                province_counts[char] = province_counts.get(char, 0) + 1

    for (q, r), char in temp_grid.items():
        is_land = char not in ["・", "海"]
        cx, cy = grid_to_pixel(q, r, HEX_RADIUS)
        peak_house = 0
        if is_land and char in HISTORICAL_DATA:
            _, t_house = HISTORICAL_DATA[char]
            peak_house = int(t_house / province_counts[char])

        owner = "未所属"
        for force, coords in FORCE_LAYOUT.items():
            if (q, r) in coords: owner = force; break

        hex_map[(q, r)] = {
            "q": q, "r": r, "province": char, "center": (cx, cy),
            "is_land": is_land, "owner": owner,
            "peak_house": peak_house,
            "dev_level": 0.05,
            "castle": CAPITALS_DATA.get((q, r), None)
        }

def main():
    global selected_hex, show_ranking, game_year, game_month, player_gold, player_rice, player_soldier
    global last_event_msg, game_active, extinction_msg, extinction_timer, flash_timer, action_done
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("三國志：袁譚立志伝 - 電撃戦・兵士概念版")
    clock = pygame.time.Clock()
    
    # フォント設定（互換性のため標準フォント優先）
    def get_font(size, bold=False):
        return pygame.font.SysFont(["msmincho", "msgothic", "hiraginosans", "sans"], size, bold=bold)

    font = get_font(14)
    ui_font = get_font(18)
    title_font = get_font(22, True)
    rank_font = get_font(20)
    info_font = get_font(24, True)
    big_font = get_font(60, True)

    setup_map_data()
    player_force = "袁譚"
    diplomacy[player_force] = "自分"

    while True:
        mouse_pos = pygame.mouse.get_pos()
        btn_rank_rect = pygame.Rect(380, SCREEN_HEIGHT - 260, 100, 180)
        btn_next_rect = pygame.Rect(500, SCREEN_HEIGHT - 260, 150, 180)
        
        alive_forces_before = set(d["owner"] for d in hex_map.values() if d["owner"] != "未所属")

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            
            if event.type == pygame.KEYDOWN and game_active:
                # K: 開発
                if event.key == pygame.K_k:
                    if action_done: last_event_msg = "今月は行動済みです"
                    elif selected_hex and hex_map[selected_hex]["owner"] == player_force:
                        d = hex_map[selected_hex]
                        if d["dev_level"] < 1.0:
                            if player_gold >= 400:
                                player_gold -= 400
                                d["dev_level"] = min(1.0, d["dev_level"] + 0.08)
                                last_event_msg = f"開発実施：{int(d['dev_level']*100)}%"
                                action_done = True
                            else: last_event_msg = "金が足りません"
                
                # B: 徴兵
                if event.key == pygame.K_b:
                    if action_done: last_event_msg = "今月は行動済みです"
                    elif player_gold >= 500 and player_rice >= 2000:
                        player_gold -= 500
                        player_rice -= 2000
                        player_soldier += 1200
                        last_event_msg = "徴兵：兵士+1200 (金-500 糧-2000)"
                        action_done = True
                    else: last_event_msg = "金または糧が足りません"

                # G: 外交
                if event.key == pygame.K_g:
                    if action_done: last_event_msg = "今月は行動済みです"
                    elif selected_hex:
                        target = hex_map[selected_hex]["owner"]
                        if target != player_force and target != "未所属":
                            if player_gold >= 1000:
                                player_gold -= 1000
                                action_done = True
                                r = random.random()
                                if r < 0.4: diplomacy[target] = "同盟"; last_event_msg = f"{target}と同盟締結！"
                                elif r < 0.7: diplomacy[target] = "臣従"; last_event_msg = f"{target}が臣従を要求"
                                else: diplomacy[target] = "敵対"; last_event_msg = f"{target}と外交決裂"

            if event.type == pygame.MOUSEBUTTONDOWN and game_active:
                if not show_ranking:
                    if btn_rank_rect.collidepoint(mouse_pos): show_ranking = True
                    elif btn_next_rect.collidepoint(mouse_pos):
                        # --- 次月進行ロジック ---
                        game_month += 1
                        if game_month > 12: game_month = 1; game_year += 1
                        action_done = False
                        
                        my_lands = [d for d in hex_map.values() if d["owner"] == player_force]
                        if not my_lands: game_active = False; continue
                        
                        total_houses = sum(int(d["peak_house"] * d["dev_level"]) for d in my_lands)
                        # 収入計算
                        player_gold += (total_houses // 120)
                        if game_month in [6, 10]: # 収穫期
                            player_rice += total_houses // 2
                        
                        # 維持費（兵士数に応じて糧を消費）
                        player_rice -= (player_soldier // 10)
                        if player_rice < 0:
                            player_rice = 0
                            player_soldier = max(0, player_soldier - 500)
                            last_event_msg = "兵糧不足で脱走兵が発生！"

                        # AIの行動
                        for f_name in FORCE_COLORS.keys():
                            if f_name in [player_force, "未所属"]: continue
                            f_hexes = [c for c, d in hex_map.items() if d["owner"] == f_name]
                            if not f_hexes: continue
                            
                            atk_p = 0.25
                            if diplomacy.get(f_name) in ["同盟", "臣従"]: atk_p = 0
                            if random.random() < atk_p:
                                pot = [n for l_c in f_hexes for n in get_neighbors(l_c[0], l_c[1]) if n in hex_map and hex_map[n]["is_land"] and hex_map[n]["owner"] != f_name]
                                if pot:
                                    target_coord = random.choice(pot)
                                    target_hex = hex_map[target_coord]
                                    if target_hex["castle"] and target_hex["owner"] != "未所属":
                                        old_owner = target_hex["owner"]
                                        for c in hex_map:
                                            if hex_map[c]["owner"] == old_owner: hex_map[c]["owner"] = f_name
                                        if old_owner == player_force: last_event_msg = f"警報！{f_name}に本拠地を奪われました！"
                                    else:
                                        target_hex["owner"] = f_name
                        
                        alive_now = set(d["owner"] for d in hex_map.values() if d["owner"] != "未所属")
                        dead = alive_forces_before - alive_now
                        if dead: extinction_msg = f"【{'、'.join(dead)}軍】滅亡"; extinction_timer = 90
                    else:
                        clicked = get_hex_under_mouse(mouse_pos)
                        if clicked:
                            selected_hex = clicked
                            # 右クリック：出陣・占領
                            if event.button == 3:
                                if action_done: last_event_msg = "今月は行動済みです"
                                else:
                                    d = hex_map[clicked]
                                    if d["is_land"] and d["owner"] != player_force:
                                        if any(hex_map.get(n, {}).get("owner") == player_force for n in get_neighbors(clicked[0], clicked[1])):
                                            # 出陣コスト：兵士1000以上必要
                                            if player_soldier >= 1000:
                                                old_owner = d["owner"]
                                                player_soldier -= 800 # 戦闘・遠征消耗
                                                if d["castle"] and old_owner != "未所属":
                                                    count = 0
                                                    for c in hex_map:
                                                        if hex_map[c]["owner"] == old_owner:
                                                            hex_map[c]["owner"] = player_force
                                                            count += 1
                                                    last_event_msg = f"【{old_owner}軍】滅亡！全{count}マス接収"
                                                    flash_timer = 20
                                                else:
                                                    d["owner"] = player_force
                                                    if old_owner != "未所属": diplomacy[old_owner] = "敵対"
                                                    last_event_msg = "占領成功 (兵士-800)"
                                                action_done = True
                                            else: last_event_msg = "兵士不足(最低1000必要)"
                                        else: last_event_msg = "隣接領土が必要です"
                else:
                    if pygame.Rect(300, 850, 200, 50).collidepoint(mouse_pos): show_ranking = False

        # --- 描画 ---
        screen.fill(COLORS["N"])
        if not show_ranking:
            # マップ描画
            for coord, data in hex_map.items():
                cx, cy = data["center"]
                pts = [(cx + HEX_RADIUS * math.cos(math.radians(60*i-30)), cy + HEX_RADIUS * math.sin(math.radians(60*i-30))) for i in range(6)]
                owner = data["owner"]
                base_c = COLORS.get(data["province"], COLORS["・"])
                draw_c = tuple((base_c[i] + FORCE_COLORS.get(owner, (180,180,180))[i]) // 2 for i in range(3)) if owner != "未所属" else base_c
                pygame.draw.polygon(screen, draw_c, pts)
                if data["is_land"]: pygame.draw.polygon(screen, (80, 80, 80), pts, 1)
                if data["castle"]:
                    pygame.draw.rect(screen, (10, 10, 10), (cx-9, cy-9, 18, 18))
                    screen.blit(font.render(data["castle"], True, (255, 255, 255)), (cx - 15, cy + 12))
                if selected_hex == coord:
                    pygame.draw.polygon(screen, (255, 255, 255), pts, 3)

            # ステータスバー
            pygame.draw.rect(screen, (20,20,20), (0,0,800,60))
            info_txt = f"{game_year}年 {game_month}月  金:{player_gold:,}  糧:{player_rice:,}  兵:{player_soldier:,}"
            screen.blit(info_font.render(info_txt, True, (255,255,255)), (20, 15))
            status_c = (150,150,150) if action_done else (100,255,100)
            screen.blit(ui_font.render(f"【{'済' if action_done else '可'}】 報告: {last_event_msg}", True, status_c), (480, 20))

            # 情報パネル
            pygame.draw.rect(screen, (0,0,0,220), (30, 720, 340, 250), border_radius=15)
            pygame.draw.rect(screen, (100,100,100), (30, 720, 340, 250), 2, border_radius=15)
            if selected_hex:
                d = hex_map[selected_hex]
                if d["is_land"]:
                    screen.blit(title_font.render(f"【{d['castle'] or d['province']+'州'}】", True, (255, 215, 0)), (50, 735))
                    rel = diplomacy.get(d["owner"], "なし")
                    screen.blit(ui_font.render(f"支配勢力: {d['owner']} ({rel})", True, (255,255,255)), (50, 770))
                    screen.blit(ui_font.render(f"復興度: {int(d['dev_level']*100)}%", True, (255,255,255)), (50, 795))
                    pygame.draw.rect(screen, (0,255,0), (150, 800, 150 * d["dev_level"], 8))
                    
                    screen.blit(ui_font.render("B:徴兵(金500 糧2000) 兵+1200", True, (150,255,150)), (50, 830))
                    screen.blit(ui_font.render("K:開発(金400) 復興度UP", True, (150,255,150)), (50, 860))
                    screen.blit(ui_font.render("G:外交(金1000) 関係改善試行", True, (150,255,255)), (50, 890))
                    screen.blit(ui_font.render("右クリック:占領(兵1000/消費800)", True, (255,150,150)), (50, 920))
            else:
                screen.blit(ui_font.render("土地を選択してください", True, (150,150,150)), (80, 820))

            # ボタン
            pygame.draw.rect(screen, (20, 60, 20), btn_next_rect, border_radius=15)
            for i, char in enumerate("次月進行"): screen.blit(ui_font.render(char, True, (255,255,255)), (btn_next_rect.centerx - 10, btn_next_rect.y + 40 + i*25))
            pygame.draw.rect(screen, (40, 40, 40), btn_rank_rect, border_radius=15)
            for i, char in enumerate("勢力順位"): screen.blit(ui_font.render(char, True, (255,255,255)), (btn_rank_rect.centerx - 10, btn_rank_rect.y + 40 + i*25))

            if extinction_timer > 0:
                txt = big_font.render(extinction_msg, True, (255, 50, 50))
                screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))); extinction_timer -= 1
            if flash_timer > 0:
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); s.fill((255,255,255)); s.set_alpha(100); screen.blit(s,(0,0)); flash_timer -= 1
            if not game_active:
                s = pygame.Surface((800,1000), pygame.SRCALPHA); s.fill((0,0,0,200)); screen.blit(s,(0,0))
                screen.blit(info_font.render("GAME OVER", True, (255,0,0)), (350, 450))
        else:
            # ランキング表示
            stats = {}
            for d in hex_map.values():
                if d["owner"] != "未所属":
                    if d["owner"] not in stats: stats[d["owner"]] = {"マス": 0, "戸数": 0}
                    stats[d["owner"]]["マス"] += 1; stats[d["owner"]]["戸数"] += int(d["peak_house"] * d["dev_level"])
            sorted_stats = sorted(stats.items(), key=lambda x: x[1]["戸数"], reverse=True)
            pygame.draw.rect(screen, (20,20,20), (50, 50, 700, 800), border_radius=20)
            for i, (name, s_data) in enumerate(sorted_stats[:20]):
                rel = diplomacy.get(name, "-")
                color = FORCE_COLORS.get(name, (255,255,255))
                screen.blit(rank_font.render(f"{i+1}. {name:6s} [{rel}] {s_data['マス']}マス {s_data['戸数']:,}戸", True, color), (100, 100+i*35))
            pygame.draw.rect(screen, (80, 20, 20), (300, 870, 200, 50), border_radius=10); screen.blit(ui_font.render("戻る", True, (255,255,255)), (380, 885))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__": main()