import pygame
import math

# --- 1. 定数・設定 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
FPS = 60

# 色の定義
COLOR_BG = (40, 40, 40)      # 暗めの背景
COLOR_GRID = (200, 200, 200) # 白いグリッド線
COLOR_TEXT = (150, 150, 150) # 座標テキストの色
COLOR_HIGHLIGHT = (255, 255, 0) # マウスオーバー時の色

# ヘクス（六角形）の設定
HEX_RADIUS = 20
GRID_COLS = 20
GRID_ROWS = 28

# --- 2. 座標計算関数 ---
def get_hex_points(cx, cy, radius):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        px = cx + radius * math.cos(angle_rad)
        py = cy + radius * math.sin(angle_rad)
        points.append((px, py))
    return points

def grid_to_pixel(q, r, radius):
    w = math.sqrt(3) * radius
    h = 2 * radius
    return (w * (q + 0.5 * (r & 1)) + 50, h * r * 0.75 + 50)

def pixel_to_grid(px, py, radius):
    """マウス位置から最も近いグリッド座標を割り出す（簡易版）"""
    # 実際にはもっと複雑な計算が必要ですが、当たり判定用ならこれで十分
    min_dist = float('inf')
    target_grid = (0, 0)
    for r in range(GRID_ROWS):
        for q in range(GRID_COLS):
            cx, cy = grid_to_pixel(q, r, radius)
            dist = math.hypot(px - cx, py - cy)
            if dist < min_dist:
                min_dist = dist
                target_grid = (q, r)
    return target_grid

# --- 3. メイン処理 ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("三国志14風 マップ座標調査ツール")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 10)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        hover_grid = pixel_to_grid(mouse_pos[0], mouse_pos[1], HEX_RADIUS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # クリックしたら座標をコンソールに表示
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Clicked Coordinates: q={hover_grid[0]}, r={hover_grid[1]}")

        screen.fill(COLOR_BG)

        # 全グリッドを描画
        for r in range(GRID_ROWS):
            for q in range(GRID_COLS):
                cx, cy = grid_to_pixel(q, r, HEX_RADIUS)
                hex_points = get_hex_points(cx, cy, HEX_RADIUS)

                # マウスが乗っているヘクスをハイライト
                color = COLOR_HIGHLIGHT if (q, r) == hover_grid else COLOR_GRID
                width = 2 if (q, r) == hover_grid else 1
                
                pygame.draw.polygon(screen, color, hex_points, width)

                # 座標(q, r)を描画
                txt = font.render(f"{q},{r}", True, COLOR_TEXT)
                screen.blit(txt, txt.get_rect(center=(cx, cy)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()