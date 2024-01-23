import random
import pyglet
from pyglet import shapes
from pyglet.gl import *
from math import sin, cos, pi

window = pyglet.window.Window(800, 600, caption="Particle System")

particles = []
max_particles = 1000  # Set the maximum number of particles
particle_texture = pyglet.image.load("cestica.bmp").get_texture()
batch = pyglet.graphics.Batch()

# Define planes as obstacles
obstacles = [
    shapes.Line(100, 400, 200, 400, width=5, color=(255, 255, 255))
]


class Particle:
    def __init__(self):
        self.x = 200  # Initial x position for all particles
        self.y = 500  # Initial y position for all particles
        self.size = 20
        self.speed = 50
        self.angle = random.uniform(0, 2 * pi)  # Random angle for each particle
        self.lifespan = 500
        self.sprite = pyglet.sprite.Sprite(particle_texture,self.x,self.y,batch=batch)
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.scale = 0.2

    def update(self, dt):
        self.x += self.speed * cos(self.angle) * dt
        self.y += self.speed * sin(self.angle) * dt
        self.lifespan -= random.randint(0, 5)
        self.sprite.x=self.x
        self.sprite.y=self.y

        # Change color based on lifespan
        alpha = int((self.lifespan / 500) * 255)
        self.sprite.opacity=alpha

        # Change size based on lifespan
        scale_factor = max((self.lifespan / 500) * 0.2, 0.05)
        self.sprite.scale = scale_factor

        # Check for collision with obstacles
        for obstacle in obstacles:
            if (
                    self.x < max(obstacle.x, obstacle.x2)
                    and self.x + self.size > min(obstacle.x, obstacle.x2)
                    and self.y < max(obstacle.y, obstacle.y2)
                    and self.y + self.size > min(obstacle.y, obstacle.y2)
            ):
                self.angle += pi  # Reflect the particle


def update(dt):
    if len(particles) < max_particles:
        particle = Particle()
        particles.append(particle)

    for particle in particles:
        particle.update(dt)

    particles[:] = [particle for particle in particles if particle.lifespan > 0]

@window.event
def on_draw():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    window.clear()
    batch.draw()

    for obstacle in obstacles:
        obstacle.draw()


pyglet.clock.schedule_interval(update, 0.05)
pyglet.app.run()