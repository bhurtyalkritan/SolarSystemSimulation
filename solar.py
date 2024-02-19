import pygame
import math

# Initializing Pygame
pygame.init()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

# Sun properties
sun_color = (255, 255, 0)  # Yellow
sun_radius = 30

# Planet colors
planet_colors = {
    "Mercury": (169, 169, 169),  # Grey
    "Venus": (205, 133, 63),    # Pale Yellow
    "Earth": (30, 144, 255),    # Blue
    "Mars": (188, 39, 50),      # Red
    "Jupiter": (204, 102, 0),   # Orange
    "Saturn": (224, 208, 176),  # Gold
    "Uranus": (72, 209, 204),   # Cyan
    "Neptune": (0, 0, 205)      # Dark Blue
}

# Simplified data for the planets
planets_data = [
    ("Mercury", 50, 88, 3, 0.205),
    ("Venus", 70, 224.7, 6, 0.007),
    ("Earth", 90, 365.25, 6, 0.017),
    ("Mars", 110, 687, 4, 0.093),
    ("Jupiter", 150, 4331, 12, 0.048),
    ("Saturn", 190, 10747, 10, 0.056),
    ("Uranus", 220, 30589, 8, 0.046),
    ("Neptune", 250, 59800, 8, 0.010)
]

def draw_planet(name, orbital_radius, day, orbital_period, radius, color, eccentricity):
    """Draws the planet and its orbit using an approximation."""
    angle = (day / orbital_period) * 2 * math.pi
    a = orbital_radius
    b = orbital_radius * math.sqrt(1 - eccentricity**2)

    x = width / 2 + a * math.cos(angle)
    y = height / 2 + b * math.sin(angle)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    distance = math.sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
    if distance < radius + 5:
        font = pygame.font.SysFont("Arial", 16)
        info_text = f"{name}: Day {day}, Period: {orbital_period} days"
        info_surface = font.render(info_text, True, (255, 255, 255))
        screen.blit(info_surface, (mouse_x + 10, mouse_y + 10))

    eclipse_factor = 0.5 + 0.5 * math.cos(angle)
    eclipse_color = darken_color(color, eclipse_factor)

    pygame.draw.circle(screen, eclipse_color, (int(x), int(y)), radius)

    font = pygame.font.SysFont("Arial", 16)
    name_surface = font.render(name, True, (255, 255, 255))
    screen.blit(name_surface, (int(x) - radius, int(y) - radius - 20))


def draw_orbits():
    """Draws orbital paths for each planet."""
    for name, orbital_radius, orbital_period, radius, eccentricity in planets_data:
        a = orbital_radius
        b = orbital_radius * math.sqrt(1 - eccentricity**2)
        ellipse_rect = pygame.Rect(width / 2 - a, height / 2 - b, 2 * a, 2 * b)
        pygame.draw.ellipse(screen, (255, 255, 255), ellipse_rect, 1)

def darken_color(color, factor):
    """Function to darken the color for eclipses."""
    return max(0, int(color[0] * factor)), max(0, int(color[1] * factor)), max(0, int(color[2] * factor))


running = True
paused = False
simulation_day = 0
simulation_speed = 1  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    if not paused:
        screen.fill((0, 0, 0))  # Black background

        # Draws the sun in the center
        pygame.draw.circle(screen, sun_color, (width // 2, height // 2), sun_radius)

        # Draws orbital paths
        draw_orbits()

        # Draws planets
        for planet in planets_data:
            draw_planet(planet[0], planet[1], simulation_day, planet[2], planet[3], planet_colors[planet[0]], planet[4])

        # Updates day marker
        font = pygame.font.SysFont("Arial", 24)
        day_surface = font.render(f"Day: {int(simulation_day)}", True, (255, 255, 255))
        screen.blit(day_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

        # Increments day
        simulation_day += simulation_speed
    else:
        # Allows screen to update
        pygame.display.flip()
        clock.tick(60)  

pygame.quit()
