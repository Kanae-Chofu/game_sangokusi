import pygame
import math

# --- 1. 基本設定 ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 1000
FPS = 60
HEX_RADIUS = 20
GRID_COLS, GRID_ROWS = 20, 24

# 設計図に基づいた色定義
COLORS = {
    "司": (160, 185, 220), "豫": (215, 200, 225), "冀": (255, 245, 140),
    "兗": (235, 175, 140), "徐": (215, 235, 210), "青": (190, 210, 235),
    "荊": (205, 235, 245), "揚": (245, 215, 195), "益": (210, 230, 150),
    "涼": (195, 180, 145), "幷": (185, 140, 180), "幽": (245, 200, 135),
    "交": (240, 205, 215), "・": (52, 50, 49),   "海": (20, 30, 90), 
    "N": (40, 40, 40) # 範囲外の色
}

# --- 2. マップデータ（1行20文字 × 24行） ---
# 手書き設計図の塗りつぶし範囲を1マスずつ定義
LAYOUT = [
    "・・・・・・・・・・・・・・・幽幽幽幽幽", # 0
    "涼涼・・・・・・・・・幽幽幽幽幽海海幽幽", # 1
    "涼涼涼・・・幷幷幷幷幷幽幽幽海海海海海幽", # 2
    "涼涼・・・・・幷幷幷幷冀冀冀冀海海海海海", # 3
    "・涼涼涼涼涼涼幷幷幷幷冀冀冀冀冀青青青青", # 4
    "・・涼涼涼涼涼幷幷幷幷冀冀冀冀冀青青青青", # 5
    "・・涼涼涼涼涼幷司司司司冀冀兗兗青青海海", # 6   
    "・・涼涼司司司司司司司兗兗兗兗兗徐徐海海", # 6
    "・・・涼涼司司司司司豫兗兗兗兗豫徐徐海海", # 7
    "・・・涼涼司司司司司豫豫兗兗豫豫徐徐海海", # 8
    "・・・涼涼益益益荊荊荊豫豫豫豫豫徐徐徐海", # 10
    "・・涼涼益益益益益荊荊荊豫豫豫豫徐徐徐海", # 11
    "・・・涼益益益益益益荊荊荊豫豫豫揚揚揚海", # 12
    "・・・益益益益益益荊荊荊荊荊揚揚揚揚揚海", # 13
    "・・・益益益益益益荊荊荊荊荊荊揚揚揚揚揚", # 14
    "・・・益益益益益益荊荊荊荊荊揚揚揚揚揚揚", # 15
    "・・・益益益益益益荊荊荊荊荊揚揚揚揚揚揚", # 16
    "・・益益益益益益荊荊荊荊荊揚揚揚揚揚揚海", # 17
    "・・益益益益益益荊荊荊荊荊揚揚揚揚揚海海", # 18
    "益益益益益益益益荊荊荊荊荊揚揚揚揚揚海海", # 19
    "益益益益益益益交交交交交荊揚揚揚揚揚海海", # 20
    "益益益益益益交交交交交交交交交交交海海海", # 21
    "・益益益益交交交交交交交交交交交海海海海", # 22
    "・・・・・・・・交交交交海海海海海海海海", # 23
]

# --- 3. 描画計算関数 ---
def get_hex_points(cx, cy, radius):
    """六角形の頂点座標を計算"""
    return [(cx + radius * math.cos(math.pi/180 * (60*i-30)),
             cy + radius * math.sin(math.pi/180 * (60*i-30))) for i in range(6)]

def grid_to_pixel(q, r, radius):
    """グリッド座標をピクセル座標に変換（横ズレ考慮）"""
    w, h = math.sqrt(3) * radius, 2 * radius
    return (w * (q + 0.5 * (r & 1)) + 50, h * r * 0.75 + 50)

# --- 4. メイン処理 ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("三国志14風 完全データマップ")
    
    # OSに合わせた日本語フォントの読み込み
    try:
        font = pygame.font.SysFont("msmincho", 14) # Windows
    except:
        font = pygame.font.SysFont("notosanscjkjp", 14) # Linux/Mac系
        
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 背景色（範囲外の色）で塗りつぶし
        screen.fill(COLORS["N"])

        for r in range(GRID_ROWS):
            row_str = LAYOUT[r]
            # 文字数不足によるエラーを回避するために min() を使用
            for q in range(min(len(row_str), GRID_COLS)):
                char = row_str[q]
                
                cx, cy = grid_to_pixel(q, r, HEX_RADIUS)
                points = get_hex_points(cx, cy, HEX_RADIUS)
                
                # 塗りつぶし描画
                color = COLORS.get(char, COLORS["・"])
                pygame.draw.polygon(screen, color, points)
                
                # 境界線と文字の描画（「・」と「海」以外）
                if char not in ["・", "海"]:
                    pygame.draw.polygon(screen, (80, 80, 80), points, 1)
                    label = font.render(char, True, (40, 40, 40))
                    screen.blit(label, label.get_rect(center=(cx, cy)))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()