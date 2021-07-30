import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        Hint:
        x1, y1 = enemy.get_pos()
        """
        x1, y1 = enemy.get_pos()    # 敵人座標
        x2, y2 = self.center        # 塔的座標
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # 如果距離小於半徑就代表有觸發
        if distance <= self.radius:
            return True

        return False

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        # create semi-transparent surface，不囉嗦，大小直接整個視窗
        transparent_surface = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        transparency = 50  # define transparency: 0~255, 0 is fully transparent
        # draw the 圓形 on the transparent surface
        pygame.draw.circle(transparent_surface, (255, 255, 255, transparency), self.center, self.radius, 0)
        # 將surface(畫布)貼齊視窗，即畫布左上角頂點放置在視窗(0, 0)
        win.blit(transparent_surface, (0, 0))


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 30  # used in self.is_cool_down()
        self.is_selected = True  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else
            counter return to zero
        end if
        """
        # 未達到max_count代表還在冷卻
        if self.cd_count < self.cd_max_count:
            self.cd_count += 1
            return False
        else:
            self.cd_count = 0
            return True

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        # 若冷卻完成且在攻擊範圍內就攻擊，每次只對一位敵攻擊
        for en in enemy_group.get():
            while self.is_cool_down() and self.range_circle.collide(en):
                en.get_hurt(self.damage)
            break

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        # 視窗左上角為(0 ,0)，因此取長方形的左上右下頂點為x,y最小最大值
        x_min, y_min = self.rect.topleft
        x_max, y_max = self.rect.bottomright
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True
        else:
            return False

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

