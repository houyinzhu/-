import pygame
import math
import sys
import random
import os

# 初始化Pygame
pygame.init()

# 游戏窗口设置
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("飞跃减速带模拟")
clock = pygame.time.Clock()

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GREEN = (60, 180, 80)
BLUE = (50, 120, 220)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 220, 60)
ORANGE = (255, 140, 40)
PURPLE = (160, 100, 200)
SKY_BLUE = (135, 206, 235)
ROAD_GRAY = (80, 80, 80)
BROWN = (150, 100, 50)

# 字体初始化函数
def init_font(size=30):
    """尝试多种方法初始化字体，支持中文显示"""
    font_list = []
    
    # 方法1: 尝试加载系统字体
    try:
        # Windows系统常见中文字体
        windows_fonts = ["msyh.ttc", "simhei.ttf", "simsun.ttc", "simfang.ttf", "simkai.ttf"]
        for font_name in windows_fonts:
            try:
                font_path = f"C:/Windows/Fonts/{font_name}"
                if os.path.exists(font_path):
                    return pygame.font.Font(font_path, size)
            except:
                continue
    except:
        pass
    
    # 方法2: 尝试使用默认字体
    try:
        return pygame.font.Font(None, size)
    except:
        pass
    
    # 方法3: 使用系统字体
    try:
        # 尝试常见字体名称
        font_names = ["arial", "helvetica", "times new roman", "courier"]
        for font_name in font_names:
            try:
                font = pygame.font.SysFont(font_name, size)
                if font:
                    return font
            except:
                continue
    except:
        pass
    
    # 方法4: 最后尝试使用默认系统字体
    try:
        return pygame.font.SysFont(None, size)
    except:
        # 如果所有方法都失败，创建一个空字体
        class DummyFont:
            def render(self, text, antialias, color):
                surface = pygame.Surface((len(text) * 10, size), pygame.SRCALPHA)
                pygame.draw.rect(surface, color, (0, 0, len(text) * 10, size))
                return surface
        return DummyFont()

# 初始化字体
font_small = init_font(20)
font_normal = init_font(30)
font_large = init_font(48)
font_title = init_font(60)

# 按钮类
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font if font else font_normal
        self.is_hovered = False
        self.clicked = False
        
    def draw(self, surface):
        # 绘制按钮背景
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        # 绘制按钮文字
        try:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
        except:
            # 如果字体渲染失败，使用简单文本
            text_width = len(self.text) * 10
            text_height = 20
            text_surf = pygame.Surface((text_width, text_height), pygame.SRCALPHA)
            pygame.draw.rect(text_surf, self.text_color, (0, 0, text_width, text_height))
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
        
        # 如果按钮被点击，添加点击效果
        if self.clicked:
            overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 100))
            surface.blit(overlay, self.rect.topleft)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def check_click(self, pos, mouse_down):
        if self.rect.collidepoint(pos) and mouse_down:
            self.clicked = True
            return True
        else:
            self.clicked = False
            return False

# 游戏状态类
class Game:
    def __init__(self):
        # 游戏状态
        self.state = "MENU"  # MENU, PLAYING, SETTINGS, SPEED_SELECT
        self.prev_state = "MENU"
        
        # 游戏设置
        self.car_type = "普通汽车"  # 普通汽车, 跑车
        self.selected_speed = None  # 预设速度
        self.custom_speed = ""  # 自定义速度
        self.difficulty = "中等"  # 简单, 中等, 困难
        
        # 预设速度选项
        self.speed_options = [
            {"label": "安全速度 (30 km/h)", "value": 30},
            {"label": "普通速度 (60 km/h)", "value": 60},
            {"label": "危险速度 (100 km/h)", "value": 100},
            {"label": "极限速度 (150 km/h)", "value": 150},
            {"label": "起飞速度 (320 km/h)", "value": 320},
            {"label": "自定义速度", "value": "custom"}
        ]
        
        # 难度选项
        self.difficulty_options = ["简单", "中等", "困难"]
        
        # 游戏参数
        self.speed_kmh = 0
        self.speed_mph = 0
        self.car_x = 100
        self.car_y = HEIGHT // 2 + 50
        self.car_width = 120
        self.car_height = 60
        self.car_color = BLUE
        self.car_tilt = 0
        self.car_vertical_move = 0
        self.car_velocity = 0
        self.car_crash_particles = []
        self.car_wobble = 0
        
        # 减速带参数
        self.bump_x = WIDTH // 2
        self.bump_width = 20
        self.bump_height = 200
        self.bump_color = RED
        
        # 物理参数
        self.max_speed_normal = 200
        self.max_speed_sports = 320
        self.takeoff_speed = 322
        self.critical_speed = 100
        self.safe_speed = 30
        
        # 根据难度调整参数
        self.update_difficulty_params()
        
        # 结果
        self.result_text = ""
        self.result_details = []
        self.crash_reason = ""
        
        # 输入框
        self.input_active = False
        self.input_rect = pygame.Rect(WIDTH - 250, 20, 200, 40)
        
        # 背景元素
        self.clouds = []
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(20, 150),
                'speed': random.uniform(0.2, 0.8),
                'size': random.randint(30, 70)
            })
            
        self.trees = []
        for _ in range(8):
            self.trees.append({
                'x': random.randint(0, WIDTH),
                'height': random.randint(80, 150),
                'color': (random.randint(30, 100), random.randint(80, 150), random.randint(30, 80))
            })
        
        # 道路标记
        self.road_markings = []
        
        # 按钮
        self.init_buttons()
    
    def update_difficulty_params(self):
        """根据难度调整游戏参数"""
        if self.difficulty == "简单":
            self.critical_speed = 120
            self.safe_speed = 40
        elif self.difficulty == "中等":
            self.critical_speed = 100
            self.safe_speed = 30
        elif self.difficulty == "困难":
            self.critical_speed = 80
            self.safe_speed = 20
    
    def init_buttons(self):
        """初始化所有按钮"""
        # 主菜单按钮
        self.menu_buttons = {
            "start": Button(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50, "开始游戏", BLUE, (30, 90, 170)),
            "settings": Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50, "游戏设置", GREEN, (40, 120, 60)),
            "speed_select": Button(WIDTH//2 - 100, HEIGHT//2 + 90, 200, 50, "速度选择", PURPLE, (130, 80, 180)),
            "exit": Button(WIDTH//2 - 100, HEIGHT//2 + 160, 200, 50, "退出游戏", RED, (180, 50, 50))
        }
        
        # 游戏设置按钮
        self.settings_buttons = {
            "car_normal": Button(200, 200, 180, 50, "普通汽车", BLUE, (30, 90, 170)),
            "car_sports": Button(400, 200, 180, 50, "跑车", RED, (180, 50, 50)),
            "difficulty_easy": Button(200, 280, 180, 50, "简单难度", GREEN, (40, 120, 60)),
            "difficulty_medium": Button(400, 280, 180, 50, "中等难度", ORANGE, (200, 120, 40)),
            "difficulty_hard": Button(600, 280, 180, 50, "困难难度", RED, (180, 50, 50)),
            "back": Button(WIDTH//2 - 100, HEIGHT - 100, 200, 50, "返回主菜单", GRAY, DARK_GRAY)
        }
        
        # 速度选择按钮
        self.speed_buttons = {}
        for i, option in enumerate(self.speed_options):
            y_pos = 150 + i * 70
            self.speed_buttons[f"speed_{i}"] = Button(WIDTH//2 - 200, y_pos, 400, 50, 
                                                     option["label"], BLUE, (30, 90, 170))
        
        # 游戏中的按钮
        self.game_buttons = {
            "restart": Button(WIDTH - 220, HEIGHT - 100, 200, 50, "重新开始", BLUE, (30, 90, 170)),
            "back_menu": Button(WIDTH - 220, HEIGHT - 40, 200, 50, "返回主菜单", GRAY, DARK_GRAY),
            "start_sim": Button(WIDTH - 220, 80, 200, 50, "开始模拟", GREEN, (40, 120, 60))
        }
        
        # 自定义速度输入框
        self.custom_speed_button = Button(WIDTH//2 - 100, HEIGHT - 150, 200, 50, "输入自定义速度", PURPLE, (130, 80, 180))
        self.back_speed_select = Button(WIDTH//2 - 100, HEIGHT - 80, 200, 50, "返回", GRAY, DARK_GRAY)
    
    def reset_game(self):
        """重置游戏状态"""
        self.state = "PLAYING"
        self.speed_kmh = 0
        self.speed_mph = 0
        self.car_x = 100
        self.car_y = HEIGHT // 2 + 50
        self.car_tilt = 0
        self.car_vertical_move = 0
        self.car_velocity = 0
        self.car_crash_particles = []
        self.car_wobble = 0
        self.result_text = ""
        self.result_details = []
        self.crash_reason = ""
        
        # 如果选择了预设速度，使用预设速度
        if self.selected_speed is not None and self.selected_speed != "custom":
            self.speed_kmh = self.selected_speed
            self.speed_mph = self.selected_speed * 0.621371
            self.state = "RUNNING"
            self.car_velocity = self.speed_kmh / 10
            self.calculate_result()
        elif self.custom_speed:
            try:
                self.speed_kmh = float(self.custom_speed)
                self.speed_mph = self.speed_kmh * 0.621371
                self.state = "RUNNING"
                self.car_velocity = self.speed_kmh / 10
                self.calculate_result()
            except ValueError:
                pass
        
        self.create_road_markings()
    
    def create_road_markings(self):
        """创建道路标记"""
        self.road_markings = []
        
        # 减速带的位置和宽度
        bump_start = self.bump_x - self.bump_width // 2
        bump_end = self.bump_x + self.bump_width // 2
        
        # 创建道路中线虚线，避开减速带区域
        dash_length = 30
        gap_length = 20
        current_x = 50
        
        while current_x < WIDTH:
            # 检查这个虚线是否与减速带重叠
            if not (current_x + dash_length > bump_start and current_x < bump_end):
                # 不重叠，添加虚线
                self.road_markings.append({
                    'type': 'center_line',
                    'x': current_x,
                    'y': HEIGHT // 2 + 145,
                    'width': dash_length,
                    'height': 10
                })
            
            # 移动到下一个位置
            current_x += dash_length + gap_length
            
            # 如果下一个位置在减速带内，跳过整个减速带区域
            if bump_start <= current_x <= bump_end:
                current_x = bump_end + gap_length
    
    def calculate_result(self):
        """根据PDF内容计算结果"""
        max_speed = self.max_speed_normal if self.car_type == "普通汽车" else self.max_speed_sports
        
        # 计算物理结果
        self.result_details = []
        
        # 检查是否超过车辆最高速度
        if self.speed_kmh > max_speed:
            self.result_text = "车辆超过设计极限！"
            self.crash_reason = f"车辆设计最高速度为{max_speed} km/h ({max_speed*0.621371:.0f} mph)"
            self.state = "CRASHED"
            return
            
        # 检查是否超过起飞速度
        if self.speed_kmh >= self.takeoff_speed:
            self.result_text = "车辆起飞并坠毁！"
            self.crash_reason = f"速度达到{self.speed_kmh:.0f} km/h ({self.speed_mph:.0f} mph)，超过起飞速度{self.takeoff_speed} km/h"
            self.state = "CRASHED"
            self.result_details.append("在高速下，空气升力将车辆抬起")
            self.result_details.append("车辆在空中翻滚后坠毁")
            return
            
        # 检查是否超过危险速度
        if self.speed_kmh >= self.critical_speed:
            self.result_text = "车辆严重损坏！"
            self.crash_reason = f"以{self.speed_kmh:.0f} km/h ({self.speed_mph:.0f} mph)的速度撞击减速带"
            self.state = "CRASHED"
            self.result_details.append("轮胎和悬挂系统无法承受冲击")
            self.result_details.append("车辆失控并撞毁")
            return
            
        # 检查是否在安全速度范围内
        if self.speed_kmh <= self.safe_speed:
            self.result_text = "安全通过！"
            self.crash_reason = ""
            self.state = "SUCCESS"
            self.result_details.append("以安全速度通过减速带")
            self.result_details.append("车辆仅有轻微颠簸")
            return
            
        # 中等速度 - 可能损坏但不会完全损毁
        self.result_text = "车辆受损但可修复"
        self.crash_reason = f"以{self.speed_kmh:.0f} km/h ({self.speed_mph:.0f} mph)的速度撞击减速带"
        self.state = "CRASHED"
        self.result_details.append("悬挂系统受损")
        self.result_details.append("可能需要维修")
    
    def update(self):
        # 更新云的位置
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            if cloud['x'] > WIDTH + 100:
                cloud['x'] = -100
        
        # 如果游戏正在运行，更新汽车状态
        if self.state == "RUNNING":
            self.car_x += self.car_velocity
            
            # 汽车接近减速带时的效果
            distance_to_bump = abs(self.car_x - self.bump_x)
            if distance_to_bump < 150:
                # 模拟颠簸
                self.car_vertical_move = math.sin(pygame.time.get_ticks() * 0.01) * 5
                self.car_tilt = math.sin(pygame.time.get_ticks() * 0.02) * 5
                
            # 汽车通过减速带
            if self.car_x > self.bump_x - self.bump_width//2 and self.car_x < self.bump_x + self.bump_width//2:
                # 根据速度决定颠簸程度
                bump_intensity = min(self.speed_kmh / 50, 3.0)
                self.car_vertical_move = 10 * bump_intensity
                self.car_tilt = random.uniform(-10, 10) * bump_intensity
                
                # 如果速度太高，车辆损坏
                if self.speed_kmh >= self.critical_speed:
                    self.create_crash_particles()
            
            # 汽车离开减速带后的效果
            if self.car_x > self.bump_x + self.bump_width//2 + 50:
                if self.speed_kmh >= self.critical_speed:
                    self.car_vertical_move = 0
                    self.car_tilt = 0
                else:
                    # 轻微摇晃
                    self.car_wobble = math.sin(pygame.time.get_ticks() * 0.005) * 2
                    self.car_vertical_move = self.car_wobble
                    self.car_tilt = self.car_wobble * 0.5
            
            # 汽车离开屏幕
            if self.car_x > WIDTH + 200:
                if self.speed_kmh >= self.critical_speed:
                    self.state = "CRASHED"
                else:
                    self.state = "SUCCESS"
        
        # 更新损毁粒子
        for particle in self.car_crash_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.1  # 重力
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.car_crash_particles.remove(particle)
    
    def create_crash_particles(self):
        """创建车辆损毁的粒子效果"""
        for _ in range(20):
            self.car_crash_particles.append({
                'x': self.car_x + random.randint(-30, 30),
                'y': self.car_y + random.randint(-20, 20),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-5, -1),
                'color': random.choice([RED, ORANGE, YELLOW, DARK_GRAY]),
                'size': random.randint(3, 8),
                'life': random.randint(30, 60)
            })
    
    def draw_menu(self):
        """绘制主菜单"""
        # 绘制渐变背景
        for y in range(HEIGHT):
            # 从深蓝色渐变到浅蓝色
            color_value = 30 + int(120 * (y / HEIGHT))
            pygame.draw.line(screen, (10, color_value, 80), (0, y), (WIDTH, y))
        
        # 绘制标题
        try:
            title = font_title.render("飞跃减速带模拟", True, YELLOW)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        except:
            # 如果字体渲染失败，绘制一个简单的矩形替代
            pygame.draw.rect(screen, YELLOW, (WIDTH//2 - 200, 100, 400, 60))
        
        # 绘制副标题
        try:
            subtitle = font_small.render("Q. 最快能以多快的速度驾车冲过减速带并幸存下来？", True, LIGHT_GRAY)
            screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 200))
        except:
            pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH//2 - 300, 200, 600, 20))
        
        # 绘制当前设置
        try:
            settings_text = f"当前设置: {self.car_type} | {self.difficulty}难度"
            settings_surface = font_small.render(settings_text, True, LIGHT_GRAY)
            screen.blit(settings_surface, (WIDTH//2 - settings_surface.get_width()//2, 260))
        except:
            pass
        
        # 绘制按钮
        for button in self.menu_buttons.values():
            button.draw(screen)
        
        # 绘制说明
        instructions = [
            "基于《飞越减速带》文章 - 麦林·巴伯",
            "探索不同速度下车辆通过减速带的结果",
            "在游戏中了解物理学原理"
        ]
        
        for i, instruction in enumerate(instructions):
            try:
                text = font_small.render(instruction, True, LIGHT_GRAY)
                screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 100 + i * 25))
            except:
                pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH//2 - 150, HEIGHT - 100 + i * 25, 300, 20))
    
    def draw_settings(self):
        """绘制设置界面"""
        # 绘制渐变背景
        for y in range(HEIGHT):
            color_value = 30 + int(120 * (y / HEIGHT))
            pygame.draw.line(screen, (10, color_value, 80), (0, y), (WIDTH, y))
        
        # 绘制标题
        try:
            title = font_large.render("游戏设置", True, YELLOW)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        except:
            pygame.draw.rect(screen, YELLOW, (WIDTH//2 - 100, 50, 200, 50))
        
        # 绘制车辆类型选择
        try:
            type_text = font_normal.render("选择车辆类型:", True, WHITE)
            screen.blit(type_text, (WIDTH//2 - type_text.get_width()//2, 130))
        except:
            pygame.draw.rect(screen, WHITE, (WIDTH//2 - 100, 130, 200, 30))
        
        # 绘制车辆类型按钮
        self.settings_buttons["car_normal"].draw(screen)
        self.settings_buttons["car_sports"].draw(screen)
        
        # 高亮当前选择的车辆类型
        if self.car_type == "普通汽车":
            pygame.draw.rect(screen, YELLOW, self.settings_buttons["car_normal"].rect, 3, border_radius=10)
        else:
            pygame.draw.rect(screen, YELLOW, self.settings_buttons["car_sports"].rect, 3, border_radius=10)
        
        # 绘制车辆描述
        try:
            if self.car_type == "普通汽车":
                desc_text = "普通汽车: 最高速度 200 km/h"
            else:
                desc_text = "跑车: 最高速度 320 km/h"
            desc_surface = font_small.render(desc_text, True, LIGHT_GRAY)
            screen.blit(desc_surface, (WIDTH//2 - desc_surface.get_width()//2, 270))
        except:
            pass
        
        # 绘制难度选择
        try:
            difficulty_text = font_normal.render("选择游戏难度:", True, WHITE)
            screen.blit(difficulty_text, (WIDTH//2 - difficulty_text.get_width()//2, 320))
        except:
            pygame.draw.rect(screen, WHITE, (WIDTH//2 - 100, 320, 200, 30))
        
        # 绘制难度按钮
        self.settings_buttons["difficulty_easy"].draw(screen)
        self.settings_buttons["difficulty_medium"].draw(screen)
        self.settings_buttons["difficulty_hard"].draw(screen)
        
        # 高亮当前选择的难度
        if self.difficulty == "简单":
            pygame.draw.rect(screen, YELLOW, self.settings_buttons["difficulty_easy"].rect, 3, border_radius=10)
        elif self.difficulty == "中等":
            pygame.draw.rect(screen, YELLOW, self.settings_buttons["difficulty_medium"].rect, 3, border_radius=10)
        else:
            pygame.draw.rect(screen, YELLOW, self.settings_buttons["difficulty_hard"].rect, 3, border_radius=10)
        
        # 绘制难度描述
        try:
            if self.difficulty == "简单":
                desc = "简单: 安全速度 40 km/h，危险速度 120 km/h"
            elif self.difficulty == "中等":
                desc = "中等: 安全速度 30 km/h，危险速度 100 km/h"
            else:
                desc = "困难: 安全速度 20 km/h，危险速度 80 km/h"
            difficulty_desc = font_small.render(desc, True, LIGHT_GRAY)
            screen.blit(difficulty_desc, (WIDTH//2 - difficulty_desc.get_width()//2, 420))
        except:
            pass
        
        # 绘制返回按钮
        self.settings_buttons["back"].draw(screen)
        
        # 绘制说明
        try:
            instruction = font_small.render("选择车辆类型和游戏难度后点击返回主菜单", True, LIGHT_GRAY)
            screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT - 50))
        except:
            pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH//2 - 200, HEIGHT - 50, 400, 20))
    
    def draw_speed_select(self):
        """绘制速度选择界面"""
        # 绘制渐变背景
        for y in range(HEIGHT):
            color_value = 30 + int(120 * (y / HEIGHT))
            pygame.draw.line(screen, (10, color_value, 80), (0, y), (WIDTH, y))
        
        # 绘制标题
        try:
            title = font_large.render("速度选择", True, YELLOW)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        except:
            pygame.draw.rect(screen, YELLOW, (WIDTH//2 - 100, 50, 200, 50))
        
        # 绘制说明
        try:
            instruction = font_small.render("选择预设速度或自定义速度开始游戏", True, WHITE)
            screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, 120))
        except:
            pygame.draw.rect(screen, WHITE, (WIDTH//2 - 150, 120, 300, 20))
        
        # 绘制速度选项按钮
        for i, (key, button) in enumerate(self.speed_buttons.items()):
            button.draw(screen)
            
            # 高亮当前选择的速度
            if i < len(self.speed_options) - 1:  # 不是自定义选项
                if self.selected_speed == self.speed_options[i]["value"]:
                    pygame.draw.rect(screen, YELLOW, button.rect, 3, border_radius=10)
            else:  # 自定义选项
                if self.selected_speed == "custom":
                    pygame.draw.rect(screen, YELLOW, button.rect, 3, border_radius=10)
        
        # 如果选择了自定义速度，显示输入框
        if self.selected_speed == "custom":
            # 绘制输入框背景
            input_bg = pygame.Rect(WIDTH//2 - 150, HEIGHT - 200, 300, 40)
            pygame.draw.rect(screen, WHITE, input_bg, border_radius=5)
            pygame.draw.rect(screen, BLUE if self.input_active else GRAY, input_bg, 2, border_radius=5)
            
            # 绘制输入文本
            try:
                input_text = font_normal.render(self.custom_speed, True, BLACK)
                screen.blit(input_text, (input_bg.x + 10, input_bg.y + 10))
            except:
                pygame.draw.rect(screen, BLACK, (input_bg.x + 10, input_bg.y + 10, len(self.custom_speed) * 10, 20))
            
            # 绘制提示
            try:
                hint = font_small.render("输入速度 (km/h) 然后按回车确认", True, LIGHT_GRAY)
                screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 150))
            except:
                pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH//2 - 150, HEIGHT - 150, 300, 20))
            
            # 绘制当前设置
            if self.custom_speed:
                try:
                    speed = float(self.custom_speed)
                    mph = speed * 0.621371
                    current_text = font_small.render(f"自定义速度: {speed:.0f} km/h ({mph:.0f} mph)", True, GREEN)
                    screen.blit(current_text, (WIDTH//2 - current_text.get_width()//2, HEIGHT - 120))
                except ValueError:
                    pass
        
        # 绘制返回按钮
        self.back_speed_select.draw(screen)
        
        # 绘制当前选择的车辆和难度
        try:
            current_text = font_small.render(f"当前: {self.car_type} | {self.difficulty}难度", True, LIGHT_GRAY)
            screen.blit(current_text, (WIDTH//2 - current_text.get_width()//2, HEIGHT - 30))
        except:
            pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH//2 - 150, HEIGHT - 30, 300, 20))
    
    def draw_game(self):
        """绘制游戏界面"""
        # 绘制天空
        screen.fill(SKY_BLUE)
        
        # 绘制云朵
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (int(cloud['x']), cloud['y']), cloud['size'])
            pygame.draw.circle(screen, WHITE, (int(cloud['x']) + cloud['size']//2, cloud['y'] - cloud['size']//4), cloud['size']//2)
            pygame.draw.circle(screen, WHITE, (int(cloud['x']) - cloud['size']//2, cloud['y'] - cloud['size']//4), cloud['size']//2)
        
        # 绘制远处树木
        for tree in self.trees:
            # 树干
            pygame.draw.rect(screen, BROWN, (tree['x'], HEIGHT//2 + 80, 15, tree['height']))
            # 树冠
            pygame.draw.circle(screen, tree['color'], (tree['x'] + 7, HEIGHT//2 + 80), 30)
        
        # 绘制道路
        pygame.draw.rect(screen, ROAD_GRAY, (0, HEIGHT//2 + 50, WIDTH, 200))
        
        # 绘制道路中线虚线（避开减速带）
        for marking in self.road_markings:
            if marking['type'] == 'center_line':
                pygame.draw.rect(screen, YELLOW, 
                                (marking['x'], marking['y'], 
                                 marking['width'], marking['height']))
        
        # 绘制路肩
        pygame.draw.rect(screen, GRAY, (0, HEIGHT//2 + 50, WIDTH, 10))
        pygame.draw.rect(screen, GRAY, (0, HEIGHT//2 + 240, WIDTH, 10))
        
        # 绘制横向减速带（不与黄虚线重合）
        bump_y = HEIGHT//2 + 50
        pygame.draw.rect(screen, self.bump_color, 
                        (self.bump_x - self.bump_width//2, bump_y, 
                         self.bump_width, self.bump_height))
        
        # 绘制减速带条纹
        for i in range(6):
            stripe_y = bump_y + i * self.bump_height//5
            pygame.draw.rect(screen, WHITE, 
                           (self.bump_x - self.bump_width//2, stripe_y, 
                            self.bump_width, self.bump_height//10))
        
        # 绘制减速带警告标志
        try:
            warning_text = font_normal.render("减速带", True, BLACK)
            screen.blit(warning_text, (self.bump_x - warning_text.get_width()//2, 
                                      bump_y + self.bump_height//2 - warning_text.get_height()//2))
        except:
            pygame.draw.rect(screen, BLACK, (self.bump_x - 30, bump_y + self.bump_height//2 - 10, 60, 20))
        
        # 绘制车辆
        if self.state != "CRASHED" or len(self.car_crash_particles) < 30:
            car_rect = pygame.Rect(
                self.car_x - self.car_width//2,
                self.car_y - self.car_height//2 + self.car_vertical_move,
                self.car_width,
                self.car_height
            )
            
            # 创建旋转的汽车表面
            car_surface = pygame.Surface((self.car_width, self.car_height), pygame.SRCALPHA)
            
            # 根据汽车类型选择颜色
            car_color = BLUE if self.car_type == "普通汽车" else RED
            
            # 绘制汽车主体
            pygame.draw.rect(car_surface, car_color, (0, 0, self.car_width, self.car_height), border_radius=10)
            
            # 绘制车窗
            pygame.draw.rect(car_surface, (200, 230, 255), (10, 10, self.car_width-20, 20), border_radius=5)
            
            # 绘制车轮
            wheel_color = DARK_GRAY
            pygame.draw.rect(car_surface, wheel_color, (10, self.car_height-15, 20, 10), border_radius=3)
            pygame.draw.rect(car_surface, wheel_color, (self.car_width-30, self.car_height-15, 20, 10), border_radius=3)
            pygame.draw.rect(car_surface, wheel_color, (10, 5, 20, 10), border_radius=3)
            pygame.draw.rect(car_surface, wheel_color, (self.car_width-30, 5, 20, 10), border_radius=3)
            
            # 旋转汽车表面
            rotated_car = pygame.transform.rotate(car_surface, self.car_tilt)
            rotated_rect = rotated_car.get_rect(center=car_rect.center)
            
            screen.blit(rotated_car, rotated_rect.topleft)
        
        # 绘制损毁粒子
        for particle in self.car_crash_particles:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
        
        # 绘制UI面板
        self.draw_game_ui()
    
    def draw_game_ui(self):
        """绘制游戏UI"""
        # 绘制半透明UI背景
        ui_surface = pygame.Surface((WIDTH, 150), pygame.SRCALPHA)
        ui_surface.fill((0, 0, 0, 180))
        screen.blit(ui_surface, (0, 0))
        
        # 绘制标题
        try:
            title_text = font_normal.render("飞跃减速带模拟 - 游戏进行中", True, YELLOW)
            screen.blit(title_text, (20, 20))
        except:
            pygame.draw.rect(screen, YELLOW, (20, 20, 300, 30))
        
        # 绘制当前设置
        try:
            settings_text = f"车辆: {self.car_type} | 难度: {self.difficulty} | 速度: {self.speed_kmh:.0f} km/h ({self.speed_mph:.0f} mph)"
            settings_surface = font_small.render(settings_text, True, WHITE)
            screen.blit(settings_surface, (20, 70))
        except:
            pygame.draw.rect(screen, WHITE, (20, 70, 400, 20))
        
        # 绘制状态
        if self.state == "PLAYING":
            status_text = "准备开始模拟"
            status_color = YELLOW
        elif self.state == "RUNNING":
            status_text = "模拟进行中..."
            status_color = BLUE
        elif self.state == "CRASHED":
            status_text = "模拟结束: 车辆损坏"
            status_color = RED
        elif self.state == "SUCCESS":
            status_text = "模拟结束: 安全通过"
            status_color = GREEN
        else:
            status_text = "未知状态"
            status_color = WHITE
            
        try:
            status_surface = font_normal.render(status_text, True, status_color)
            screen.blit(status_surface, (20, 100))
        except:
            pygame.draw.rect(screen, status_color, (20, 100, 200, 30))
        
        # 绘制游戏中的按钮
        if self.state == "PLAYING":
            self.game_buttons["start_sim"].draw(screen)
        else:
            self.game_buttons["restart"].draw(screen)
        
        self.game_buttons["back_menu"].draw(screen)
        
        # 绘制结果
        if self.result_text:
            result_color = GREEN if "安全" in self.result_text or "成功" in self.result_text else RED
            try:
                result_surface = font_normal.render(self.result_text, True, result_color)
                screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT - 180))
            except:
                pygame.draw.rect(screen, result_color, (WIDTH // 2 - 150, HEIGHT - 180, 300, 30))
            
            # 绘制详细结果
            if self.crash_reason:
                try:
                    reason_surface = font_small.render(self.crash_reason, True, YELLOW)
                    screen.blit(reason_surface, (WIDTH // 2 - reason_surface.get_width() // 2, HEIGHT - 140))
                except:
                    pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - 150, HEIGHT - 140, 300, 20))
            
            for i, detail in enumerate(self.result_details):
                try:
                    detail_surface = font_small.render(detail, True, LIGHT_GRAY)
                    screen.blit(detail_surface, (WIDTH // 2 - detail_surface.get_width() // 2, HEIGHT - 110 + i * 25))
                except:
                    pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH // 2 - 150, HEIGHT - 110 + i * 25, 300, 20))
        
        # 绘制PDF引用
        quotes = [
            "引自《飞越减速带》- 麦林·巴伯",
            f"安全速度: <{self.safe_speed} km/h",
            f"危险速度: >{self.critical_speed} km/h",
            f"起飞速度: {self.takeoff_speed} km/h (200 mph)"
        ]
        
        for i, quote in enumerate(quotes):
            try:
                quote_surface = font_small.render(quote, True, (150, 150, 150))
                screen.blit(quote_surface, (WIDTH - 300, HEIGHT - 120 + i * 20))
            except:
                pygame.draw.rect(screen, (150, 150, 150), (WIDTH - 300, HEIGHT - 120 + i * 20, 250, 15))
        
        # 绘制减速带位置提示
        try:
            bump_note = font_small.render("减速带横向放置，不与黄虚线重合", True, ORANGE)
            screen.blit(bump_note, (20, HEIGHT - 40))
        except:
            pygame.draw.rect(screen, ORANGE, (20, HEIGHT - 40, 250, 15))
    
    def draw(self):
        """根据当前状态绘制相应界面"""
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "SETTINGS":
            self.draw_settings()
        elif self.state == "SPEED_SELECT":
            self.draw_speed_select()
        else:  # PLAYING, RUNNING, CRASHED, SUCCESS
            self.draw_game()

# 创建游戏实例
game = Game()

# 主游戏循环
running = True
mouse_down = False

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            
            # 根据当前状态处理按钮点击
            if game.state == "MENU":
                # 主菜单按钮
                if game.menu_buttons["start"].check_click(mouse_pos, mouse_down):
                    game.state = "SPEED_SELECT"
                elif game.menu_buttons["settings"].check_click(mouse_pos, mouse_down):
                    game.state = "SETTINGS"
                elif game.menu_buttons["speed_select"].check_click(mouse_pos, mouse_down):
                    game.state = "SPEED_SELECT"
                elif game.menu_buttons["exit"].check_click(mouse_pos, mouse_down):
                    running = False
                    
            elif game.state == "SETTINGS":
                # 设置界面按钮
                if game.settings_buttons["car_normal"].check_click(mouse_pos, mouse_down):
                    game.car_type = "普通汽车"
                    game.car_color = BLUE
                elif game.settings_buttons["car_sports"].check_click(mouse_pos, mouse_down):
                    game.car_type = "跑车"
                    game.car_color = RED
                elif game.settings_buttons["difficulty_easy"].check_click(mouse_pos, mouse_down):
                    game.difficulty = "简单"
                    game.update_difficulty_params()
                elif game.settings_buttons["difficulty_medium"].check_click(mouse_pos, mouse_down):
                    game.difficulty = "中等"
                    game.update_difficulty_params()
                elif game.settings_buttons["difficulty_hard"].check_click(mouse_pos, mouse_down):
                    game.difficulty = "困难"
                    game.update_difficulty_params()
                elif game.settings_buttons["back"].check_click(mouse_pos, mouse_down):
                    game.state = "MENU"
                    
            elif game.state == "SPEED_SELECT":
                # 速度选择界面按钮
                for i, (key, button) in enumerate(game.speed_buttons.items()):
                    if button.check_click(mouse_pos, mouse_down):
                        if i < len(game.speed_options) - 1:  # 预设速度
                            game.selected_speed = game.speed_options[i]["value"]
                            game.custom_speed = ""
                            game.input_active = False
                        else:  # 自定义速度
                            game.selected_speed = "custom"
                            game.input_active = True
                
                # 自定义速度输入框
                if game.custom_speed_button.check_click(mouse_pos, mouse_down):
                    game.selected_speed = "custom"
                    game.input_active = True
                
                # 返回按钮
                if game.back_speed_select.check_click(mouse_pos, mouse_down):
                    # 如果有选择的速度，直接开始游戏
                    if game.selected_speed is not None:
                        game.reset_game()
                        game.state = "PLAYING"
                    else:
                        game.state = "MENU"
                        
            elif game.state in ["PLAYING", "RUNNING", "CRASHED", "SUCCESS"]:
                # 游戏界面按钮
                if game.game_buttons["restart"].check_click(mouse_pos, mouse_down):
                    game.reset_game()
                elif game.game_buttons["back_menu"].check_click(mouse_pos, mouse_down):
                    game.state = "MENU"
                elif game.game_buttons["start_sim"].check_click(mouse_pos, mouse_down):
                    if game.state == "PLAYING":
                        if game.selected_speed is not None or game.custom_speed:
                            game.reset_game()
                        else:
                            # 如果没有选择速度，跳转到速度选择界面
                            game.state = "SPEED_SELECT"
        
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
            
        elif event.type == pygame.KEYDOWN:
            # 处理键盘输入
            if game.state == "SPEED_SELECT" and game.selected_speed == "custom" and game.input_active:
                # 自定义速度输入
                if event.key == pygame.K_BACKSPACE:
                    game.custom_speed = game.custom_speed[:-1]
                elif event.key == pygame.K_RETURN:
                    # 确认输入
                    if game.custom_speed:
                        try:
                            speed = float(game.custom_speed)
                            if speed > 0:
                                game.state = "PLAYING"
                                game.reset_game()
                        except ValueError:
                            pass
                elif event.key == pygame.K_ESCAPE:
                    game.input_active = False
                elif event.unicode.isdigit() or event.unicode == '.':
                    if len(game.custom_speed) < 6:
                        game.custom_speed += event.unicode
            
            # 全局快捷键
            if event.key == pygame.K_ESCAPE:
                if game.state == "MENU":
                    running = False
                else:
                    game.state = "MENU"
            elif event.key == pygame.K_F1:
                game.state = "MENU"
            elif event.key == pygame.K_F2:
                game.state = "SETTINGS"
            elif event.key == pygame.K_F3:
                game.state = "SPEED_SELECT"
            elif event.key == pygame.K_F5:
                if game.state in ["PLAYING", "RUNNING", "CRASHED", "SUCCESS"]:
                    game.reset_game()
    
    # 更新按钮悬停状态
    if game.state == "MENU":
        for button in game.menu_buttons.values():
            button.check_hover(mouse_pos)
    elif game.state == "SETTINGS":
        for button in game.settings_buttons.values():
            button.check_hover(mouse_pos)
    elif game.state == "SPEED_SELECT":
        for button in game.speed_buttons.values():
            button.check_hover(mouse_pos)
        game.custom_speed_button.check_hover(mouse_pos)
        game.back_speed_select.check_hover(mouse_pos)
    elif game.state in ["PLAYING", "RUNNING", "CRASHED", "SUCCESS"]:
        for button in game.game_buttons.values():
            button.check_hover(mouse_pos)
    
    # 更新游戏状态
    if game.state in ["RUNNING", "CRASHED", "SUCCESS"]:
        game.update()
    
    # 绘制游戏
    game.draw()
    
    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(60)

# 退出游戏
pygame.quit()
sys.exit()