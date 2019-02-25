import math
import pygame

def angle_project_point(angle,length):
    point = [0, 0]
    point[0] = int(math.sin(-math.radians(angle)) * length)
    point[1] = int(-math.cos(math.radians(angle)) * length)

    return point

class VectorArrow():
    def __init__(self):
        self.direction = [0, 1]
        self.length = 1
        self.angle = 0

    def draw_on(self, screen, position, offset=0):
        if self.length <= 1:
            return

        end_position = [0, 0]
        end_position[0] = position[0] + math.sin(-math.radians(self.angle))*(self.length+offset)
        end_position[1] = position[1] + -math.cos(math.radians(self.angle))*(self.length+offset)

        start_position = [0, 0]
        start_position[0] = position[0] + math.sin(-math.radians(self.angle)) * offset
        start_position[1] = position[1] + -math.cos(math.radians(self.angle)) * offset

        pygame.draw.line(screen, (255, 0, 0), start_position, end_position, 2)
        L = 10
        H = 5
        endX = end_position[0]
        endY = end_position[1]
        dX = end_position[0]-position[0]
        dY = end_position[1]-position[1]
        Len = math.sqrt(dX*dX + dY*dY)
        udX = dX/Len
        udY = dY/Len
        perpX = -udY
        perpY = udX
        leftX = endX - L*udX + H*perpX
        leftY = endY - L*udY + H*perpY
        rightX = endX - L * udX - H * perpX
        rightY = endY - L * udY - H * perpY

        pygame.draw.polygon(screen, (255, 0, 0), [end_position, [leftX, leftY], [rightX, rightY]], 2)

    def update_by_angle(self, angle, length):
        self.angle = angle
        self.length = length


class radar_sensor(object):
    def __init__(self, fov=45, range=300, orientation=0, color=(0, 255, 0)):
        self.fov = fov
        self.range = range
        self.orientation = orientation
        self.color = color

    def detect(self, position, heading, rocks):
        detected = list()
        for i, rock in enumerate(rocks):

            x = rock.position[0] - position[0]
            y = rock.position[1] - position[1]

            dist = math.hypot(x, y)

            bearing = 360 - math.degrees(math.atan2(x, -y))
            bearing = (bearing + 360) % 360

            if dist <= self.range:
                angle = 180 - abs(abs(bearing - (self.orientation + heading) % 360) - 180)
                if angle < self.fov/2:
                    detected.append([i, bearing, dist])

        return detected

    def draw_fov(self, screen, position, heading):

        lh_bound = angle_project_point(self.orientation + heading - self.fov / 2, self.range)
        rh_bound = angle_project_point(self.orientation + heading + self.fov / 2, self.range)
        pygame.draw.line(screen, (0, 50, 0), position, [position[0]+lh_bound[0], position[1]+lh_bound[1]])
        pygame.draw.line(screen, (0, 50, 0), position, [position[0]+rh_bound[0], position[1]+rh_bound[1]])


class sensor_set:
    def __init__(self):
        self.radars = list()
        self.detected = list()

    def append(self, new_sensor):
        if type(new_sensor) == radar_sensor:
            self.radars.append(new_sensor)

        else:
            pass

def perception(screen, spaceship, rocks):
    ship_arrow = VectorArrow()
    ship_arrow.update_by_angle(spaceship.angle, spaceship.speed * 6)
    ship_arrow.draw_on(screen, spaceship.position, 30)

    # for rock in rocks:
    #     bearing = point_bearing(spaceship.position, rock.position)
    #     pygame.draw.line(screen, (50, 100, 200), spaceship.position, rock.position, 1)
    #     # default_font = pygame.font.get_default_font()
    #     # font_renderer = pygame.font.Font(default_font, 12)
    #     # screen.blit(font_renderer.render(str("{:.1f}".format(bearing)),1,(255,255,255)), rock.position)

    for radar in spaceship.sensors.radars:
        radar.draw_fov(screen, spaceship.position, spaceship.angle)
        new_detected = radar.detect(spaceship.position, spaceship.angle, rocks)

        for obj in new_detected:
            detect_pos = angle_project_point(obj[1], obj[2])
            detect_pos[0] += spaceship.position[0]
            detect_pos[1] += spaceship.position[1]
            pygame.draw.circle(screen, radar.color, [int(i) for i in detect_pos], int(5))

    return

def point_bearing(pointA, pointB):
    x = pointB[0] - pointA[0]
    y = pointB[1] - pointA[1]
    bearing = 360 - math.degrees(math.atan2(x, -y))
    bearing = (bearing + 360) % 360

    return bearing