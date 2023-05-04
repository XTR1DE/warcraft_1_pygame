import pygame
import math

pygame.init()


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img, speed, health, damage, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = health
        self.max_health = health
        self.damage = damage
        self.h = h
        self.w = w
        self.x1 = self.rect.x
        self.y1 = self.rect.y
        # выбор и деятельность
        self.choosed = False
        self.collect_wood = False
        self.autoattack = False     # if self.radius_hitbox.colliderect()....
        self.shield = False
        self.build = True

    def health_bar(self, window):
        fill_width = self.w * self.health // self.max_health
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 4, fill_width, self.h // 8)
        fill_rect_red = pygame.Rect(self.rect.x, self.rect.y - 4, self.w, self.h // 8)
        pygame.draw.rect(window, (255, 0, 0), fill_rect_red)
        pygame.draw.rect(window, (0, 255, 0), fill_rect)

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
        self.health_bar(window)

    def hitbox(self):
        pygame.draw.rect(game.window, (78, 78, 78), (self.rect.x, self.rect.y, self.w, self.h), 1)


class Drawing:
    def __init__(self, window, background, orcs, winsize):
        self.window = window  # Определяем окно, в котором будет рисоваться
        self.background = background  # Определяем фон
        self.winsize = winsize  # Определяем размер окна
        self.orcs = orcs  # Определяем массив орков
        self.chooses = 0

        self.font1 = pygame.font.Font('BLKCHCRY.TTF', 58)  # Шрифт
        self.font = pygame.font.Font('BLKCHCRY.TTF', 38)  # Шрифт
        self.menus_image = pygame.transform.scale(pygame.image.load('./menus.png').convert_alpha(), (1560, 1060))  # Грузим изображение меню и изменяем масштаб до 1560x1060 пикселей
        self.menu_mask = pygame.mask.from_surface(self.menus_image)  # Создаем маску для изображения меню
        self.mini_map = GameSprite('./icons/Black.png', 0, 0, 0, 6, 27, 315, 350)
        self.mini_map.image = self.mini_map.image.convert_alpha()  # Грузим изображение мини-карты и изменяем масштаб до 313x350 пикселей
        self.cancel = GameSprite('./icons/cancel.png', 0, 0, 0, 227, 910, 70, 70)  # Создаем игровой спрайт "Отменить"
        self.shield = GameSprite('./icons/shield_icon.png', 0, 0, 0, 20, 614, 110, 90)
        self.avatars = {
            "Peon": pygame.transform.scale(pygame.image.load('./icons/Peon_icon.png'), (144, 102)),
            "Spearman": pygame.transform.scale(pygame.image.load('./icons/Spearman_icon.png'), (144, 102)),
            "Rider": pygame.transform.scale(pygame.image.load('./icons/Rider_icon.png'), (144, 102)),
            "Black": pygame.transform.scale(pygame.image.load('./icons/Black.png'), (144, 102))
        }
        self.avatars_cords = (22, 401)

    def menu(self):
        mouse_clicked = pygame.mouse.get_pressed()
        self.window.blit(self.menus_image, (0, 0), )  # Отрисовываем изображение меню
        self.window.blit(self.mini_map.image, (self.mini_map.rect.x, self.mini_map.rect.y))  # Отрисовываем изображение мини-карты
        self.chooses = len([orc for orc in self.orcs if orc.choosed])

        if mouse_clicked[2]:  # Проверяем, нажата ли правая кнопка мыши
            try:
                if self.menu_mask.get_at(pygame.mouse.get_pos()) \
                        or self.mini_map.rect.collidepoint(pygame.mouse.get_pos()):  # Получаем цвет пикселя из маски по координатам курсора мыши
                    for orc in self.orcs:  # Проходимся по всем оркам
                        orc.direction = ''  # Устанавливаем у всех орков пустое направление
            except IndexError:  # Если происходит ошибка индексации
                pass  # Пропускаем

        if self.chooses > 0:
            self.window.blit(self.shield.image, (self.shield.rect.x, self.shield.rect.y))
            self.window.blit(self.cancel.image, (self.cancel.rect.x, self.cancel.rect.y))  # Отображаем кнопку "Отменить"
            if mouse_clicked[0]:  # Проверяем, нажата ли левая кнопка мыши
                if self.cancel.rect.collidepoint(pygame.mouse.get_pos()):  # Проверяем, была ли нажата кнопка "Отменить"
                    for orc in self.orcs:  # Проходимся по всем оркам
                        orc.direction = ''  # Устанавливаем у всех орков пустое направление
                        orc.choosed = False  # Снимаем выделение с орка
                if self.shield.rect.collidepoint(pygame.mouse.get_pos()):
                    for orc in self.orcs:
                        if orc.choosed:
                            if not orc.defense:
                                orc.toggle_shield()
                            else:
                                orc.disable_shield()
                            orc.choosed = False
        if self.chooses == 1:  # Если выбран только один орк
            for orc in self.orcs:  # Проходимся по всем оркам
                if orc.choosed:  # Проверяем, выделен ли текущий орк
                    self.window.blit(self.avatars[orc.type], (24, 401))
                    self.window.blit(self.font.render(orc.type, True, (255, 255, 255)), (26, 514))  # Отображаем тип орка
                    self.window.blit(self.font.render("Health: " + str(orc.health), True, (255, 255, 255)), (160, 401))  # Отображаем количество здоровья орка
                    self.window.blit(self.font.render("Damage: " + str(orc.damage), True, (255, 255, 255)), (160, 441))  # Отображаем количество урона, наносимого орком
        if self.chooses > 1:  # Если выбрано больше одного орка
            self.window.blit(self.font.render("Group " + str(self.chooses), True, (255, 255, 255)), (26, 514))  # Отображаем надпись "Группа" и количество выбранных орков
            self.window.blit(self.avatars['Black'], self.avatars_cords)

        if self.chooses == 0:
            self.window.blit(self.avatars['Black'], self.avatars_cords)
        self.window.blit(self.font1.render("Lumber: " + str(game.wood), True, (255, 255, 255)), (game.winsize[0]//4, -10))
        self.window.blit(self.font1.render("Gold: " + str(game.gold), True, (255, 255, 255)), (game.winsize[0]//1.4, -10))


class building(GameSprite):
    def __init__(self, img, speed, health, x, y, w, h, type):
        super().__init__(img, speed, health, x, y, w, h)
        self.type = type
        self.type_images = {
            "TownHall": pygame.transform.scale(pygame.image.load('TownHall.png'), (self.rect.x, self.rect.y)),
            "Barracks": pygame.transform.scale(pygame.image.load('Barracks.png'), (self.rect.x, self.rect.y)),
            "Farm": pygame.transform.scale(pygame.image.load('Farm.png'), (self.rect.x, self.rect.y)),
            "GoldMine": pygame.transform.scale(pygame.image.load('GoldMine.png'), (self.rect.x, self.rect.y)),
            "Mill": pygame.transform.scale(pygame.image.load('Mill.png'), (self.rect.x, self.rect.y))
        }


class Player(GameSprite):
    def __init__(self, img, speed, health, damage, x, y, w, h, type):
        super().__init__(img, speed, health, damage, x, y, w, h)
        self.direction = ''  # направление
        self.moving = False  # for animation
        self.animate_group = pygame.sprite.Group()
        self.a, self.b, self.c = 0, 0, 0  # катеты и гипотенуза, для равномерного перемещение
        self.angle = 0  # угол поворота
        self.dx, self.dy = 0, 0  # равномерное смещение
        self.choosed = False  # выбран ли герой
        self.type = type  # тип героя
        self.collect_wood = self.type == 'Peon'  # если он лесоруб, то может собирать дерево
        self.x2, self.y2 = 0, 0  # позиция, куда кликнута была мышка
        self.cooldawn_wood = 800
        self.defense = False

    def click(self):
        # Выбор героя
        mouse_clicked = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_clicked[0]:
            if self.rect.collidepoint(mouse_pos):
                self.choosed = True
        # Если выбрали героя
        if self.choosed:
            self.hitbox()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.health -= 1
            # выбираем куда идти герою
            if mouse_clicked[2]:
                self.choosed = False
                a1 = pygame.mouse.get_pos()
                print(a1)
                self.x2, self.y2 = a1[0], a1[1]

                # Разность сторон y, катет
                self.b = abs(self.rect.y - a1[1])

                # Разность сторон x, катет
                self.a = abs(self.rect.x - a1[0])

                # Гиппотенуза
                self.c = math.sqrt(self.a ** 2 + self.b ** 2)

                # Предотвращение вылета при делении на ноль
                try:
                    self.angle = math.atan(self.a / self.b) * (180 / math.pi)
                except ZeroDivisionError:
                    pass
                pygame.draw.line(game.window, (255, 0, 0), (self.rect.centerx, self.rect.centery), a1)

                # Равномерное смещене по y
                self.dy = math.cos(math.radians(self.angle)) * self.speed

                # Равномерное смешение по x
                self.dx = math.sin(math.radians(self.angle)) * self.speed

                # Выбор четверти кординатной плоскости
                if self.rect.centerx < self.x2 and self.rect.centery < self.y2:
                    self.direction = '4'
                if self.rect.centerx < self.x2 and self.rect.centery > self.y2:
                    self.direction = '1'
                if self.rect.centerx > self.x2 and self.rect.centery < self.y2:
                    self.direction = '3'
                if self.rect.centerx > self.x2 and self.rect.centery > self.y2:
                    self.direction = '2'
        self.move()

    def move(self):
        if self.direction == '1' and self.rect.centery > self.y2:
            if self.rect.centerx < self.x2:
                self.rect.x += self.dx
                self.rect.y -= self.dy
            else:
                self.direction = ''
                self.choosed = False
        if self.direction == '2':
            if self.rect.centerx > self.x2 and self.rect.centery > self.y2:
                self.rect.x -= self.dx
                self.rect.y -= self.dy
            else:
                self.direction = ''
                self.choosed = False
        if self.direction == '3':
            if self.rect.centerx > self.x2 and self.rect.centery < self.y2:
                self.rect.x -= self.dx
                self.rect.y += self.dy
            else:
                self.direction = ''
                self.choosed = False
        if self.direction == '4':
            if self.rect.centerx < self.x2 and self.rect.centery < self.y2:
                self.rect.x += self.dx
                self.rect.y += self.dy
            else:
                self.direction = ''
                self.choosed = False
        if self.collect_wood:
            for tree in game.trees:
                if tree.rect.colliderect(self.rect.x, self.rect.y, self.w, self.h):
                    self.cooldawn_wood -= 1
                    # if:
                    #    if:
                    if 160 > self.cooldawn_wood > 120:      # animate
                        if 120 > self.cooldawn_wood > 80:       # animate
                            if 80 > self.cooldawn_wood > 0:         # animate
                                pass
                if self.cooldawn_wood <= 0:
                    tree.health -= 3
                    self.cooldawn_wood = 800
                if tree.health <= 0:
                    tree.kill()
                    game.wood += 50

    def protect(self):
        pass

    def toggle_shield(self):
        self.speed -= 1
        self.defense = True
        print('shield activate', self.defense)
        self.protect()

    def disable_shield(self):
        self.speed += 1
        self.defense = False
        print('shield was disable', self.defense)


class Game:
    def __init__(self):
        self.winsize = (1560, 1060)
        self.game = True
        self.window = pygame.display.set_mode(self.winsize)
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.map_cords_x = 0
        self.map_cords_y = 0
        self.background = pygame.transform.scale(pygame.image.load("./map.png"), (2000, 2000))
        self.orcs = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.menu = Drawing(self.window, self.background, self.orcs, self.winsize)  # menu
        self.wood = 0
        self.gold = 0
        self.create()

    def create(self):
        x, y = 500, 500
        for i in range(5):
            self.orcs.add(Player("./rider1.png", 3, 10, 3, x, y, 40, 40, 'Rider'))
            x += 75
            y += 50
        x, y = 660, 490
        for i in range(3):
            x += 50
            self.orcs.add(Player("./lumber_.png", 2, 5, 1, x, y, 35, 35, 'Peon'))
        x, y = 420, 110
        for b in range(5):
            y += 30
            for n in range(5):
                self.trees.add(GameSprite("./tree.png", 0, 3, 0, x, y, 40, 40))
                x += 30
            x = 420

    def run(self):
        while self.game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game = False
            self.window.blit(self.background, (self.map_cords_x, self.map_cords_y))
            self.trees.draw(self.window)
            for orc in self.orcs:
                orc.click()
                orc.draw(self.window)
                if orc.health <= 0:
                    orc.kill()
            self.menu.menu()
            print(333)
            self.clock.tick(self.fps)
            pygame.display.update()


game = Game()
game.run()
