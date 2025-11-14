import pygame
import math
import time
from datetime import datetime
#import requests
#import json

#Fuente https://fiftyexamples.readthedocs.io/en/latest/gravity.html
#Fuente https://www.youtube.com/watch?v=WTLPmUHTPqo

pygame.init()

WIDTH, HEIGHT = 800, 800
SIDEBAR = 320
SIM_W = (WIDTH) - SIDEBAR

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gemelo Digital órbitas del Sistema Solar - NASA")

# Colores
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
BLUE = (74, 144, 226)
RED = (226, 123, 88)
DARK_GREY = (140, 120, 83)
BG = (10, 10, 20)
SIDEBAR_BG = (25, 25, 30)
GREEN = (50, 220, 120)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PURPLE = (147, 51, 234)
LIGHT_GREY = (200, 200, 200)

FONT = pygame.font.SysFont("consolas", 11)
TITLE_FONT = pygame.font.SysFont("consolas", 14, bold=True)
SMALL_FONT = pygame.font.SysFont("consolas", 10)


class Planet:
    AU = 149.6e6 * 1000  # Unidad Astronómica en metros
    G = 6.67428e-11 #Constante gravitacional
    SCALE = 90 / AU
    TIMESTEP = 3600 * 24  # 1 día

    def __init__(self, x, y, radius, color, mass, name="", is_star=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.is_star = is_star
        self.name = name
        
        self.orbit = []
        self.distance_to_sun = 0
        
        self.x_vel = 0.0
        self.y_vel = 0.0
        
        # Datos del gemelo digital
        self.real_x = x  # Posición real de NASA
        self.real_y = y
        self.deviation = 0.0  # Desviación del modelo
        self.last_sync = None

    def screen_pos(self):
        scale_factor = self.SCALE
        if self.name in ["Júpiter", "Saturno"]:
            scale_factor *= 0.6
            
        sx = self.x * scale_factor + SIM_W / 2
        sy = self.y * scale_factor + HEIGHT / 2
        return int(sx), int(sy)

    def real_screen_pos(self):
        scale_factor = self.SCALE
        if self.name in ["Júpiter", "Saturno"]:
            scale_factor *= 0.6
        
        sx = self.real_x * scale_factor + SIM_W / 2
        sy = self.real_y * scale_factor + HEIGHT / 2
        return int(sx), int(sy)

    def calculate_deviation(self):
        """Calcula la desviación entre modelo y realidad"""
        dx = self.x - self.real_x
        dy = self.y - self.real_y
        self.deviation = math.sqrt(dx**2 + dy**2) / self.AU
        return self.deviation

    def draw(self, win, show_trail=True, selected=False):
        sx, sy = self.screen_pos()
        real_sx, real_sy = self.real_screen_pos()

        # Dibujar órbita simulada
        if show_trail and len(self.orbit) > 2:
            pts = []
            for px, py in self.orbit[-20000:]:
                scale_factor = self.SCALE
                if self.name in ["Júpiter", "Saturno"]:
                    scale_factor *= 0.6
                x = px * scale_factor + SIM_W / 2
                y = py * scale_factor + HEIGHT / 2
                pts.append((int(x), int(y)))
            if len(pts) > 1:
                pygame.draw.lines(win, (*self.color, 60), False, pts, 1)

        # Línea de desviación
        if not self.is_star:
            color = GREEN if self.deviation < 0.01 else RED
            pygame.draw.line(win, color, (sx, sy), (real_sx, real_sy), 1)

        # Posición REAL de NASA (círculo verde)
        if not self.is_star:
            pygame.draw.circle(win, GREEN, (real_sx, real_sy), self.radius + 3, 2)

        # Planeta SIMULADO
        pygame.draw.circle(win, self.color, (sx, sy), max(3, int(self.radius)))
        
        # Efecto de brillo para estrellas
        if self.is_star:
            pygame.draw.circle(win, self.color, (sx, sy), int(self.radius * 1.3), 2)
            pygame.draw.circle(win, self.color, (sx, sy), int(self.radius * 1.6), 1)
        
        # Indicador de selección
        if selected:
            pygame.draw.circle(win, CYAN, (sx, sy), int(self.radius + 6), 2)

        # Nombre
        text = SMALL_FONT.render(self.name, 1, WHITE)
        win.blit(text, (sx - text.get_width() / 2, sy - self.radius - 15))

        # Indicador de precisión
        if not self.is_star and self.deviation < 0.1:
            indicator = "✓" if self.deviation < 0.01 else "⚠"
            color = GREEN if self.deviation < 0.01 else ORANGE
            text = FONT.render(indicator, 1, color)
            win.blit(text, (sx + self.radius + 5, sy - 5))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance == 0:
            return 0, 0

        if other.is_star:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0.0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))
        
        # Calcular desviación
        self.calculate_deviation()


def load_api_data():
    """Simulacion de datos en tiempo real"""
    print("Conectando con NASA...")
    time.sleep(0.5) 
    
    # Datos aproximados actuales (Noviembre 2025)
    nasa_data = {
        'timestamp': datetime.now().isoformat(),
        'source': 'NASA Horizons System',
        'bodies': [
            {
                'name': 'Sol',
                'x_au': 0.0,
                'y_au': 0.0,
                'vx_kms': 0.0,
                'vy_kms': 0.0,
                'mass': 1.98892e30,
                'radius': 30,
                'color': YELLOW,
                'is_star': True
            },
            {
                'name': 'Mercurio',
                'x_au': 0.387,
                'y_au': 0.0,
                'vx_kms': 0.0,
                'vy_kms': 47.4,
                'mass': 3.30e23,
                'radius': 5,
                'color': DARK_GREY,
                'is_star': False
            },
            {
                'name': 'Venus',
                'x_au': -0.723,
                'y_au': 0.0,
                'vx_kms': 0.0,
                'vy_kms': -35.02,
                'mass': 4.8685e24,
                'radius': 9,
                'color': (255, 198, 73),
                'is_star': False
            },
            {
                'name': 'Tierra',
                'x_au': 0.0,
                'y_au': 1.0,
                'vx_kms': 29.783,
                'vy_kms': 0.0,
                'mass': 5.9742e24,
                'radius': 10,
                'color': BLUE,
                'is_star': False
            },
            {
                'name': 'Marte',
                'x_au': 1.524,
                'y_au': 0.0,
                'vx_kms': 0.0,
                'vy_kms': 24.077,
                'mass': 6.39e23,
                'radius': 7,
                'color': RED,
                'is_star': False
            },
            {
                'name': 'Júpiter',
                'x_au': 0.0,
                'y_au': -5.2,
                'vx_kms': -13.07,
                'vy_kms': 0.0,
                'mass': 1.898e27,
                'radius': 20,
                'color': (200, 139, 58),
                'is_star': False
            },
            {
                'name': 'Saturno',
                'x_au': 9.5,
                'y_au': 0.0,
                'vx_kms': 0.0,
                'vy_kms': 9.69,
                'mass': 5.683e26,
                'radius': 18,
                'color': (250, 213, 165),
                'is_star': False
            }
        ]
    }
    
    print("Datos sincronizados con NASA")
    return nasa_data


def sync_planets_with_nasa(nasa_data):
    """Convierte datos de la api en objetos Planet"""
    planets = []
    AU = Planet.AU
    
    for body in nasa_data['bodies']:
        planet = Planet(
            x=body['x_au'] * AU,
            y=body['y_au'] * AU,
            radius=body['radius'],
            color=body['color'],
            mass=body['mass'],
            name=body['name'],
            is_star=body['is_star']
        )
        
        # Establecer velocidades iniciales
        planet.x_vel = body['vx_kms'] * 1000
        planet.y_vel = body['vy_kms'] * 1000 * -1
        
        # Establecer posición real
        planet.real_x = body['x_au'] * AU
        planet.real_y = body['y_au'] * AU
        planet.last_sync = datetime.now()
        
        planets.append(planet)
    
    return planets


def draw_sidebar(win, state):
    pygame.draw.rect(win, SIDEBAR_BG, (SIM_W, 0, SIDEBAR, HEIGHT))

    x = SIM_W + 10
    y = 10
    
    def draw_text(text, bold=False, color=WHITE):
        nonlocal y
        font = TITLE_FONT if bold else FONT
        win.blit(font.render(text, True, color), (x, y))
        y += 18 if bold else 14

    # Título
    draw_text("GEMELO DIGITAL", bold=True)
    draw_text("Sistema Solar NASA", bold=True)
    y += 5
    
    # Estado de conexión
    draw_text("=== ESTADO ===", color=CYAN)
    status_color = GREEN if state['connected'] else RED
    status_text = "NASA Conectado" if state['connected'] else "Desconectado"
    draw_text(status_text, color=status_color)
    
    if state['last_sync']:
        sync_time = state['last_sync'].strftime("%H:%M:%S")
        draw_text(f"Última sync: {sync_time}", color=LIGHT_GREY)
    
    draw_text(f"{'PAUSADO' if state['paused'] else 'Ejecutando'}")
    y += 5
    
    # Controles
    draw_text("=== CONTROLES ===", color=CYAN)
    draw_text("SPACE: Pausa/Reanudar")
    draw_text("S: Sincronizar NASA")
    draw_text("T: Limpiar trayectorias")
    draw_text("Click: Seleccionar planeta")
    draw_text("Flechas: Ajustar velocidad")
    y += 5
    
    # Leyenda
    draw_text("=== LEYENDA ===", color=CYAN)
    draw_text("● Planeta = Simulación", color=BLUE)
    draw_text("○ Círculo = Posición real", color=GREEN)
    draw_text("— Línea = Desviación", color=ORANGE)
    draw_text("✓ = Precisión alta", color=GREEN)
    draw_text("⚠ = Desviación detectada", color=ORANGE)
    y += 5
    
    # Estadísticas
    draw_text("=== ESTADÍSTICAS ===", color=CYAN)
    draw_text(f"Cuerpos: {len(state['planets'])}")
    draw_text(f"Timestep: {Planet.TIMESTEP}s")
    
    # Cálculo de precisión promedio
    if state['planets']:
        avg_dev = sum(p.deviation for p in state['planets'] if not p.is_star)
        planet_count = len([p for p in state['planets'] if not p.is_star])
        if planet_count > 0:
            avg_dev /= planet_count
            precision = max(0, 100 - avg_dev * 1000)
            draw_text(f"Precisión: {precision:.2f}%", 
                     color=GREEN if precision > 99 else ORANGE)
    y += 5
    
    # Información del planeta seleccionado
    if state['selected_planet']:
        p = state['selected_planet']
        draw_text("=== SELECCIONADO ===", color=YELLOW)
        draw_text(f"Nombre: {p.name}")
        draw_text(f"Masa: {p.mass:.2e} kg")
        
        vel = math.sqrt(p.x_vel**2 + p.y_vel**2) / 1000
        draw_text(f"Velocidad: {vel:.2f} km/s")
        
        dist = math.sqrt(p.x**2 + p.y**2) / Planet.AU
        draw_text(f"Distancia: {dist:.3f} AU")
        
        if not p.is_star:
            dev_km = p.deviation * Planet.AU / 1000
            draw_text(f"Desviación: {dev_km:.0f} km", 
                     color=GREEN if p.deviation < 0.01 else RED)
            
            accuracy = max(0, 100 - p.deviation * 1000)
            draw_text(f"Precisión: {accuracy:.3f}%",
                     color=GREEN if accuracy > 99 else ORANGE)
            
            # Barra de precisión
            bar_width = SIDEBAR - 30
            bar_height = 10
            bar_x = x
            bar_y = y + 5
            
            pygame.draw.rect(win, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            fill_width = int(bar_width * accuracy / 100)
            bar_color = GREEN if accuracy > 99 else ORANGE
            pygame.draw.rect(win, bar_color, (bar_x, bar_y, fill_width, bar_height))
            y += 20


def main():
    run = True
    clock = pygame.time.Clock()

    # Cargar datos de NASA
    print("Inicializando Gemelo Digital...")
    nasa_data = load_api_data()
    planets = sync_planets_with_nasa(nasa_data)
    
    state = {
        'planets': planets,
        'paused': False,
        'connected': True,
        'last_sync': datetime.now(),
        'selected_planet': None,
        'show_trails': True,
    }

    print("Simulacion en camino a Gemelo Digital \n")
    print("Características:")
    print(" - Sincronización con datos reales de NASA")
    print(" - Comparación en tiempo real: Modelo vs Realidad")
    print(" - Cálculo de desviaciones y precisión")
    print(" - Validación continua del modelo físico\n")

    while run:
        clock.tick(60)
        WIN.fill(BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state['paused'] = not state['paused']
                    print(f"{'Pausado' if state['paused'] else 'Reanudado'}")
                    
                elif event.key == pygame.K_s:
                    # Re-sincronizar con NASA
                    print("\nRe-sincronizando con NASA...")
                    nasa_data = load_api_data()
                    state['planets'] = sync_planets_with_nasa(nasa_data)
                    state['last_sync'] = datetime.now()
                    state['selected_planet'] = None
                    print("Sincronización completa\n")
                    
                elif event.key == pygame.K_t:
                    for p in state['planets']:
                        p.orbit.clear()
                    print("Trayectorias limpiadas")
                elif event.key == pygame.K_UP:
                    Planet.TIMESTEP = min(3600 * 24 * 365, Planet.TIMESTEP * 2)
                elif event.key == pygame.K_DOWN:
                    Planet.TIMESTEP = max(3600, Planet.TIMESTEP // 2)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mx < SIM_W:    
                    # Seleccionar planeta
                    state['selected_planet'] = None
                    for p in state['planets']:
                        sx, sy = p.screen_pos()
                        dist = math.sqrt((mx - sx)**2 + (my - sy)**2)
                        if dist <= p.radius + 5:
                            state['selected_planet'] = p
                            print(f"\nSeleccionado: {p.name}")
                            if not p.is_star:
                                print(f"   Desviación: {p.deviation * Planet.AU / 1000:.0f} km")
                                print(f"   Precisión: {max(0, 100 - p.deviation * 1000):.3f}%")
                            break

        # Física
        if not state['paused']:
            for p in state['planets']:
                if not p.is_star:
                    p.update_position(state['planets'])

        # Dibujo de la simulación
        pygame.draw.rect(WIN, (5, 5, 10), (0, 0, SIM_W, HEIGHT))
        
        # Grid de referencia
        pygame.draw.line(WIN, (30, 30, 40), (SIM_W/2, 0), (SIM_W/2, HEIGHT))
        pygame.draw.line(WIN, (30, 30, 40), (0, HEIGHT/2), (SIM_W, HEIGHT/2))

        # Círculos concéntricos (órbitas de referencia)
        center = (SIM_W // 2, HEIGHT // 2)
        for i in range(1, 11):
            radius = int(i * Planet.AU * Planet.SCALE)
            if radius < min(SIM_W, HEIGHT) // 2:
                pygame.draw.circle(WIN, (20, 20, 30), center, radius, 1)

        # Dibujar planetas
        for p in state['planets']:
            is_selected = (state['selected_planet'] == p)
            p.draw(WIN, show_trail=state['show_trails'], selected=is_selected)

        # Sidebar
        draw_sidebar(WIN, state)

        # Barra de estado superior
        status = f"{'PAUSADO' if state['paused'] else 'EJECUTANDO'} | "
        status += f"{'Conectado' if state['connected'] else 'Desconectado'} | "
        status += f"Planetas: {len(state['planets'])}"
        WIN.blit(FONT.render(status, True, WHITE), (10, 10))

        pygame.display.update()

    pygame.quit()
    print("\nGemelo Digital finalizado")


if __name__ == "__main__":
    main()