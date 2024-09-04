import pygame
import math
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kỷ Niệm 79 Năm Ngày Quốc Khánh CHXHCN Việt Nam")
    
# Màu sắc
RED = (218, 37, 29)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
DARK_RED = (139, 0, 0)

# Tải hình ảnh cờ Đảng
flag_party_image = pygame.image.load("code_lỏ/co-dang-viet-nam.jpg")
flag_party_image = pygame.transform.scale(flag_party_image, (WIDTH, HEIGHT))

# Vẽ ngôi sao
def draw_star(surface, color, center, size, fill_percentage=100, rotation=0):
    points = []
    for i in range(5):
        angle = math.pi * 2 * i / 5 - math.pi / 2 + rotation
        point = (
            center[0] + size * math.cos(angle),
            center[1] + size * math.sin(angle)
        )
        points.append(point)
        
        inner_angle = angle + math.pi / 5
        inner_point = (
            center[0] + size * 0.38 * math.cos(inner_angle),
            center[1] + size * 0.38 * math.sin(inner_angle)
        )
        points.append(inner_point)
    
    # Tính toán số điểm cần vẽ dựa trên phần trăm lấp đầy
    num_points = max(3, int(len(points) * fill_percentage / 100))
    if num_points > 2:
        pygame.draw.polygon(surface, color, points[:num_points])

# Hàm vẽ nền gradient
def draw_gradient_background(surface, color1, color2):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = (
            int(color1[0] * (1 - ratio) + color2[0] * ratio),
            int(color1[1] * (1 - ratio) + color2[1] * ratio),
            int(color1[2] * (1 - ratio) + color2[2] * ratio)
        )
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))

# Hàm tạo sao nền
def create_starfield(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 3)
        speed = random.uniform(0.1, 0.5)
        stars.append([x, y, size, speed])
    return stars

# Hàm vẽ sao nền
def draw_starfield(surface, stars):
    for star in stars:
        pygame.draw.circle(surface, YELLOW, (star[0], star[1]), star[2])
        star[1] += star[3]  # Di chuyển sao xuống dưới
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = random.randint(-20, 0)

# Hàm vẽ cờ Việt Nam
def draw_vietnam_flag(surface, alpha):
    flag_surface = pygame.Surface((WIDTH, HEIGHT))
    flag_surface.set_alpha(alpha)
    # Vẽ nền đỏ
    flag_surface.fill(RED)
    # Vẽ ngôi sao vàng
    star_center = (WIDTH // 2, HEIGHT // 2)
    star_size = min(WIDTH, HEIGHT) // 5
    draw_star(flag_surface, YELLOW, star_center, star_size, 100, 0)
    surface.blit(flag_surface, (0, 0))

# Vòng lặp chính
running = True
fill_percentage = 0
clock = pygame.time.Clock()
rotation_angle = 0
text_opacity = 0
stars = create_starfield(100)
show_party_flag = False  # Biến điều khiển hiển thị cờ Đảng
fade_effect = 255  # Biến điều khiển hiệu ứng mờ dần
flag_display_start_time = pygame.time.get_ticks()  # Thời điểm bắt đầu hiển thị cờ Việt Nam
flag_display_duration = 5000  # Thời gian hiển thị cờ Việt Nam (5 giây)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not show_party_flag:
        # Vẽ nền gradient
        draw_gradient_background(screen, BLACK, DARK_RED)

        # Vẽ sao nền
        draw_starfield(screen, stars)

        # Vẽ nền đỏ với hiệu ứng lấp đầy
        fill_width = int(WIDTH * fill_percentage / 100)
        pygame.draw.rect(screen, RED, (0, 0, fill_width, HEIGHT))

        # Vẽ ngôi sao vàng với hiệu ứng lấp đầy và xoay
        star_center = (WIDTH // 2, HEIGHT // 2)
        star_size = min(WIDTH, HEIGHT) // 5
        star_fill = max(0, min(100, (fill_percentage - 50) * 2))  # Giới hạn từ 0 đến 100
        rotation_angle += 0.01  # Tăng góc xoay từ từ
        if star_fill > 0:
            draw_star(screen, YELLOW, star_center, star_size, star_fill, rotation_angle)

        # Vẽ văn bản với hiệu ứng xuất hiện dần và glow
        font = pygame.font.Font(None, 48)
        text_surface = font.render("2/9/1945 - 2/9/2024", True, YELLOW)
        text_surface.set_alpha(text_opacity)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))

        screen.blit(text_surface, text_rect)

        if text_opacity < 255:
            text_opacity += 2  # Tăng độ mờ từ từ

        # Tăng phần trăm lấp đầy
        if fill_percentage < 100:
            fill_percentage += 0.5  # Giảm tốc độ lấp đầy
        else:
            if fill_percentage >= 100 and fill_percentage <= 150:
                fill_percentage += 0.5  # Dừng 1 giây khi hoàn thành
            else:
                # Kiểm tra thời gian hiển thị cờ Việt Nam
                current_time = pygame.time.get_ticks()
                if current_time - flag_display_start_time >= flag_display_duration:
                    show_party_flag = True  # Hiển thị cờ Đảng sau khi hoàn tất hiệu ứng
                    fill_percentage = 0  # Reset để lặp lại hiệu ứng
                    text_opacity = 0  # Reset text opacity
                    fade_effect = 255  # Bắt đầu hiệu ứng mờ dần
    else:
        # Hiển thị cờ Việt Nam với độ mờ dần
        draw_vietnam_flag(screen, fade_effect)

        # Tạo bề mặt đen
        black_surface = pygame.Surface((WIDTH, HEIGHT))
        black_surface.fill(BLACK)
        screen.blit(black_surface, (0, 0))

        # Hiển thị cờ Đảng với độ mờ dần từ đen ra
        flag_party_image.set_alpha(255 - fade_effect)
        screen.blit(flag_party_image, (0, 0))

        # Cập nhật hiệu ứng mờ dần
        if fade_effect > 0:
            fade_effect -= 2  # Giảm độ mờ dần theo thời gian

    # Cập nhật màn hình
    pygame.display.flip()

    clock.tick(60)  # Giới hạn 60 khung hình/giây

# Kết thúc Pygame
pygame.quit()