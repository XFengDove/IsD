import pygame
import sys
import math
import random
from Secure import SecuerT
import json


# 初始化 Pygame
pygame.init()
pygame.mixer.init()
# class MusicList():
#     def __init__(self):
#         self.MusicData=pygame.mixer.music.load("GameData/沉闷敲击声.mp3")
#     def Play(self):
#         pygame.mixer.music.play()


# 设置窗口尺寸
UserWin=pygame.display.list_modes()
WIDTH, HEIGHT = UserWin[0]
screen = pygame.display.set_mode(UserWin[0])
pygame.display.set_caption("IsD")

# 定义颜色
BACKGROUND = (30, 30, 50)
PLAYER_COLOR = (0, 200, 255)
TEXT_COLOR = (220, 220, 220)
BALL_COLOR = (255, 100, 100)
RANGE_COLOR = (150, 50, 50, 150)  # 半透明红色
EXPLOSION_COLORS = [(255, 200, 0), (255, 100, 0), (255, 50, 0)]
HP_COLOR = (50, 200, 50)  # 生命值颜色 (绿色)
MP_COLOR = (50, 100, 255)  # 魔力值颜色 (蓝色)
UI_BG_COLOR = (20, 20, 40, 220)  # UI背景颜色 (半透明)
UI_BORDER_COLOR = (100, 100, 150)
ATTRIBUTE_COLORS = {
    "生命值": (220, 50, 50),
    "魔力值": (50, 150, 220),
    "物理攻击": (200, 150, 50),
    "法术攻击": (180, 80, 200),
    "暴击率": (200, 100, 50),
    "暴击伤害": (200, 50, 100),
    "防御": (100, 150, 200),
}

def LoadUserData():
    Ud=SecuerT()
    return Ud.Load_SData("UserData.json")
class CharacterSystem:
    def __init__(self):
        with open("UserData.json","r",encoding="utf-8") as f:
            self.attributes=json.load(f)["User"]

        self.show_attributes = False
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 32)
        self.small_font = pygame.font.SysFont(None, 20)

    def take_damage(self, amount):
        """角色受到伤害"""
        self.attributes["Role"]["生命值"] = max(0, self.attributes["Role"]["生命值"] - amount)
        return self.attributes["Role"]["生命值"] > 0

    def use_mana(self, amount):
        """消耗魔力值"""
        if self.attributes["Role"]["NowMana"] >= amount:
            self.attributes["Role"]["NowMana"] -= amount
            return True
        return False

    def regenerate(self, dt):
        """随时间恢复生命值和魔力值"""
        # 每秒钟恢复1%的生命值和2%的魔力值
        hp_regen = self.attributes["Role"]["最大生命值"] * 0.01 * dt
        mp_regen = self.attributes["Role"]["MaxMana"] * 0.02 * dt

        self.attributes["Role"]["生命值"] = min(
            self.attributes["Role"]["最大生命值"],
            self.attributes["Role"]["生命值"] + hp_regen
        )
        self.attributes["Role"]["NowMana"] = min(
            self.attributes["Role"]["MaxMana"],
            self.attributes["Role"]["NowMana"] + mp_regen
        )

    def draw_attributes(self, surface):
        """绘制角色属性界面"""
        if not self.show_attributes:
            return

        # 创建半透明背景
        bg_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        bg_surface.fill(UI_BG_COLOR)
        surface.blit(bg_surface, (0, 0))

        # 绘制属性窗口
        window_width, window_height = 700, 900
        window_x, window_y = (WIDTH - window_width) // 2, (HEIGHT - window_height) // 2

        # 绘制窗口背景
        pygame.draw.rect(surface, (40, 40, 70), (window_x, window_y, window_width, window_height))
        pygame.draw.rect(surface, UI_BORDER_COLOR, (window_x, window_y, window_width, window_height), 3)

        # 绘制标题
        title = self.title_font.render("角色属性", True, (220, 220, 255))
        surface.blit(title, (window_x + (window_width - title.get_width()) // 2, window_y + 20))

        # 绘制基本属性
        y_offset = window_y + 70
        section_title = self.font.render("基本属性", True, (200, 200, 100))
        surface.blit(section_title, (window_x + 30, y_offset))
        y_offset += 40

        # 基本属性列表
        basic_attrs = [
            ("Name", self.attributes["Basic"]["Name"]),
            ("Birthday", self.attributes["Basic"]["BirthDay"])
        ]

        for attr, value in basic_attrs:
            text = self.font.render(f"{attr}: {value}", True, TEXT_COLOR)
            surface.blit(text, (window_x + 50, y_offset))
            y_offset += 30

        # 绘制角色属性
        y_offset += 20
        section_title = self.font.render("角色属性", True, (200, 200, 100))
        surface.blit(section_title, (window_x + 30, y_offset))
        y_offset += 40

        # 角色属性列表
        role_attrs = [
            ("生命值", f"{self.attributes['Role']['生命值']:.1f}/{self.attributes['Role']['生命值']}"),
            ("魔力值", f"{self.attributes['Role']['NowMana']:.1f}/{self.attributes['Role']['MaxMana']}"),
            ("物理攻击力", self.attributes["Role"]["物理攻击力"]),
            ("法术攻击力", self.attributes["Role"]["法术攻击力"]),
            ("暴击率", f"{self.attributes['Role']['暴击率'] * 100:.1f}%"),
            ("暴击伤害", f"{self.attributes['Role']['暴击伤害'] * 100:.1f}%"),
            ("穿透", self.attributes["Role"]["穿透"]),
            ("物理伤害加成", f"{self.attributes['Role']['物理伤害加成'] * 100:.1f}%"),
            ("防御力", self.attributes["Role"]["防御力"]),
            ("物理抗性", f"{self.attributes['Role']['物理抗性']}%"),
            ("法术抗性", f"{self.attributes['Role']['法术抗性']}%"),
            ("全伤害加成", f"{self.attributes['Role']['全伤害加成'] * 100:.1f}%"),
        ]

        # 分两列显示
        col1_x = window_x + 50
        col2_x = window_x + window_width // 2

        for i, (attr, value) in enumerate(role_attrs):
            col = col1_x if i % 2 == 0 else col2_x
            row_y = y_offset + (i // 2) * 30

            # 获取属性颜色
            color = ATTRIBUTE_COLORS.get(attr.split()[0], TEXT_COLOR)

            attr_text = self.font.render(f"{attr}:", True, color)
            value_text = self.font.render(str(value), True, TEXT_COLOR)

            surface.blit(attr_text, (col, row_y))
            surface.blit(value_text, (col + 150, row_y))

        # 法术伤害加成
        y_offset += (len(role_attrs) // 2 + 1) * 30
        section_title = self.font.render("法术伤害加成", True, (200, 200, 100))
        surface.blit(section_title, (window_x + 30, y_offset))
        y_offset += 40

        spell_attrs = self.attributes["Role"]["法术伤害加成"]
        for i, (element, value) in enumerate(spell_attrs.items()):
            col = col1_x if i % 2 == 0 else col2_x
            row_y = y_offset + (i // 2) * 30

            color = (200, 100, 50) if element == "火焰" else \
                (50, 150, 200) if element == "水" else \
                    (150, 200, 250) if element == "冰" else \
                        (255, 255, 150)

            attr_text = self.font.render(f"{element}系:", True, color)
            value_text = self.font.render(f"{value * 100:.1f}%", True, TEXT_COLOR)

            surface.blit(attr_text, (col, row_y))
            surface.blit(value_text, (col + 100, row_y))

        # 装备信息
        y_offset += (len(spell_attrs) // 2 + 1) * 30
        section_title = self.font.render("装备信息", True, (200, 200, 100))
        surface.blit(section_title, (window_x + 30, y_offset))
        y_offset += 40

        materiel = self.attributes["Materiel"]
        equipment = [
            ("武器", materiel["Weapon"]),
            ("头盔", materiel["Hard"]),
            ("手套", materiel["Hand"]),
            ("胸甲", materiel["Chest"]),
            ("护腿", materiel["Gaiters"]),
            ("靴子", materiel["Shoes"])
        ]

        for i, (slot, item) in enumerate(equipment):
            col = col1_x if i % 2 == 0 else col2_x
            row_y = y_offset + (i // 2) * 30

            slot_text = self.font.render(f"{slot}:", True, (180, 180, 220))
            item_text = self.font.render(item, True, (200, 180, 100))

            surface.blit(slot_text, (col, row_y))
            surface.blit(item_text, (col + 80, row_y))

        # 首饰信息
        y_offset += (len(equipment) // 2 + 1) * 30
        jewelry = materiel["Jewelry"]
        jewelry_list = [
            ("上戒指", jewelry["Ring_Up"]),
            ("中戒指", jewelry["Ring_Mid"]),
            ("下戒指", jewelry["Ring_Low"]),
            ("上勋章", jewelry["Medal_Up"]),
            ("中勋章", jewelry["Medal_Mid"]),
            ("下勋章", jewelry["Medal_Low"])
        ]

        for i, (slot, item) in enumerate(jewelry_list):
            col = col1_x if i % 2 == 0 else col2_x
            row_y = y_offset + (i // 2) * 30

            slot_text = self.font.render(f"{slot}:", True, (180, 180, 220))
            item_text = self.font.render(item, True, (200, 180, 100))

            surface.blit(slot_text, (col, row_y))
            surface.blit(item_text, (col + 80, row_y))

            # 关闭提示A按 B 键关闭属性界面", True, (180, 180, 220))
            # surface.blit(hint, (window_x + window_width - hint.get_width() - 20, window_y + window_height - 40))

    def draw_hp_mp_bars(self, surface, x, y, width, height):
        """绘制血条和魔力条"""
        # 绘制血条背景
        pygame.draw.rect(surface, (80, 30, 30), (x, y, width, height))
        # 绘制血条
        hp_ratio = self.attributes["Role"]["生命值"] / self.attributes["Role"]["最大生命值"]
        hp_width = max(5, int(width * hp_ratio))
        pygame.draw.rect(surface, HP_COLOR, (x, y, hp_width, height))

        # 魔力条背景
        pygame.draw.rect(surface, (30, 30, 80), (x, y + height + 5, width, height))
        # 魔力条
        mp_ratio = self.attributes["Role"]["NowMana"] / self.attributes["Role"]["MaxMana"]
        mp_width = max(5, int(width * mp_ratio))
        pygame.draw.rect(surface, MP_COLOR, (x, y + height + 5, mp_width, height))

        # 文字标签
        hp_text = self.small_font.render(
            f"HP: {self.attributes['Role']['生命值']:.1f}/{self.attributes['Role']['最大生命值']}", True, TEXT_COLOR)
        mp_text = self.small_font.render(
            f"MP: {self.attributes['Role']['NowMana']:.1f}/{self.attributes['Role']['MaxMana']}", True,
            TEXT_COLOR)

        surface.blit(hp_text, (x + width + 10, y))
        surface.blit(mp_text, (x + width + 10, y + height + 5))
# 玩家设置
player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 1
max_speed = 5
acceleration = 0.2
deceleration = 0.15
smooth_factor = 0.45  # 转向平滑系数
attack_range = 720  # 攻击范围
shot_cooldown = 0.2  # 发射冷却时间（秒）

# 移动方向向量
move_x = 0
move_y = 0
current_direction_x = 0
current_direction_y = 0


# 设置
class EnergyBall:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.target_x = target_x
        self.target_y = target_y

        # 计算方向向量
        dx = target_x - start_x
        dy = target_y - start_y
        distance = max(1, math.sqrt(dx * dx + dy * dy))  # 避免除以零

        self.direction_x = dx / distance
        self.direction_y = dy / distance

        self.speed = 12
        self.distance = distance
        self.traveled = 0
        self.size = 8
        self.active = True
        self.trail = []  # 轨迹点
        self.trail_max = 10
        self.exploding = False
        self.explosion_timer = 0
        self.explosion_duration = 0.4  # 爆炸持续时间（秒）
        self.particles = []  # 爆炸粒子

        # 光球颜色
        self.color = (
            random.randint(200, 255),
            random.randint(50, 150),
            random.randint(50, 150)
        )

        # 光球效果
        self.glow_size = self.size * 2.5
        self.glow_color = (
            min(255, self.color[0] + 50),
            min(255, self.color[1] + 30),
            min(255, self.color[2] + 30),
            100  # 透明度
        )

    def update(self, dt):
        if not self.active:
            return False

        if self.exploding:
            # 更新爆炸状态
            self.explosion_timer += dt
            if self.explosion_timer >= self.explosion_duration:
                self.active = False
                return False

            # 更新粒子
            for particle in self.particles[:]:
                particle[0] += particle[2] * dt * 60
                particle[1] += particle[3] * dt * 60
                particle[4] -= dt * 2  # 减小粒子大小
                particle[5] -= dt * 3  # 减小粒子透明度

                if particle[4] <= 0 or particle[5] <= 0:
                    self.particles.remove(particle)

            return True

        # 移动光球
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        self.traveled += self.speed

        # 添加轨迹点
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_max:
            self.trail.pop(0)

        # 检查是否到达目标或超出范围
        if self.traveled >= self.distance or self.traveled >= attack_range:
            self.explode()

        return True

    def explode(self):
        self.exploding = True
        self.explosion_timer = 0

        # 创建爆炸粒子
        num_particles = 30
        for _ in range(num_particles):
            # [x, y, speed_x, speed_y, size, alpha, color]
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 8)
            size = random.uniform(3, 8)
            color_idx = random.randint(0, len(EXPLOSION_COLORS) - 1)

            self.particles.append([
                self.x,
                self.y,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                size,
                1.0,  # alpha
                EXPLOSION_COLORS[color_idx]
            ])

    def draw(self, surface):
        if not self.active:
            return

        if self.exploding:
            # 绘制爆炸粒子
            for particle in self.particles:
                x, y, _, _, size, alpha, color = particle
                alpha_val = int(alpha * 255)
                particle_color = (*color, alpha_val)

                # 绘制粒子发光效果
                glow_surface = pygame.Surface((int(size * 3), int(size * 3)), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*color, int(alpha_val * 0.5)),
                                   (int(size * 1.5), int(size * 1.5)),
                                   int(size * 1.5))
                surface.blit(glow_surface, (int(x - size * 1.5), int(y - size * 1.5)))

                # 绘制粒子核心
                pygame.draw.circle(surface, particle_color, (int(x), int(y)), int(size))
        else:
            # 绘制轨迹
            for i, (trail_x, trail_y) in enumerate(self.trail):
                alpha = int(255 * i / len(self.trail))
                size = max(1, int(self.size * i / len(self.trail)))
                pygame.draw.circle(surface,
                                   (*self.color[:3], alpha),
                                   (int(trail_x), int(trail_y)),
                                   size)

            # 绘制光球发光效果
            glow_surface = pygame.Surface((self.glow_size * 2, self.glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, self.glow_color,
                               (self.glow_size, self.glow_size),
                               self.glow_size)
            surface.blit(glow_surface, (self.x - self.glow_size, self.y - self.glow_size))

            # 绘制光球核心
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


# 光球列表
energy_balls = []
last_shot_time = 0  # 上次发射时间

character_system = CharacterSystem()

# 创建时钟对象控制帧率
clock = pygame.time.Clock()

# 显示说明文字
font = pygame.font.SysFont(None, 28)
instructions = [
    "使用 WASD 或方向键移动",
    "按住 SHIFT 加速",
    "鼠标左键: 持续发射光球",
    "光球命中目标或到达极限距离后爆炸",
    "按 ESC 键退出程序"
]
instructions=[i.encode("GBK") for i in instructions]


def draw_instructions():
    """在窗口底部绘制操作说明"""
    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (20, HEIGHT - 100 + i * 25))


def draw_player():
    """绘制玩家角色"""
    # 绘制主体
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_size, player_size), 0, 10)

    # 添加高光效果
    pygame.draw.rect(screen, (150, 240, 255), (player_x, player_y, player_size, player_size // 3), 0, 10)

    # 添加眼睛
    eye_x_offset = 0
    if abs(current_direction_x) > 0.1 or abs(current_direction_y) > 0.1:
        # 根据移动方向调整眼睛位置
        eye_x_offset = current_direction_x * 5

    pygame.draw.circle(screen, (0, 0, 0),
                       (player_x + player_size // 3 + eye_x_offset, player_y + player_size // 3), 4)
    pygame.draw.circle(screen, (0, 0, 0),
                       (player_x + 2 * player_size // 3 + eye_x_offset, player_y + player_size // 3), 4)

    # 添加嘴巴(根据速度变化表情)
    mouth_height = 3 + abs(player_speed) * 0.8
    pygame.draw.arc(screen, (0, 0, 0),
                    (player_x + player_size // 4, player_y + player_size // 2,
                     player_size // 2, mouth_height),
                    0, math.pi, 2)

    # 绘制方向指示器
    if abs(current_direction_x) > 0.1 or abs(current_direction_y) > 0.1:
        center_x = player_x + player_size // 2
        center_y = player_y + player_size // 2
        end_x = center_x + current_direction_x * player_size * 0.8
        end_y = center_y + current_direction_y * player_size * 0.8

        pygame.draw.line(screen, (255, 255, 0), (center_x, center_y), (end_x, end_y), 3)
        pygame.draw.circle(screen, (255, 200, 0), (end_x, end_y), 5)


def draw_range_indicator(mouse_x, mouse_y):
    """绘制攻击范围指示器"""
    player_center_x = player_x + player_size // 2
    player_center_y = player_y + player_size // 2

    # 计算鼠标到玩家的距离
    dx = mouse_x - player_center_x
    dy = mouse_y - player_center_y
    distance = math.sqrt(dx * dx + dy * dy)

    # 创建半透明表面
    indicator_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # 绘制攻击范围圆
    pygame.draw.circle(indicator_surface, (*RANGE_COLOR[:3], 50),
                       (player_center_x, player_center_y),
                       attack_range, 1)

    # 绘制攻击方向线
    if distance > 0:
        angle = math.atan2(dy, dx)
        target_x = player_center_x + math.cos(angle) * min(distance, attack_range)
        target_y = player_center_y + math.sin(angle) * min(distance, attack_range)

        # 绘制虚线
        dash_length = 10
        gap_length = 5
        line_length = min(distance, attack_range)
        num_dashes = max(1, int(line_length / (dash_length + gap_length)))

        for i in range(num_dashes):
            start_ratio = i * (dash_length + gap_length) / line_length
            end_ratio = (i * (dash_length + gap_length) + dash_length) / line_length

            start_x = player_center_x + math.cos(angle) * line_length * start_ratio
            start_y = player_center_y + math.sin(angle) * line_length * start_ratio
            end_x = player_center_x + math.cos(angle) * line_length * end_ratio
            end_y = player_center_y + math.sin(angle) * line_length * end_ratio

            # 根据距离改变颜色
            if distance > attack_range and end_ratio >= 1.0:
                line_color = (255, 50, 50, 200)
            else:
                line_color = (200, 200, 100, 200)

            pygame.draw.line(indicator_surface, line_color,
                             (start_x, start_y),
                             (end_x, end_y), 2)

        # 绘制目标点
        if distance > attack_range:
            target_x = player_center_x + math.cos(angle) * attack_range
            target_y = player_center_y + math.sin(angle) * attack_range
            pygame.draw.circle(indicator_surface, (255, 50, 50, 200),
                               (int(target_x), int(target_y)), 8)

            # 添加文本
            font_small = pygame.font.SysFont(None, 22)
            text = font_small.render("MAX", True, (255, 100, 100, 200))
            text_pos = (target_x - text.get_width() // 2, target_y - 30)
            indicator_surface.blit(text, text_pos)

    # 绘制到屏幕上
    screen.blit(indicator_surface, (0, 0))

    return target_x, target_y


# 主游戏循环
running = True
while running:
    # MusicData=pygame.mixer.music.load("GameData/沉闷敲击声.m4a")
    # pygame.mixer.music.play(MusicData)H
    dt = clock.tick(60) / 1000.0  # 获取帧时间(秒)
    current_time = pygame.time.get_ticks() / 1000.0  # 当前时间(秒)
    character_system.regenerate(dt)
    # 处理事件
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]  # 获取鼠标左键状态

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_b:
                # 切换属性界面显示
                character_system.show_attributes = not character_system.show_attributes
            elif event.key == pygame.K_h:
                # 模拟受到伤害
                character_system.take_damage(5)
            elif event.key == pygame.K_m:
                # 模拟消耗魔力
                character_system.use_mana(10)
    if character_system.show_attributes:
        # 绘制背景
        screen.fill(BACKGROUND)

        # 绘制网格背景
        for x in range(0, WIDTH, 40):
            pygame.draw.line(screen, (40, 40, 60), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(screen, (40, 40, 60), (0, y), (WIDTH, y), 1)

        # 绘制角色
        draw_player()

        # 绘制属性界面
        character_system.draw_attributes(screen)

        # 更新显示
        pygame.display.flip()
        continue
    # 持续发射光球（长按左键）
    if mouse_pressed and current_time - last_shot_time > shot_cooldown:
        player_center_x = player_x + player_size // 2
        player_center_y = player_y + player_size // 2

        # 计算实际目标位置（考虑攻击范围）
        target_x, target_y = draw_range_indicator(mouse_x, mouse_y)

        # 创建光球
        energy_balls.append(EnergyBall(
            player_center_x,
            player_center_y,
            target_x,
            target_y
        ))

        last_shot_time = current_time

    # 获取按键状态
    keys = pygame.key.get_pressed()
    move_up = keys[pygame.K_UP] or keys[pygame.K_w]
    move_down = keys[pygame.K_DOWN] or keys[pygame.K_s]
    move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    sprint = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

    # 计算移动向量
    target_x = 0
    target_y = 0

    if move_up and not move_down:
        target_y = -1
    elif move_down and not move_up:
        target_y = 1

    if move_left and not move_right:
        target_x = -1
    elif move_right and not move_left:
        target_x = 1

    # 归一化对角线移动
    if target_x != 0 and target_y != 0:
        target_x *= 0.7071  # 1/sqrt(2)
        target_y *= 0.7071

    # 平滑转向 - 使用线性插值
    if target_x != 0 or target_y != 0:
        current_direction_x += (target_x - current_direction_x) * smooth_factor
        current_direction_y += (target_y - current_direction_y) * smooth_factor

        # 归一化当前方向向量
        length = math.sqrt(current_direction_x ** 2 + current_direction_y ** 2)
        if length > 0:
            current_direction_x /= length
            current_direction_y /= length
    else:
        # 如果没有移动输入，逐渐归零
        current_direction_x *= 0.9
        current_direction_y *= 0.9
        if abs(current_direction_x) < 0.01 and abs(current_direction_y) < 0.01:
            current_direction_x = 0
            current_direction_y = 0

    # 惯性系统
    current_max_speed = max_speed * (1.5 if sprint else 1)

    if target_x != 0 or target_y != 0:
        # 加速
        player_speed = min(player_speed + acceleration, current_max_speed)
    else:
        # 减速
        if player_speed > deceleration:
            player_speed -= deceleration
        else:
            player_speed = 0

    # 更新位置
    if player_speed > 0:
        player_x += current_direction_x * player_speed
        player_y += current_direction_y * player_speed

    # 确保角色不会移出窗口
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    # 更新光球
    for ball in energy_balls[:]:
        if not ball.update(dt):
            energy_balls.remove(ball)

    # 绘制背景
    screen.fill(BACKGROUND)

    # 绘制网格背景 - 以角色为中心
    center_x = player_x + player_size // 2
    center_y = player_y + player_size // 2

    # 计算网格偏移
    offset_x = center_x % 40
    offset_y = center_y % 40

    # 绘制水平网格线
    for y in range(-int(offset_y), HEIGHT, 40):
        pygame.draw.line(screen, (40, 40, 60), (0, y), (WIDTH, y), 1)

    # 绘制垂直网格线
    for x in range(-int(offset_x), WIDTH, 40):
        pygame.draw.line(screen, (40, 40, 60), (x, 0), (x, HEIGHT), 1)

    # 绘制中心线 - 以角色为中心
    pygame.draw.line(screen, (70, 70, 100), (center_x, 0), (center_x, HEIGHT), 2)
    pygame.draw.line(screen, (70, 70, 100), (0, center_y), (WIDTH, center_y), 2)

    # 绘制攻击范围指示器
    draw_range_indicator(mouse_x, mouse_y)

    # 绘制光球
    for ball in energy_balls:
        ball.draw(screen)

    # 绘制角色
    draw_player()

    # 绘制血条和魔力条
    character_system.draw_hp_mp_bars(screen, 20, 20, 200, 15)

    # 显示说明
    draw_instructions()

    # 显示状态信息
    info_text = [
        f"位置: ({player_x:.1f}, {player_y:.1f})",
        f"速度: {player_speed:.1f}",
        f"光球数量: {len(energy_balls)}",
        f"攻击范围: {attack_range}像素",
        f"发射冷却: {shot_cooldown:.1f}秒"
    ]
    for i, text in enumerate(info_text):
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (10, 10 + i * 25))

    # 更新显示
    pygame.display.flip()

# 退出
pygame.quit()
sys.exit()