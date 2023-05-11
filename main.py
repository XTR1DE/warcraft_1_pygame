import pygame
import math
import random

pygame.init()

state = {
    'pressed_on_mini_map': False
}


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img, speed, health, damage, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.new_rect = self.image.get_rect()
        self.new_rect.x = x
        self.new_rect.y = y
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
        fill_rect = pygame.Rect(self.new_rect.x, self.new_rect.y - 4, fill_width, 5)
        fill_rect_red = pygame.Rect(self.new_rect.x, self.new_rect.y - 4, self.w, 5)
        pygame.draw.rect(window, (255, 0, 0), fill_rect_red)
        pygame.draw.rect(window, (0, 255, 0), fill_rect)

    def draw(self, window):
        self.new_rect.x = self.rect.x - (Drawing.dx - Drawing.mini_map.rect.x) * 12
        self.new_rect.y = self.rect.y - (Drawing.dy - Drawing.mini_map.rect.y) * 12
        self.new_rect.width = self.rect.width
        self.new_rect.height = self.rect.height
        # print("Позиция нового объекта", new_rect.x, new_rect.y)

        window.blit(self.image, (self.new_rect.x, self.new_rect.y))
        self.health_bar(window)

    def hitbox(self):
        pygame.draw.rect(game.window, (78, 78, 78), (self.new_rect.x, self.new_rect.y, self.w, self.h), 1)


class Fog(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)

    def draw(self, window):
        pygame.draw.rect(window, (0, 0, 0), self.rect)


class Drawing:
    dx, dy = 0, 0
    mini_map = GameSprite('./map.png', 0, 0, 0, 6, 26, 0, 0)

    def __init__(self, window, background, orcs, knights, buildings, winsize, map_size, map_cords_x, map_cords_y):
        self.window = window  # Определяем окно, в котором будет рисоваться
        self.background = background  # Определяем фон
        self.winsize = winsize  # Определяем размер окна
        self.map_size = map_size
        self.map_cords_x, self.map_cords_y = map_cords_x, map_cords_y
        self.orcs = orcs  # Определяем массив орков
        self.knights = knights
        self.buildings = buildings
        self.chooses = 0

        self.font2 = pygame.font.Font('BLKCHCRY.TTF', 29)
        self.font1 = pygame.font.Font('BLKCHCRY.TTF', 58)  # Шрифт
        self.font = pygame.font.Font('BLKCHCRY.TTF', 38)  # Шрифт
        self.menus_image = pygame.transform.scale(pygame.image.load('./menus.png').convert_alpha(), (1560, 1060))  # Грузим изображение меню и изменяем масштаб до 1560x1060 пикселей
        self.menu_mask = pygame.mask.from_surface(self.menus_image)  # Создаем маску для изображения меню
        Drawing.mini_map = GameSprite('./map.png', 0, 0, 0, 6, 26, self.map_size[0]//12, self.map_size[1]//12)
        self.cancel = GameSprite("./icons/Cancel_icon.png", 0, 0, 0, 227, 910, 70, 70)  # Создаем игровой спрайт "Отменить"
        self.shield = GameSprite("./icons/Shield_icon.png", 0, 0, 0, 20, 614, 110, 90)
        self.get_back = GameSprite("./icons/BackToBase.png", 0, 0, 0, 20, 710, 110, 90)
        self.fov = pygame.rect.Rect(0, 0, 0, 0)
        # Build
        self.farm = GameSprite("./icons/Farm_icon.png", 0, 0, 0, 20, 614, 110, 90)
        self.mill = GameSprite("./icons/Mill_icon.png", 0, 0, 0, 150, 614, 110, 90)
        self.barracks = GameSprite("./icons/Barracks_icon.png", 0, 0, 0, 20, 710, 110, 90)
        # Peon
        self.axe = GameSprite("./icons/Axe_icon.png", 0, 0, 0, 150, 614, 110, 90)
        self.auto_farm = GameSprite("./icons/Auto_Farm_icon.png", 0, 0, 0, 20, 805, 110, 90)
        self.build = GameSprite("./icons/Build_icon.png", 0, 0, 0, 150, 805, 110, 90)
        self.repair = GameSprite("./icons/Repair_icon.png", 0, 0, 0, 150, 710, 110, 90)
        self.create_peon = GameSprite("./icons/Peon_icon.png", 0, 0, 0, 20, 614, 110, 90)
        # Spearman
        self.spear = GameSprite("./icons/Spear_icon.png", 0, 0, 0, 150, 614, 110, 90)
        self.create_spearman = GameSprite("./icons/Spearman_icon.png", 0, 0, 0, 20, 614, 110, 90)
        self.create_lumber = GameSprite("./icons/Lumber_icon.png", 0, 0, 0, 150, 614, 110, 90)

        self.avatars_cords, self.avatars_size, self.atributes_cords = (22, 401), (144, 102), (160, 401)
        self.avatars = {
            "Peon": pygame.transform.scale(pygame.image.load('./icons/Peon_icon.png'), self.avatars_size),
            "Spearman": pygame.transform.scale(pygame.image.load('./icons/Spearman_icon.png'), self.avatars_size),
            "Rider": pygame.transform.scale(pygame.image.load('./icons/Rider_icon.png'), self.avatars_size),
            "Lumber": pygame.transform.scale(pygame.image.load('./icons/Lumber_icon.png'), self.avatars_size),
            "Black": pygame.transform.scale(pygame.image.load('./icons/Black_icon.png'), self.avatars_size),
            "Green": pygame.transform.scale(pygame.image.load('./icons/Green_icon.png'), (3, 3)),
            "Axe": pygame.transform.scale(pygame.image.load('./icons/Axe_icon.png'), self.avatars_size),
            "TownHall": pygame.transform.scale(pygame.image.load('./icons/TownHall_icon.png'), self.avatars_size),
            "Barracks": pygame.transform.scale(pygame.image.load('./icons/Barracks_icon.png'), self.avatars_size),
            "Mill": pygame.transform.scale(pygame.image.load('./icons/Mill_icon.png'), self.avatars_size),
            "Farm": pygame.transform.scale(pygame.image.load('./icons/Farm_icon.png'), self.avatars_size),
            "GoldMine": pygame.transform.scale(pygame.image.load('./icons/GoldMine_icon.png'), self.avatars_size),

        }
        self.avatars_knight = {
            "Rider": pygame.transform.scale(pygame.image.load('./icons/Knight_Rider_icon.png'), self.avatars_size),
            "Knight": pygame.transform.scale(pygame.image.load('./icons/Knight_icon.png'), self.avatars_size),
            "Arbalester": pygame.transform.scale(pygame.image.load('./icons/Knight_Arbalester_icon.png'), self.avatars_size),
            "Catapult": pygame.transform.scale(pygame.image.load('./icons/Knight_Catapult_icon.png'), self.avatars_size)
        }

    def map(self):
        self.fov = pygame.rect.Rect((game.map_cords_x/12*-1+Drawing.mini_map.w/12+14, game.map_cords_y/12*-1+Drawing.mini_map.h/12), (self.winsize[0]/12-Drawing.mini_map.w/12, self.winsize[1]/12))
        self.window.blit(Drawing.mini_map.image, (Drawing.mini_map.rect.x, Drawing.mini_map.rect.y))  # Отрисовываем изображение мини-карты
        for orc in self.orcs:
            self.window.blit(pygame.transform.scale(pygame.image.load('./icons/Green_icon.png'), (3, 3)), (Drawing.mini_map.rect.x + orc.rect.x//12, Drawing.mini_map.rect.y + orc.rect.y//12))
        for building in self.buildings:
            if not building.type == 'TownHall':
                self.window.blit(pygame.transform.scale(pygame.image.load('./icons/Green_icon.png'), (6, 6)), (Drawing.mini_map.rect.x + building.rect.x//12, Drawing.mini_map.rect.y + building.rect.y//12))
            else:
                self.window.blit(pygame.transform.scale(pygame.image.load('./icons/Yellow_icon.png'), (6, 6)), (Drawing.mini_map.rect.x + building.rect.x//12, Drawing.mini_map.rect.y + building.rect.y//12))
        if Drawing.mini_map.rect.collidepoint(pygame.mouse.get_pos()):
            if not (pygame.mouse.get_pos()[0] - ((self.winsize[0] // 12) / 2 - Drawing.mini_map.rect.x) < Drawing.mini_map.rect.x
                    or (pygame.mouse.get_pos()[0] + ((self.winsize[0] // 12) / 2 - Drawing.mini_map.w//12)) > (Drawing.mini_map.rect.x + Drawing.mini_map.w-2)
                    or pygame.mouse.get_pos()[1] - ((self.winsize[1] // 12) / 2) < Drawing.mini_map.rect.y
                    or pygame.mouse.get_pos()[1] + ((self.winsize[1] // 12) / 2) > (Drawing.mini_map.rect.y + Drawing.mini_map.h)):
                if pygame.mouse.get_pressed()[0]:
                    game.map_cords_x = ((pygame.mouse.get_pos()[0]*12 - Drawing.mini_map.w - 20 - self.winsize[0]//2) * -1)
                    game.map_cords_y = ((pygame.mouse.get_pos()[1]*12 - Drawing.mini_map.w - 20 - self.winsize[1]//2) * -1)
                pygame.draw.rect(self.window, (255, 255, 0), (pygame.mouse.get_pos()[0]-self.fov.w/2, pygame.mouse.get_pos()[1]-self.fov.h/2, self.fov.w, self.fov.h), 4)
                if pygame.mouse.get_pressed()[0]:
                    Drawing.dx, Drawing.dy = self.fov.x - Drawing.mini_map.rect.x - 6, self.fov.y - Drawing.mini_map.rect.y - 1
                    if not state['pressed_on_mini_map']:    # сдвиг обьектов
                        for orc in self.orcs:
                            orc.rect.x -= Drawing.dx*12
                            orc.rect.y -= Drawing.dy*12
                            print(orc.rect.x, orc.rect.y)
                        state['pressed_on_mini_map'] = True
                else:
                    state['pressed_on_mini_map'] = False
            else:
                pygame.draw.rect(self.window, (255, 0, 0), (pygame.mouse.get_pos()[0]-self.fov.w/2, pygame.mouse.get_pos()[1]-self.fov.h/2, self.fov.w, self.fov.h), 4)
        pygame.draw.rect(self.window, (255, 255, 255), self.fov, 4)

    def menu(self):
        self.map()
        mouse_clicked = pygame.mouse.get_pressed()
        self.window.blit(self.menus_image, (0, 0), )  # Отрисовываем изображение меню
        self.chooses = len([orc for orc in self.orcs if orc.choosed])
        self.knight_chooses = len([knight for knight in self.knights if knight.choosed])
        self.buildings_chooses = len([building for building in self.buildings if building.choosed])

        if self.buildings_chooses > 0:
            for orc in self.orcs:
                orc.choosed = False
            for knight in self.knights:
                knight.choosed = False

            self.window.blit(self.cancel.image, (self.cancel.rect.x, self.cancel.rect.y))
            if mouse_clicked[0]:  # Проверяем, нажата ли левая кнопка мыши
                if self.cancel.rect.collidepoint(pygame.mouse.get_pos()):  # Проверяем, была ли нажата кнопка "Отменить"
                    for building in self.buildings:
                        building.choosed = False

        if self.buildings_chooses == 1:
            for building in self.buildings:
                if building.choosed:
                    self.window.blit(self.avatars[building.type], self.avatars_cords)
                    self.window.blit(self.font.render(building.type, True, (255, 255, 255)), (self.avatars_cords[0], self.avatars_cords[1] + self.avatars_size[1]))
                    self.window.blit(self.font.render("Health: " + str(round(building.health, 2)), True, (255, 255, 255)), self.atributes_cords)
                    if building.type == 'TownHall':
                        if not building.is_clicked:
                            self.window.blit(self.create_peon.image, (self.create_peon.rect.x, self.create_peon.rect.y))
                            if pygame.mouse.get_pressed()[0]:
                                if self.create_peon.rect.collidepoint(pygame.mouse.get_pos()):
                                    if game.wood >= 40 and game.gold >= 450:
                                        building.is_clicked = True
                                        game.wood -= 40
                                        game.gold -= 450
                                        building.choosed = False
                                    else:
                                        print('Не хватает ресурсов')
                                        building.choosed = False
                        else:
                            pygame.draw.rect(self.window, (128, 128, 128), pygame.Rect(self.create_peon.rect.x, self.create_peon.rect.y, 230, 30))
                            pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(self.create_peon.rect.x, self.create_peon.rect.y, 230 * building.cooldawn // building.max_cooldawn, 30))
                            self.window.blit(self.font2.render("% complete", True, (255, 255, 255)), (self.create_peon.rect.centerx+5, self.create_peon.rect.y-2))
                    elif building.type == 'Farm':
                        pygame.draw.rect(self.window, (128, 128, 128), pygame.Rect(20, 614, 230, 30))
                        pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(20, 614, 230 * building.cooldawn // building.max_cooldawn, 30))
                        self.window.blit(self.font2.render("% complete", True, (255, 255, 255)), (20 + 5, 614 - 2))
                    elif building.type == 'GoldMine':
                        self.window.blit(self.font.render("Farmers: " + str(len(game.inside_goldmine)), True, (255, 255, 255)), (self.atributes_cords[0], self.avatars_cords[1]+40))
                        pygame.draw.rect(self.window, (128, 128, 128), pygame.Rect(20, 614, 230, 30))
                        pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(20, 614, 230 * building.gold // building.max_gold, 30))
                        self.window.blit(self.font2.render("% Max", True, (255, 255, 255)), (20 + 5, 614 - 2))
                    elif building.type == 'Barracks':
                        if not building.is_clicked:
                            self.window.blit(self.create_spearman.image, (self.create_spearman.rect.x, self.create_spearman.rect.y))
                            self.window.blit(self.create_lumber.image, (self.create_lumber.rect.x, self.create_lumber.rect.y))
                            if pygame.mouse.get_pressed()[0]:
                                if self.create_spearman.rect.collidepoint(pygame.mouse.get_pos()):
                                    if game.gold >= 400:
                                        building.is_clicked = True
                                        building.spearman = True
                                        game.gold -= 400
                                    else:
                                        building.choosed = False
                                        print('Не хватает ресурсов')
                                if self.create_lumber.rect.collidepoint(pygame.mouse.get_pos()):
                                    if game.gold >= 400:
                                        building.is_clicked = True
                                        building.lumber = True
                                        game.gold -= 400
                                    else:
                                        building.choosed = False
                                        print('Не хватает ресурсов')
                        else:
                            pygame.draw.rect(self.window, (128, 128, 128), pygame.Rect(20, 614, 230, 30))
                            pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(20, 614, 230 * building.cooldawn // building.max_cooldawn, 30))
                            self.window.blit(self.font2.render("% complete", True, (255, 255, 255)), (20 + 5, 614 - 2))

        if self.buildings_chooses > 1:
            self.window.blit(self.font.render("Group " + str(self.buildings_chooses), True, (255, 255, 255)), (self.avatars_cords[0], self.avatars_cords[1] + self.avatars_size[1]))
            self.window.blit(self.avatars['Black'], self.avatars_cords)

        if self.knight_chooses > 0:
            for orc in self.orcs:
                orc.choosed = False
            for building in self.buildings:
                building.choosed = False

            self.window.blit(self.cancel.image, (self.cancel.rect.x, self.cancel.rect.y))
            if mouse_clicked[0]:  # Проверяем, нажата ли левая кнопка мыши
                if self.cancel.rect.collidepoint(pygame.mouse.get_pos()):  # Проверяем, была ли нажата кнопка "Отменить"
                    for knight in self.knights:
                        knight.choosed = False

        if self.knight_chooses == 1:
            for knight in self.knights:
                if knight.choosed:
                    self.window.blit(self.avatars_knight[knight.type], self.avatars_cords)
                    self.window.blit(self.font.render(knight.type, True, (255, 255, 255)), (self.avatars_cords[0], self.avatars_cords[1]+self.avatars_size[1]))
                    self.window.blit(self.font.render("Health: " + str(round(knight.health, 2)), True, (255, 255, 255)), self.atributes_cords)
                    self.window.blit(self.font.render("Damage: " + str(knight.damage), True, (255, 255, 255)), (self.atributes_cords[0], self.atributes_cords[1]+40))
                    self.window.blit(self.font.render("Armor: " + str(knight.armor), True, (255, 255, 255)), (self.atributes_cords[0], self.atributes_cords[1]+80))

        if self.knight_chooses > 1:  # Если выбрано больше одного рыцаря
            self.window.blit(self.font.render("Group " + str(self.knight_chooses), True, (255, 255, 255)), (self.avatars_cords[0], self.avatars_cords[1]+self.avatars_size[1]))  # Отображаем надпись "Группа" и количество выбранных рыцарей
            self.window.blit(self.avatars['Black'], self.avatars_cords)

        if self.chooses > 0:
            for knight in self.knights:
                knight.choosed = False
            for building in self.buildings:
                building.choosed = False
            self.window.blit(self.cancel.image, (self.cancel.rect.x, self.cancel.rect.y))  # Отображаем кнопку "Отменить"
            for orc in self.orcs:
                if orc.choosed:
                    if not orc.building:
                        self.window.blit(self.get_back.image, (self.get_back.rect.x, self.get_back.rect.y))
            if mouse_clicked[0]:  # Проверяем, нажата ли левая кнопка мыши
                if self.cancel.rect.collidepoint(pygame.mouse.get_pos()):  # Проверяем, была ли нажата кнопка "Отменить"
                    for orc in self.orcs:  # Проходимся по всем оркам
                        orc.building = False
                        orc.direction = ''  # Устанавливаем у всех орков пустое направление
                        orc.choosed = False  # Снимаем выделение с орка
                for orc in self.orcs:
                    if orc.choosed:
                        if self.get_back.rect.collidepoint(pygame.mouse.get_pos()):
                            if not orc.building:
                                orc.back_to_base()
                                orc.choosed = False
                                orc.building = False

        if self.chooses == 1:  # Если выбран только один орк
            for orc in self.orcs:  # Проходимся по всем оркам
                if orc.choosed:  # Проверяем, выделен ли текущий
                    self.window.blit(self.avatars[orc.type], self.avatars_cords)
                    self.window.blit(self.font.render(orc.type, True, (255, 255, 255)), (self.avatars_cords[0], self.avatars_cords[1]+self.avatars_size[1]))  # Отображаем тип орка
                    self.window.blit(self.font.render("Health: " + str(round(orc.health, 2)), True, (255, 255, 255)), self.atributes_cords)  # Отображаем количество здоровья орка
                    self.window.blit(self.font.render("Damage: " + str(orc.damage), True, (255, 255, 255)), (self.atributes_cords[0], self.atributes_cords[1]+40))  # Отображаем количество урона, наносимого орком
                    self.window.blit(self.font.render("Armor: " + str(orc.armor), True, (255, 255, 255)), (self.atributes_cords[0], self.atributes_cords[1]+80))
                    if orc.type == 'Peon':
                        if not orc.building:
                            self.window.blit(self.auto_farm.image, (self.auto_farm.rect.x, self.auto_farm.rect.y))
                            self.window.blit(self.build.image, (self.build.rect.x, self.build.rect.y))
                            self.window.blit(self.repair.image, (self.repair.rect.x, self.repair.rect.y))
                            self.window.blit(self.shield.image, (self.shield.rect.x, self.shield.rect.y))
                            self.window.blit(self.get_back.image, (self.get_back.rect.x, self.get_back.rect.y))
                            if mouse_clicked[0]:
                                if self.auto_farm.rect.collidepoint(pygame.mouse.get_pos()):
                                    if orc.farming:
                                        orc.farming = False
                                    else:
                                        orc.farming = True
                                        orc.building = False
                                        print('Farming')
                                    orc.choosed = False
                                if self.build.rect.collidepoint(pygame.mouse.get_pos()):
                                    if orc.building:
                                        orc.building = False
                                    else:
                                        orc.building = True
                                        orc.farming = False
                                        print('Building')
                                if self.shield.rect.collidepoint(pygame.mouse.get_pos()):
                                    if not orc.defense:
                                        orc.toggle_shield()
                                    else:
                                        orc.disable_shield()
                                    orc.choosed = False

                                if self.get_back.rect.collidepoint(pygame.mouse.get_pos()):
                                    orc.back_to_base()
                                    orc.building = False
                                    orc.farming = False
                                    orc.choosed = False
                        else:
                            self.window.blit(self.farm.image, (self.farm.rect.x, self.farm.rect.y))
                            self.window.blit(self.mill.image, (self.mill.rect.x, self.mill.rect.y))
                            self.window.blit(self.barracks.image, (self.barracks.rect.x, self.barracks.rect.y))
                            if mouse_clicked[0]:
                                if self.farm.rect.collidepoint(pygame.mouse.get_pos()):
                                    orc.build_farm = True
                                if self.mill.rect.collidepoint(pygame.mouse.get_pos()):
                                    orc.build_mill = True
                                if self.barracks.rect.collidepoint(pygame.mouse.get_pos()):
                                    orc.build_barracks = True

                    elif orc.type == 'Spearman':
                        self.window.blit(self.shield.image, (self.shield.rect.x, self.shield.rect.y))
                        self.window.blit(self.spear.image, (self.spear.rect.x, self.spear.rect.y))
                        if mouse_clicked[0]:
                            if self.spear.rect.collidepoint(pygame.mouse.get_pos()):
                                if not orc.defense:
                                    if orc.throw:
                                        orc.throw = False
                                        orc.radius -= 10
                                        orc.damage += 1.5
                                    else:
                                        orc.throw = True
                                        orc.radius += 10
                                        orc.damage -= 1.5
                                    orc.choosed = False
                                else:
                                    print("can't attack, you have shield ", "\n")
                                    orc.choosed = False
                            if self.shield.rect.collidepoint(pygame.mouse.get_pos()):
                                if not orc.defense:
                                    orc.toggle_shield()
                                else:
                                    orc.disable_shield()
                                orc.choosed = False
                            if self.get_back.rect.collidepoint(pygame.mouse.get_pos()):
                                orc.back_to_base()
                                orc.building = False
                                orc.farming = False
                                orc.choosed = False
                    elif orc.type == 'Lumber' or orc.type == 'Rider':
                        self.window.blit(self.axe.image, (self.axe.rect.x, self.axe.rect.y))
                        self.window.blit(self.shield.image, (self.shield.rect.x, self.shield.rect.y))
                        self.window.blit(self.get_back.image, (self.get_back.rect.x, self.get_back.rect.y))
                        if mouse_clicked[0]:
                            if self.shield.rect.collidepoint(pygame.mouse.get_pos()):
                                if not orc.defense:
                                    orc.toggle_shield()
                                else:
                                    orc.disable_shield()
                                orc.choosed = False
                            if self.axe.rect.collidepoint(pygame.mouse.get_pos()):
                                if not orc.defense:
                                    if orc.attacks:
                                        orc.attacks = False
                                    else:
                                        orc.attacks = True
                                    orc.choosed = False
                                else:
                                    print("can't attack, you have shield ", "\n")
                                    orc.choosed = False
                            if self.get_back.rect.collidepoint(pygame.mouse.get_pos()):
                                orc.back_to_base()
                                orc.building = False
                                orc.farming = False
                                orc.choosed = False

        if self.chooses > 1:  # Если выбрано больше одного орка
            self.window.blit(self.font.render("Group " + str(self.chooses), True, (255, 255, 255)), (self.avatars_cords[0], self.avatars_cords[1]+self.avatars_size[1]))  # Отображаем надпись "Группа" и количество выбранных орков
            self.window.blit(self.avatars['Black'], self.avatars_cords)

        if self.chooses == 0 and self.knight_chooses == 0 and self.buildings_chooses == 0:
            self.window.blit(self.avatars['Black'], self.avatars_cords)

        self.window.blit(self.font1.render("Lumber: " + str(game.wood), True, (255, 255, 255)), (game.winsize[0]//4, -10))
        self.window.blit(self.font1.render("Gold: " + str(game.gold), True, (255, 255, 255)), (game.winsize[0]//1.4, -10))


class Building(GameSprite):
    def __init__(self, img, speed, health, damage, x, y, w, h, type):
        super().__init__(img, speed, health, damage, x, y, w, h)
        self.type = type
        self.choosed = False
        self.is_clicked = False
        self.spearman, self.lumber = False, False
        self.cooldawn = 350 if self.type == 'TownHall' or self.type == 'Barracks' else 500
        self.max_cooldawn = self.cooldawn
        self.gold = 3500
        self.max_gold = self.gold

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.choosed = True
        if self.choosed:
            self.hitbox()
        if self.type == 'TownHall':
            if self.is_clicked:
                self.cooldawn -= 1
                if self.cooldawn <= 0:
                    self.cooldawn = self.max_cooldawn
                    game.orcs.add(Player("./peon.png", 2, 5, 1, 2, self.rect.x-50, self.rect.y, 35, 35, 'Peon', 15))
                    self.is_clicked = False
        if self.type == 'Farm':
            self.cooldawn -= 1
            if self.cooldawn <= 0:
                game.wood += 15
                self.cooldawn = self.max_cooldawn
        if self.type == 'GoldMine':
            for orc in game.inside_goldmine:
                orc.cooldawn_gold -= 1
                if orc.cooldawn_gold <= 0:
                    self.gold -= 10
                    orc.gold += 10
                    orc.cooldawn_gold = orc.cooldawn_gold_max
                if orc.gold >= 100:
                    orc.kill()
                    game.orcs.add(orc)
                    orc.rect.x, orc.rect.y = self.rect.x - 70, self.rect.y
                    orc.direction = ''
            if self.gold <= 0:
                self.kill()
                for orc in game.inside_goldmine:
                    orc.rect.x, orc.rect.y = self.rect.x-70, self.rect.y
                    game.orcs.add(orc)
        if self.type == 'Barracks':
            if self.is_clicked:
                self.cooldawn -= 1
                if self.cooldawn <= 0:
                    if self.spearman:
                        game.orcs.add(Player("Spearman.png", 2, 10, 4, 4, self.rect.x-70, self.rect.y, 40, 40, 'Spearman', 25))
                    if self.lumber:
                        game.orcs.add(Player("lumber.png", 2, 10, 4, 4, self.rect.x-70, self.rect.y, 40, 40, 'Lumber', 15))
                    self.spearman = False
                    self.lumber = False
                    self.is_clicked = False
                    self.cooldawn = self.max_cooldawn


class Player(GameSprite):
    def __init__(self, img, speed, health, damage, armor, x, y, w, h, type, radius):
        super().__init__(img, speed, health, damage, x, y, w, h)
        self.armor = armor
        self.radius = radius
        self.type = type  # тип героя
        self.direction = ''  # направление
        self.gold = 0
        self.collect_wood = self.type == 'Peon'  # если он лесоруб, то может собирать дерево
        self.cooldawn_wood = 800
        self.cooldawn_attack = 200 if self.type == 'Rider' or self.type == 'Spearman' else 250
        self.cooldawn_max = self.cooldawn_attack
        self.cooldawn_gold = 350
        self.cooldawn_gold_max = self.cooldawn_gold
        self.choosed = False  # выбран ли герой
        self.defense = False
        self.can_attack = not self.type == 'Peon'
        self.farming = False
        self.building = False
        self.attacks = True if self.type == 'Spearman' else False
        self.throw = False      # spearman
        self.nowbuilding = False
        self.build_farm, self.build_mill, self.build_barracks = False, False, False

        self.x2, self.y2 = 0, 0  # позиция, куда кликнута была мышка
        self.angle, self.a, self.b, self.c = 0, 0, 0, 0  # катеты и гипотенуза, для равномерного перемещение  / угол поворота
        self.dx, self.dy = 0, 0  # равномерное смещение
        self.radius_hitbox = pygame.Rect((self.rect.x-self.radius, self.rect.y-self.radius), (self.w+self.radius*2, self.h+self.radius*2))

    def radius1(self):
        self.radius_hitbox = pygame.Rect((self.rect.x-self.radius, self.rect.y-self.radius), (self.w+self.radius*2, self.h+self.radius*2))
        # pygame.draw.rect(game.window, (255, 0, 0), self.radius_hitbox, 1)radius_hitbox

    def click(self):
        # Выбор героя
        if len([orc for orc in game.orcs if orc.building]) == 0:
            mouse_clicked = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if mouse_clicked[0]:
                if self.new_rect.collidepoint(mouse_pos):
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
                    if game.menu.mini_map.rect.collidepoint(pygame.mouse.get_pos()):
                        self.x2 *= 12
                        self.y2 *= 12
                    # Разность сторон y, катет
                    self.b = abs(self.new_rect.y - a1[1])

                    # Разность сторон x, катет
                    self.a = abs(self.new_rect.x - a1[0])

                    # Гиппотенуза
                    self.c = math.sqrt(self.a ** 2 + self.b ** 2)

                    # Предотвращение вылета при делении на ноль
                    try:
                        self.angle = math.atan(self.a / self.b) * (180 / math.pi)
                    except ZeroDivisionError:
                        pass
                    pygame.draw.line(game.window, (255, 0, 0), (self.new_rect.centerx, self.new_rect.centery), a1)

                    # Равномерное смещене по y
                    self.dy = math.cos(math.radians(self.angle)) * self.speed

                    # Равномерное смешение по x
                    self.dx = math.sin(math.radians(self.angle)) * self.speed

                    # Выбор четверти кординатной плоскости
                    if self.new_rect.centerx < self.x2 and self.new_rect.centery < self.y2:
                        self.direction = '4'
                    if self.new_rect.centerx < self.x2 and self.new_rect.centery > self.y2:
                        self.direction = '1'
                    if self.new_rect.centerx > self.x2 and self.new_rect.centery < self.y2:
                        self.direction = '3'
                    if self.new_rect.centerx > self.x2 and self.new_rect.centery > self.y2:
                        self.direction = '2'
                    try:
                        if game.menu.menu_mask.get_at(pygame.mouse.get_pos()) \
                                or game.menu.mini_map.rect.collidepoint(pygame.mouse.get_pos())\
                                and not game.menu.mini_map.rect.collidepoint(pygame.mouse.get_pos()):
                            self.direction = ''
                    except IndexError:  # Если происходит ошибка индексации
                        pass  # Пропускаем
                    for building in game.buildings:
                        if building.rect.collidepoint(pygame.mouse.get_pos()):
                            if building.type == 'GoldMine':
                                if not self.type == 'Peon':
                                    self.direction = ''

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
        for building in game.buildings:
            if building.type == 'GoldMine':
                if self.rect.colliderect(building):
                    if self.type == 'Peon':
                        self.kill()
                        game.inside_goldmine.add(self)
                    else:
                        self.rect.x, self.rect.y = building.rect.x - 70, building.rect.y
            if building.type == 'TownHall':
                if self.rect.colliderect(building):
                    if self.gold >= 0:
                        self.kill()
                        game.gold += self.gold
                        self.gold -= self.gold
                        self.rect.x, self.rect.y, self.direction = building.rect.x - random.randint(70, 85), random.randint(building.rect.y, building.rect.y + 15), ''
                        game.orcs.add(self)
            if building.type == 'Farm' or building.type == 'Barracks':
                if self.new_rect.colliderect(building):
                    self.rect.x, self.rect.y = building.rect.x - 70, building.rect.y

    def auto_farm(self):

        if self.collect_wood:
            for tree in game.trees:
                if tree.rect.colliderect(self.radius_hitbox):
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
                    game.wood += 10

    def construct(self):
        if self.building:
            if self.build_farm:
                for orc in game.orcs:
                    if pygame.rect.Rect(pygame.mouse.get_pos(), (80, 80)).colliderect(orc):
                        pygame.draw.rect(game.window, (255, 0, 0), (pygame.mouse.get_pos(), (80, 80)), 1)
                    else:
                        pygame.draw.rect(game.window, (255, 255, 255), (pygame.mouse.get_pos(), (80, 80)), 1)
            if self.build_mill:
                pygame.draw.rect(game.window, (255, 255, 255), (pygame.mouse.get_pos(), (85, 85)), 1)
            if self.build_barracks:
                pygame.draw.rect(game.window, (255, 255, 255), (pygame.mouse.get_pos(), (90, 90)), 1)

    def back_to_base(self):
        try:
            for building in game.buildings:
                if building.type == 'TownHall':
                    self.x2, self.y2 = building.rect.x, building.rect.y
                    self.a = abs(self.rect.x - building.rect.x)
                    self.b = abs(self.rect.y - building.rect.y)
                    self.c = math.sqrt(self.a ** 2 + self.b ** 2)
                    self.angle = math.atan(self.a / self.b) * (180 / math.pi)
                    self.dy = math.cos(math.radians(self.angle)) * self.speed
                    self.dx = math.sin(math.radians(self.angle)) * self.speed
                    if self.rect.centerx < self.x2 and self.rect.centery < self.y2:
                        self.direction = '4'
                    if self.rect.centerx < self.x2 and self.rect.centery > self.y2:
                        self.direction = '1'
                    if self.rect.centerx > self.x2 and self.rect.centery < self.y2:
                        self.direction = '3'
                    if self.rect.centerx > self.x2 and self.rect.centery > self.y2:
                        self.direction = '2'
                    self.move()
        except ZeroDivisionError:
            pass

    def attack(self):
        for knight in game.knights:
            if self.radius_hitbox.colliderect(knight):
                self.cooldawn_attack -= 1
                if self.cooldawn_attack == self.cooldawn_max - self.cooldawn_max // 5:
                    knight.health -= self.damage-(self.damage*knight.armor/10)
                    # animate
                elif self.cooldawn_attack == self.cooldawn_max - self.cooldawn_max // 5 * 2:
                    knight.health -= self.damage - (self.damage * knight.armor / 10)
                    # animate
                elif self.cooldawn_attack == self.cooldawn_max - self.cooldawn_max // 5 * 3:
                    knight.health -= self.damage - (self.damage * knight.armor / 10)
                    # animate
                elif self.cooldawn_attack == self.cooldawn_max - self.cooldawn_max // 5 * 4:
                    knight.health -= self.damage - (self.damage * knight.armor / 10)
                    # animate
                elif self.cooldawn_attack == self.cooldawn_max - self.cooldawn_max // 5 * 5: # сколько анимаций на столько и делить частей
                    knight.health -= self.damage - (self.damage * knight.armor / 10)
                    # animate
                    self.cooldawn_attack = self.cooldawn_max

    def toggle_shield(self):
        self.armor += 2
        self.speed -= 1
        self.defense = True
        print('shield activate', '\n', "defense - ", self.defense, "\n")

    def disable_shield(self):
        self.armor -= 2
        self.speed += 1
        self.defense = False
        print('shield was disable', '\n', "defense - ", self.defense, "\n")


class Knight(GameSprite):
    def __init__(self, img, speed, health, damage, armor, x, y, w, h, type, radius):
        super().__init__(img, speed, health, damage, x, y, w, h)
        self.armor = armor
        self.type = type
        self.radius = radius
        self.cooldawn_attack = 200 if self.type == 'Rider' or self.type == 'Arbalester' else 250
        self.cooldawn_max = self.cooldawn_attack
        self.radius_hitbox = pygame.Rect((self.rect.x - self.radius, self.rect.y - self.radius), (self.w + self.radius * 2, self.h + self.radius * 2))

    def radius1(self):
        self.radius_hitbox = pygame.Rect((self.rect.x - self.radius, self.rect.y - self.radius), (self.w + self.radius * 2, self.h + self.radius * 2))
        # pygame.draw.rect(game.window, (255, 0, 0), self.radius_hitbox, 1)

    def attack(self):
        for orc in game.orcs:
            if self.radius_hitbox.colliderect(orc):
                self.cooldawn_attack -= 1
                if self.cooldawn_attack == self.cooldawn_max - self.cooldawn_max // 5:
                    orc.health -= self.damage - (self.damage * orc.armor / 10)
                    # animate
                elif self.cooldawn_attack == self.cooldawn_max - self.cooldawn_max // 5 * 2:
                    orc.health -= self.damage - (self.damage * orc.armor / 10)
                    # animate
                elif self.cooldawn_attack == self.cooldawn_max - self.cooldawn_max // 5 * 3:
                    orc.health -= self.damage - (self.damage * orc.armor / 10)
                    # animate
                elif self.cooldawn_attack == self.cooldawn_max - self.cooldawn_max // 5 * 4:
                    orc.health -= self.damage - (self.damage * orc.armor / 10)
                    # animate
                elif self.cooldawn_attack == self.cooldawn_max - self.cooldawn_max // 5 * 5:  # сколько анимаций на столько и делить частей
                    orc.health -= self.damage - (self.damage * orc.armor / 10)
                    # animate
                    self.cooldawn_attack = self.cooldawn_max

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.choosed = True
        self.hitbox() if self.choosed else 0

    def auto_attack(self):
        self.update()
        self.attack()
        self.radius1()


class Game:
    def __init__(self):
        self.winsize = (1560, 1060)
        self.game = True
        self.window = pygame.display.set_mode(self.winsize)
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.map_cords_x = 0+321
        self.map_cords_y = 12
        self.map_size = (3780, 4200)
        self.background = pygame.transform.scale(pygame.image.load("./map.png"), self.map_size)
        self.orcs = pygame.sprite.Group()
        self.knights = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.inside_goldmine = pygame.sprite.Group()
        self.fogs = pygame.sprite.Group()
        self.menu = Drawing(self.window, self.background, self.orcs, self.knights, self.buildings, self.winsize, self.map_size, self.map_cords_x, self.map_cords_y)  # menu
        self.wood = 40
        self.gold = 450
        self.create()

    def create(self):
        x, y = 500, 550
        for i in range(5):
            self.orcs.add(Player("./rider1.png", 3, 10, 3, 4, x, y, 40, 40, 'Rider', 15))
            x += 75
            y += 50
        x, y = 350, 490
        for i in range(15):
            x += 50
            self.orcs.add(Player("./peon.png", 2, 5, 1, 2, x, y, 35, 35, 'Peon', 15))
        x, y = 400, 670
        for i in range(3):
            self.orcs.add(Player("lumber.png", 2, 10, 4, 4, x, y, 40, 40, 'Lumber', 15))
            x += 50
            y += 50
        x, y = 420, 110
        for b in range(5):
            y += 30
            for n in range(5):
                self.trees.add(GameSprite("./tree.png", 0, 3, 0, x, y, 40, 40))
                x += 30
            x = 420
        x = 1200
        for i in range(3):
            self.knights.add(Knight("knight.png", 3, 10, 4, 4, x, 500, 40, 40, 'Rider', 15))
            x += 80
        # random spawn goldmine
        chunks_w = int(self.map_size[0]/self.winsize[0])
        chunks_h = int(self.map_size[1]/self.winsize[1])

        self.orcs.add(Player("Spearman.png", 2, 10, 4, 4, 1150, 400, 40, 40, 'Spearman', 25))
        self.buildings.add(Building("TownHall.png", 0, 15, 0, 880, 130, 100, 100, 'TownHall'))
        self.buildings.add(Building("Farm.png", 0, 10, 0, 1000, 300, 80, 80, 'Farm'))
        self.buildings.add(Building('GoldMine.png', 0, 100, 0, 800, 300, 80, 80, 'GoldMine'))
        self.buildings.add(Building('Barracks.png', 0, 10, 0, 600, 300, 90, 90, 'Barracks'))
        # fog
        size_fog = 60
        n = self.map_size[0]//size_fog
        g = self.map_size[1]//size_fog
        x, y = 0, 0
        for o in range(n):
            for p in range(g):
                self.fogs.add(Fog(x, y, size_fog, size_fog))
                x += size_fog
            y += size_fog
            x = 0

    def run(self):
        while self.game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game = False
            keys = pygame.key.get_pressed()
            for player in self.orcs:
                if keys[pygame.K_d]:
                    player.rect.x += 3
                if keys[pygame.K_a]:
                    player.rect.x -= 3
                if keys[pygame.K_w]:
                    player.rect.y -= 3
                if keys[pygame.K_s]:
                    player.rect.y += 3
            self.window.blit(self.background, (self.map_cords_x, self.map_cords_y))
            self.trees.draw(self.window)
            for orc in self.orcs:
                orc.click()
                orc.radius1()
                orc.draw(self.window)
                if not orc.type == 'Peon' and orc.attacks and not orc.defense:
                    orc.attack()
                if orc.type == 'Peon':
                    if orc.farming:
                        orc.auto_farm()
                if orc.health <= 0:
                    orc.kill()
            for knight in self.knights:
                knight.draw(self.window)
                knight.auto_attack()
                if knight.health <= 0:
                    knight.kill()
            for building in self.buildings:
                building.draw(self.window)
                building.update()
            for fog in self.fogs:
                #if fog.rect.colliderect(self.map_cords_x*-1+self.menu.mini_map.w, self.map_cords_y*-1, self.winsize[0]-self.menu.mini_map.w, self.winsize[1]): # если туман в зоне видимости, то отрисовать туман, чтобы не нагружать
                fog.draw(self.window)
                for orc in self.orcs:
                    if orc.new_rect.colliderect(fog.rect):
                        fog.kill()
                for building in self.buildings:
                    if not building.type == 'GoldMine':
                        if building.rect.colliderect(fog.rect):
                            fog.kill()
            #pygame.draw.rect(self.window, (0, 0, 255), (self.map_cords_x*-1+self.menu.mini_map.w, self.map_cords_y*-1, self.winsize[0]-self.menu.mini_map.w, self.winsize[1]), 3) # зона видимости
            self.menu.menu()
            self.clock.tick(self.fps)
            pygame.display.update()


game = Game()
game.run()