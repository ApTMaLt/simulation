import pygame
import random
import math
import main_menu

background_colour = (255, 255, 255)
(width, height) = (900, 900)


def addVectors(ygol1, dlina1, ygol2, dlina2):
    x = math.sin(ygol1) * dlina1 + math.sin(ygol2) * dlina2
    y = math.cos(ygol1) * dlina1 + math.cos(ygol2) * dlina2

    ygol = 0.5 * math.pi - math.atan2(y, x)
    dlina = math.hypot(x, y)

    return (ygol, dlina)


def findParticle(particles, x, y):
    for particle in particles:
        if math.hypot(particle.x - x, particle.y - y) <= particle.size:
            return particle
    return None


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        ygol = math.atan2(dy, dx) + 0.5 * math.pi
        obh_massa = p1.mass + p2.mass

        (p1.ygol, p1.speed) = addVectors(p1.ygol, p1.speed * (p1.mass - p2.mass) / obh_massa,
                                         ygol, 2 * p2.speed * p2.mass / obh_massa)
        (p2.ygol, p2.speed) = addVectors(p2.ygol, p2.speed * (p2.mass - p1.mass) / obh_massa,
                                         ygol + math.pi, 2 * p1.speed * p1.mass / obh_massa)
        p1.speed *= elasticity
        p2.speed *= elasticity

        perekritie = 0.5 * (p1.size + p2.size - dist + 1)
        p1.x += math.sin(ygol) * perekritie
        p1.y -= math.cos(ygol) * perekritie
        p2.x -= math.sin(ygol) * perekritie
        p2.y += math.cos(ygol) * perekritie


class Particle():
    def __init__(self, x, y, size, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.speed = 0
        self.ygol = 0
        self.mass = mass
        self.peretaskivanie = (self.mass / (self.mass + mass_of_air)) ** self.size

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)

    def move(self):
        self.x += math.sin(self.ygol) * self.speed
        self.y -= math.cos(self.ygol) * self.speed
        self.speed *= self.peretaskivanie

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.ygol = - self.ygol
            self.speed *= elasticity
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.ygol = - self.ygol
            self.speed *= elasticity
        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.ygol = math.pi - self.ygol
            self.speed *= elasticity
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.ygol = math.pi - self.ygol
            self.speed *= elasticity


running_menu = True
while running_menu:
    gg = main_menu.main_menu()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Simulation')
    print(gg[-1])
    print(gg[-2])
    mass_of_air = gg[-1] / 100
    elasticity = gg[-2] / 10
    number_of_particles = gg[0]
    my_particles = []

    for n in range(number_of_particles):
        size = gg[1][0][n]
        density = gg[1][1][n]
        x = random.randint(size, width - size)
        y = random.randint(size, height - size)

        particle = Particle(x, y, size, density * math.pi * size ** 2)
        particle.colour = (200 - density * 20, 200 - density * 20, 255)
        particle.speed = random.random()
        particle.ygol = random.uniform(0, math.pi * 2)

        my_particles.append(particle)

    selected_particle = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                selected_particle = findParticle(my_particles, mouseX, mouseY)
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_particle = None

        if selected_particle:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            dx = mouseX - selected_particle.x
            dy = mouseY - selected_particle.y
            selected_particle.ygol = 0.5 * math.pi + math.atan2(dy, dx)
            selected_particle.speed = math.hypot(dx, dy) * 0.1

        screen.fill(background_colour)

        for i, particle in enumerate(my_particles):
            particle.move()
            particle.bounce()
            for particle2 in my_particles[i + 1:]:
                collide(particle, particle2)
            particle.display()

        pygame.display.flip()
