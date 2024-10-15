import pygame.sprite
from constants_imports import *


# Класс преград
class Wall(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width)
        self.rect.y = random.randrange(screen_height)


# Класс снарядов
class Bullet(pygame.sprite.Sprite):
    # Процесс создания: <Имя> = <Класс>(скорость, цвет, дистанция, тип существа*)
    def __init__(self, x, y, speed, distance, color, cr_type=0):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.distance = distance
        self.cr_type = cr_type

        self.image = pygame.Surface((9, 9))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Проверка на то, чей был снаряд (монстра или игрока)
        if self.cr_type == 1:
            self.dx, self.dy = Player.rect.center[0] - self.rect.x, Player.rect.center[1] - self.rect.y
        else:
            self.dx, self.dy = pygame.mouse.get_pos()[0] - self.rect.x, pygame.mouse.get_pos()[1] - self.rect.y
        dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / dist, self.dy / dist

    # Функция отвечающая за обновление действий
    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        # Если снаряд _монстра_ попадает по игроку
        if self.cr_type == 1 and pygame.sprite.collide_rect(Player, self) and Player.color != RED:
            all_sprites.remove(self)
            Player.rect.x += self.dx * Player.speed * 4
            Player.rect.y += self.dy * Player.speed * 4
            Player.life_points -= 1
        elif self.distance <= 0:
            all_sprites.remove(self)

        # Если снаряд игрока
        if self.cr_type == 0:
            # Проходимся по всем монстрам и проверяем столкновение
            for en in Enemies:
                if pygame.sprite.collide_rect(en, self):
                    # Если гарпунщик, нужно удалить его крюк
                    if en == harpooner:
                        # harpooner.stan = False
                        try:
                            harpooner.hook_del()
                        except AttributeError:
                            pass
                    if en == beekeeper.beehive:
                        beekeeper.counter_of_beehive -= 1

                    all_sprites.remove(self)
                    all_sprites.remove(en)
                    Enemies.remove(en)

                    Player.kills += 1
                    en.rect.x = random.randrange(screen_width)
                    en.rect.y = random.randrange(screen_height)
        elif self.distance <= 0:
            all_sprites.remove(self)
        self.distance -= self.speed

        # Если столкновение с преградой, уничтожаем объект
        if pygame.sprite.spritecollide(self, all_walls_sprites, False, pygame.sprite.collide_rect):
            all_sprites.remove(self)


# Класс монстра: Скелет
class Sceleton(pygame.sprite.Sprite):
    def __init__(self, width, height, name, damage, life_points, speed, color, distance):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.name = name
        self.damage = damage
        self.life_points = life_points
        self.speed = speed
        self.color = color
        self.distance = distance
        self.clock = 0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width)
        self.rect.y = random.randrange(screen_height)

        # Проверка на то, что существо появится не в других существах
        while pygame.sprite.spritecollide(self, all_sprites, False, pygame.sprite.collide_rect):
            self.rect.x = random.randrange(screen_width)
            self.rect.y = random.randrange(screen_height)

    # Функция отвечающая за измерение расстояния и пути до игрока
    def check_dist(self):
        dx, dy = Player.rect.center[0] - self.rect.x, Player.rect.center[1] - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist

        # Проверка на необходимость подходить ближе, чтобы снаряд долетел
        if self.distance <= dist:
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        elif self.clock >= 100 and self.distance > dist:
            # Создание объекта (принцип около класса)
            bullet = Bullet(self.rect.center[0], self.rect.center[1], self.speed + 5, self.distance, self.color, 1)
            all_sprites.add(bullet)
            self.clock = 0

    # Функция отвечающая за обновление действий
    def update(self):
        self.check_dist()
        self.clock += 1


# Класс монстра: Зомби
class Zombie(pygame.sprite.Sprite):
    def __init__(self, width, height, name, damage, life_points, speed, color):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.name = name
        self.damage = damage
        self.life_points = life_points
        self.speed = speed
        self.color = color
        self.clock = 0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width)
        self.rect.y = random.randrange(screen_height)

        # Проверка на то, что существо появится не в других существах
        while pygame.sprite.spritecollide(self, all_sprites, False, pygame.sprite.collide_rect):
            self.rect.x = random.randrange(screen_width)
            self.rect.y = random.randrange(screen_height)

    # Функция отвечающая за измерение расстояния и пути до игрока
    def check_dist(self):
        dx, dy = Player.rect.center[0] - self.rect.x, Player.rect.center[1] - self.rect.y
        dist = math.hypot(dx, dy) + 1
        dx, dy = dx / dist, dy / dist

        # Проверка на столкновение
        if pygame.sprite.collide_rect(self, Player) and Player.color != RED and not Player.stan:
            Player.rect.x += dx * Player.speed * 4
            Player.rect.y += dy * Player.speed * 4
            Player.life_points -= 1

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    # Функция отвечающая за обновление действий
    def update(self):
        self.check_dist()


# Класс монстра: Гарпунщик
class Harpooner(pygame.sprite.Sprite):
    # Класс крюка для "Harpooner"
    class Hook(pygame.sprite.Sprite):
        # Процесс создания: <Имя> = <Класс>(скорость, дистанция, цвет)
        def __init__(self, x, y, speed, distance, color):
            pygame.sprite.Sprite.__init__(self)
            self.speed = speed
            self.distance = distance
            self.color = color
            self.counter = self.distance

            self.image = pygame.Surface((7, 14))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.dx, self.dy = Player.rect.center[0] - self.rect.x, Player.rect.center[1] - self.rect.y
            dist = math.hypot(self.dx, self.dy)
            self.dx, self.dy = self.dx / dist, self.dy / dist

        # Функция отвечающая за обновление действий
        def update(self):
            harpooner.stan = True
            # Крюк работает следующим образом: выстрел, если столкновение, притягиваем на _тоже_ расстояние,
            # иначе, удаляем объект (ещё, пока игрок притягивается, он оглушён)
            if pygame.sprite.collide_rect(Player, self) and Player.color != RED and self.counter >= 0:
                Player.stan = True
                Player.rect.x -= self.dx * self.speed
                Player.rect.y -= self.dy * self.speed
                self.rect.x -= self.dx * self.speed
                self.rect.y -= self.dy * self.speed
                self.counter -= self.speed

            elif self.distance <= 0:
                all_sprites.remove(self)
                Player.stan = False
                harpooner.stan = False

            else:
                self.rect.x += self.dx * self.speed
                self.rect.y += self.dy * self.speed
                self.distance -= self.speed

            pygame.draw.line(screen, self.color, harpooner.rect.center, self.rect.center, 3)

            if pygame.sprite.collide_rect(Player, harpooner) and pygame.sprite.collide_rect(Player, self) \
                    and Player.color != RED:
                Player.stan = False
                harpooner.stan = False
                Player.life_points -= 1
                Player.rect.x += self.dx * Player.speed * 4
                Player.rect.y += self.dy * Player.speed * 4
                all_sprites.remove(self)

    def __init__(self, width, height, name, damage, life_points, speed, color, distance):
        pygame.sprite.Sprite.__init__(self)
        self.hook = None
        self.width = width
        self.height = height
        self.name = name
        self.damage = damage
        self.life_points = life_points
        self.speed = speed
        self.color = color
        self.distance = distance
        self.clock = 0

        self.stan = False

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width)
        self.rect.y = random.randrange(screen_height)

        # Проверка на то, что существо появится не в других существах
        while pygame.sprite.spritecollide(self, all_sprites, False, pygame.sprite.collide_rect):
            self.rect.x = random.randrange(screen_width)
            self.rect.y = random.randrange(screen_height)

    # Функция отвечающая за измерение расстояния и пути до игрока
    def check_dist(self):
        dx, dy = Player.rect.center[0] - self.rect.x, Player.rect.center[1] - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist

        # Проверка на необходимость подходить ближе, чтобы крюк долетел
        if self.distance <= dist + 5:
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        elif self.clock >= 170 and self.distance > dist + 5:
            # Создание объекта (принцип около класса)
            self.hook = self.Hook(self.rect.center[0], self.rect.center[1], self.speed + 10, self.distance, self.color)
            all_sprites.add(self.hook)
            self.clock = 0

    # Функция удаления крюка и снятие эффектов, после смерти гарпунщика
    def hook_del(self):
        self.stan = False
        Player.stan = False
        all_sprites.remove(self.hook)

    # Функция отвечающая за обновление действий
    def update(self):
        self.check_dist()
        self.clock += 1


# Класс монстра: Призрак
class Ghost(pygame.sprite.Sprite):
    def __init__(self, width, height, name, damage, life_points, speed, color, distance):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.name = name
        self.damage = damage
        self.life_points = life_points
        self.speed = speed
        self.color = color
        self.distance = distance
        self.clock = 0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width)
        self.rect.y = random.randrange(screen_height)

        # Проверка на то, что существо появится не в других существах
        while pygame.sprite.spritecollide(self, all_sprites, False, pygame.sprite.collide_rect):
            self.rect.x = random.randrange(screen_width)
            self.rect.y = random.randrange(screen_height)

    # Функция отвечающая за измерение расстояния и пути до игрока
    def check_dist(self):
        dx, dy = Player.rect.center[0] - self.rect.x, Player.rect.center[1] - self.rect.y
        dist = math.hypot(dx, dy) + 1
        dx, dy = dx / dist, dy / dist

        # Проверка на необходимость подходить ближе, для рывка к игроку
        if self.distance <= dist:
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        elif self.distance > dist:
            if self.clock >= 50:
                self.rect.x += dx * (self.speed + 5)
                self.rect.y += dy * (self.speed + 5)
            self.clock += 1

    def update(self):
        self.check_dist()
        if pygame.sprite.collide_rect(Player, self) and Player.color != RED:
            Player.slowing = True
            Enemies.remove(self)
            all_sprites.remove(self)
            self.rect.x = random.randrange(screen_width)
            self.rect.y = random.randrange(screen_height)


# Класс монстра: Пасечник
class Beekeeper(pygame.sprite.Sprite):
    # Класс улья для "Beekeeper"
    class Beehive(pygame.sprite.Sprite):
        # Класс пчелы для "Beehive"
        class Bee(pygame.sprite.Sprite):
            def __init__(self, x, y, width, height, life_points, speed, color):
                pygame.sprite.Sprite.__init__(self)
                self.width = width
                self.height = height
                self.life_points = life_points
                self.speed = speed
                self.color = color
                self.clock = 0

                self.image = pygame.Surface((self.width, self.height))
                self.image.fill(color)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

            def check_dist(self):
                dx, dy = Player.rect.center[0] - self.rect.x, Player.rect.center[1] - self.rect.y
                dist = math.hypot(dy, dx) + 1
                dx, dy = dx / dist, dy / dist

                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed

                # Проверка на столкновение
                if pygame.sprite.collide_rect(self, Player) and Player.color != RED and not Player.stan or self.clock > 300:
                    Player.rect.x += dx * Player.speed * 4
                    Player.rect.y += dy * Player.speed * 4
                    self.clock = 0
                    all_sprites.remove(self)

            def update(self):
                self.check_dist()
                self.clock += 1

        def __init__(self, x, y, width, height, life_points, color):
            pygame.sprite.Sprite.__init__(self)
            self.width = width
            self.height = height
            self.life_points = life_points
            self.color = color
            self.clock = 0
            self.counter_of_bee = 0

            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            # Создаём объект
            if self.clock > 300:
                bee = self.Bee(self.rect.center[0], self.rect.center[1], 7, 7, 1, 6, YELLOW)
                all_sprites.add(bee)
                self.clock = 0
            self.clock += 1

    def __init__(self, width, height, name, damage, life_points, speed, color):
        pygame.sprite.Sprite.__init__(self)
        self.beehive = None
        self.width = width
        self.height = height
        self.name = name
        self.damage = damage
        self.life_points = life_points
        self.speed = speed
        self.color = color
        self.clock = 0
        self.counter_of_beehive = 0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # Временно* координаты пасечника будут примерно в центре экрана
        self.rect.x = random.randrange(screen_width//6, screen_width - screen_width//6)
        self.rect.y = random.randrange(screen_height//6, screen_height - screen_height//6)

        # Проверка на то, что существо появится не в других существах
        while pygame.sprite.spritecollide(self, all_sprites, False, pygame.sprite.collide_rect):
            self.rect.x = random.randrange(screen_width//6, screen_width - screen_width//6)
            self.rect.y = random.randrange(screen_height//6, screen_height - screen_height//6)

    def check_dist(self):
        dx, dy = (self.beehive.rect.x - 30 - self.rect.x, self.beehive.rect.y - 30 - self.rect.y)
        dist = math.hypot(dx, dy) + 1
        dx, dy = dx / dist, dy / dist

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def update(self):

        if self.clock > 150 and self.counter_of_beehive <= 2:
            # Создаём объект если ульев не более 2
            self.beehive = self.Beehive(random.randint(self.rect.x - 150, self.rect.x + 150),
                                        random.randint(self.rect.y - 150, self.rect.y + 150),
                                        self.width, self.height // 2, 1, BROWN2)
            all_sprites.add(self.beehive)
            Enemies.append(self.beehive)
            self.counter_of_beehive += 1
            self.clock = 0

        if self.counter_of_beehive > 0:
            self.check_dist()

        self.clock += 1


# Класс персонажа
class Person(pygame.sprite.Sprite):
    def __init__(self, width, height, name, damage, life_points, speed, color):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.name = name
        self.damage = damage
        self.life_points = life_points
        self.speed = speed
        self.color = color
        self.clock = 0
        self.kills = 0

        # Статус игрока (замедление, оглушение и т.д.)
        self.stan = False
        self.slowing = False
        self.slow_time = 0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 80

    # Функция отвечающая за атаку
    def attack(self):
        if self.clock >= 15:
            # Создание объекта (принцип около класса)
            bullet = Bullet(self.rect.center[0], self.rect.center[1], self.speed + 5, 800, self.color)
            all_sprites.add(bullet)
            self.clock = 0

    # Функция отвечающая за обновление действий
    def update(self):
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()
        # Если персонаж не в "стане"
        if not self.stan:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
            elif keys[pygame.K_UP]:
                self.rect.y -= self.speed
        # Режим "разработчика" (неуязвимость)*
        if keys[pygame.K_1]:
            self.color = RED
        if keys[pygame.K_2]:
            self.color = WHITE
        self.image.fill(self.color)

        if self.life_points <= 0:
            pygame.quit()
            exit()
        if mouse_keys[0]:
            self.attack()

        if self.slowing and self.slow_time == 0:
            self.speed -= 7
        if self.slowing and self.slow_time < 300:
            self.slow_time += 1
        elif self.slowing and self.slow_time >= 300:
            self.slowing = False
            self.speed += 5
            self.slow_time = 0
        self.clock += 1


# Список монстров
Enemies = []

# Создание объектов классов
# Процесс создания: <Имя> = <Класс>(ширина, высота, имя, урон, очки жизни, скорость, цвет, дистанция*)
zombie = Zombie(15, 45, 'Zombie', 0, 0, 3, GREEN)
sceleton = Sceleton(15, 45, 'Sceleton', 0, 0, 2, GREY, 400)
harpooner = Harpooner(15, 45, 'Harpooner', 0, 0, 2, AQUA, 300)
ghost = Ghost(15, 45, 'Ghost', 0, 0, 1.5, PURPLE, 250)
beekeeper = Beekeeper(15, 45, 'Beekeeper', 0, 0, 2, YELLOW)


# Функция появления существ
def spawn_creatures():
    # Костыль: персонаж иногда остаётся в стане, даже после смерти врагов
    Player.stan = False
    # Добавление их в группу спрайтов и список
    all_sprites.add(zombie, sceleton, harpooner, ghost, beekeeper)
    Enemies.append(zombie)
    Enemies.append(sceleton)
    Enemies.append(harpooner)
    Enemies.append(ghost)
    Enemies.append(beekeeper)


# Создание Игрока и добавление в группу
Player = Person(15, 45, 'Hero', 1, 10, 10, WHITE)
all_sprites.add(Player)

# for _ in range(5):
#     Walls = Wall(BROWN)
#     all_walls_sprites.add(Walls)
