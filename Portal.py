# This is Richard's final project
'''
The game that I will create is called 'Portal'. The player will use 'a''d'
to move the hero horizontally and use 'w' or 'space' to jump in the game.
The hero has a portal gun and the player will use mouse to control the direction of
the portal gun and right click to shoot the portals. The player can have two portals
on the map at same time.


The goal of the game is reaching the destination on the map by creating portals and using
the change of gravity.

The game pitch sheet can be found here:
https://www.dropbox.com/s/3xa1zt5cy2adtvy/RICHARD%20GAME%20PITCH%20SHEET%204.jpg?dl=0
Black square is wall. Red square is hero






'''
import simplegui
import math

gravity = 0.1
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
CELL_SIZE = 10
GRID_HEIGHT = CANVAS_HEIGHT // CELL_SIZE
GRID_WIDTH = CANVAS_WIDTH // CELL_SIZE
EMPTY = 0
FULL = 1
wall_list = []
bullet_list = []
vel_horizontal = 2
vel_jump = 5
CHARACTER_SIZE = 16
PORTAL_SHORT = 2
PORTAL_LONG = 20
BULLET_VEL = 10
BULLET_LENGTH = 5
blue_portal_list = []
orange_portal_list = []
color = 'blue'
color_1 = 'orange'
start_game = False
menu = True
toturial = False
win = False
BUTTON_LONG = 20
BUTTON_SHORT = 2
weight_list = []
soft_wall_list = []
image_list = []
button_list = []
gate_list = []
map_list = []
map_indicator = 0
draw_map = False
main_menu_buttons = []
level_select_buttons = []
current_menu = None
level_menu = False


class grid:
    """
    Implementation of 2D grid of cells
    Includes boundary handling
    """

    def __init__(self, grid_height, grid_width):
        """
        Initializes grid to be empty, take height and width of grid as parameters
        Indexed by rows (left to right), then by columns (top to bottom)
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]

    def __str__(self):
        """
        Return multi-line string represenation for grid
        """
        ans = ""
        for row in range(self._grid_height):
            ans += str(self._cells[row])
            ans += "\n"
        return ans

    def get_grid_height(self):
        """
        Return the height of the grid for use in the GUI
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Return the width of the grid for use in the GUI
        """
        return self._grid_width

    def clear(self):
        """
        Clears grid to be empty
        """
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]

    def set_empty(self, row, col):
        """
        Set cell with index (row, col) to be empty
        """
        self._cells[row][col] = EMPTY

    #    def set_blue_portal(self,row,col):
    #        self._cells[row][col] = 2
    #
    #    def set_orange_portal(self,row,col):
    #        self._cells[row][col] = 3

    def set_full(self, row, col):
        """
        Set cell with index (row, col) to be full
        """
        self._cells[row][col] = FULL

    def set_soft(self, row, col):
        """
        Set cell to the wall that can open portal
        """
        self._cells[row][col] = 2

    def is_full(self, row, col):
        """
        Checks whether cell with index (row, col) is empty
        """
        return (self._cells[row][col] == FULL or self._cells[row][col] == 2)

    def is_soft(self, row, col):
        return self._cells[row][col] == 2

    def four_neighbors(self, row, col):
        """
        Returns horiz/vert neighbors of cell (row, col)
        """
        ans = []
        if row > 0:
            ans.append((row - 1, col))
        if row < self._grid_height - 1:
            ans.append((row + 1, col))
        if col > 0:
            ans.append((row, col - 1))
        if col < self._grid_width - 1:
            ans.append((row, col + 1))
        return ans

    def eight_neighbors(self, row, col):
        """
        Returns horiz/vert neighbors of cell (row, col) as well as
        diagonal neighbors
        """
        ans = []
        if row > 0:
            ans.append((row - 1, col))
        if row < self._grid_height - 1:
            ans.append((row + 1, col))
        if col > 0:
            ans.append((row, col - 1))
        if col < self._grid_width - 1:
            ans.append((row, col + 1))
        if (row > 0) and (col > 0):
            ans.append((row - 1, col - 1))
        if (row > 0) and (col < self._grid_width - 1):
            ans.append((row - 1, col + 1))
        if (row < self._grid_height - 1) and (col > 0):
            ans.append((row + 1, col - 1))
        if (row < self._grid_height - 1) and (col < self._grid_width - 1):
            ans.append((row + 1, col + 1))
        return ans

    def get_index(self, point, cell_size):
        """
        Takes point in screen coordinates and returns index of
        containing cell
        """
        return (point[1] / cell_size, point[0] / cell_size)


class image_info:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


class moving_objects:
    def __init__(self, pos, vel, jump, size, CELL_SIZE, image, image_info, image_2, image_info_2):
        self.index = [pos[0] // CELL_SIZE, pos[1] // CELL_SIZE]
        self.pos = pos
        self.vel = vel
        self.jump = 0
        self.next_jump = 0
        self.size = size
        self.next_pos = [pos[0], pos[1]]
        self.next_index = [self.next_pos[0] // CELL_SIZE, self.next_pos[1] // CELL_SIZE]
        self.on_the_ground = False
        self.right_top = [pos[0] + self.size, pos[1]]
        self.right_bottom = [pos[0] + self.size, pos[1] + self.size]
        self.left_bottom = [pos[0], pos[1] + self.size]
        self.center = [pos[0] + self.size / 2, pos[1] + self.size / 2]
        self.moving_list = [False, False]  # First one is left, second one is right
        self.image = image
        self.info = image_info
        self.image_left = image_2
        self.info_left = image_info_2
        self.lifespan = 0

    def future_update_horizontally(self):
        self.next_pos[0] += self.vel

    def future_update_vertically(self):
        global gravity
        self.next_pos[1] += self.jump
        self.next_jump += gravity

    def update_horizontally(self):
        self.pos[0] += self.vel
        self.right_top[0] += self.vel
        self.right_bottom[0] += self.vel
        self.left_bottom[0] += self.vel
        self.center[0] += self.vel

    def update_vertically(self):
        global gravity
        self.pos[1] += self.jump
        self.right_top[1] += self.jump
        self.right_bottom[1] += self.jump
        self.left_bottom[1] += self.jump
        self.center[1] += self.jump
        self.jump += gravity
        self.on_the_ground = False

    #        print 1, self.on_the_ground

    def get_index(self):
        self.index = [self.pos[0] // CELL_SIZE, self.pos[1] // CELL_SIZE]
        return self.index

    def get_next_index(self):
        self.next_index = [self.next_pos[0] // CELL_SIZE, self.next_pos[1] // CELL_SIZE]
        return self.next_index

    def get_index_2(self):
        return [(self.pos[0] + self.size) // CELL_SIZE, (self.pos[1] + self.size) // CELL_SIZE]

    def get_next_index_2(self):
        return [(self.next_pos[0] + self.size) // CELL_SIZE, (self.next_pos[1] + self.size) // CELL_SIZE]

    def draw(self, canvas):
        #        canvas.draw_polygon([[self.pos[0],self.pos[1]],[self.pos[0]+self.size,self.pos[1]],[self.pos[0]+self.size,self.pos[1]+self.size],
        #                            [self.pos[0],self.pos[1]+self.size]],1,"Red","Red")
        if self.moving_list[0] == False and self.moving_list[1] == True:
            self.lifespan += 1
            canvas.draw_image(self.image,
                              [self.info.get_center()[0] + 50 * (self.lifespan % 5), self.info.get_center()[1]],
                              self.info.get_size(), self.center, [16, 16])
            if self.lifespan == 10:
                self.lifespan = 0
        if self.moving_list[0] == True and self.moving_list[1] == False:
            self.lifespan += 1
            canvas.draw_image(self.image_left, [self.info_left.get_center()[0] - 50 * (self.lifespan % 5),
                                                self.info_left.get_center()[1]], self.info_left.get_size(), self.center,
                              [16, 16])
            if self.lifespan == 10:
                self.lifespan = 0
        else:
            canvas.draw_image(self.image, self.info.get_center(), self.info.get_size(), self.center, [16, 16])

    def get_next_index_left_bottom(self):
        return [self.next_pos[0] // CELL_SIZE, (self.next_pos[1] + self.size) // CELL_SIZE]

    def get_index_left_bottom(self):
        return [self.pos[0] // CELL_SIZE, (self.pos[1] + self.size) // CELL_SIZE]

    def get_index_right_top(self):
        return [(self.pos[0] + self.size) // CELL_SIZE, self.pos[1] // CELL_SIZE]

    def get_next_index_right_top(self):
        return [(self.next_pos[0] + self.size) // CELL_SIZE, self.next_pos[1] // CELL_SIZE]

    #    def is_on_the_ground(self):
    #        global whole_map
    #        for cell in range(self.get_index_left_bottom()[0],self.get_index_2()[0]+1):
    #            if whole_map.is_full(cell,self.get_index_left_bottom()[1])==False:
    #                return False
    def update_every_point(self, point0, point1):
        self.pos[0] = point0
        self.pos[1] = point1
        self.right_top = [self.pos[0] + self.size, self.pos[1]]
        self.right_bottom = [self.pos[0] + self.size, self.pos[1] + self.size]
        self.left_bottom = [self.pos[0], self.pos[1] + self.size]
        self.center = [self.pos[0] + self.size / 2, self.pos[1] + self.size / 2]
        self.next_pos[0] = point0
        self.next_pos[1] = point1

    def is_on_the_ground(self):
        global whole_map
        index = [self.center[0] // CELL_SIZE, (self.center[1] + float(self.size / 2) + 1) // CELL_SIZE]
        #        print self.center
        return whole_map.is_full(index[0], index[1])

    def pick(self):
        global weight_list
        for weight in weight_list:
            if detect_collide(weight, self):
                if weight.pick == False:
                    weight.pick = True
                    return None
                else:
                    weight.pick = False

    def update(self):
        global whole_map, blue_portal_list, orange_portal_list, vel_horizontal, CANVAS_WIDTH
        self.future_update_horizontally()
        if process_collide(self, whole_map, self.size) == False:
            self.update_horizontally()
        else:
            process_collide(self, whole_map, self.size)
        self.future_update_vertically()
        if process_collide(self, whole_map, self.size) == False:
            if self.on_the_ground == False:
                self.update_vertically()
        #            self.on_the_ground = False
        else:
            process_collide(self, whole_map, self.size)
        if blue_portal_list[0].pos[0] < CANVAS_WIDTH and orange_portal_list[0].pos[0] < CANVAS_WIDTH:
            if blue_portal_list[0].check_collide(self):
                orange_portal_list[0].bounce(self)
            if orange_portal_list[0].check_collide(self):
                blue_portal_list[0].bounce(self)

        self.on_the_ground = self.is_on_the_ground()
        if self.on_the_ground:
            self.jump = 0
            if True in self.moving_list:
                if self.vel > vel_horizontal:
                    self.vel = vel_horizontal
                if self.vel < -vel_horizontal:
                    self.vel = -vel_horizontal
            else:
                if self.vel != 0:
                    self.vel = 0


class wall:
    def __init__(self, index, image, info):
        self.index = index
        self.image = image
        self.info = info

    def draw(self, canvas):
        global CELL_SIZE
        index = list(self.index)
        canvas.draw_image(self.image, self.info.get_center(), self.info.get_size(),
                          [(self.index[0] + 0.5) * CELL_SIZE, (self.index[1] + 0.5) * CELL_SIZE],
                          [CELL_SIZE, CELL_SIZE])
        # print [index[0]*CELL_SIZE,index[1]*CELL_SIZE],[(index[0]+1)*CELL_SIZE,index[1]*CELL_SIZE]


class soft_wall:
    def __init__(self, index, image, info):
        self.index = index
        self.image = image
        self.info = info

    def draw(self, canvas):
        global CELL_SIZE
        index = list(self.index)
        canvas.draw_image(self.image, self.info.get_center(), self.info.get_size(),
                          [(self.index[0] + 0.5) * CELL_SIZE, (self.index[1] + 0.5) * CELL_SIZE],
                          [CELL_SIZE, CELL_SIZE])


class portal:
    def __init__(self, pos, color, width, height, direction):
        self.pos = pos
        self.right_top = [pos[0] + width, pos[1]]
        self.left_bottom = [pos[0], pos[1] + height]
        self.right_bottom = [pos[0] + width, pos[1] + height]
        self.direction = direction
        self.color = color
        self.width = width
        self.height = height
        self.index = [pos[0] // CELL_SIZE, pos[1] // CELL_SIZE]
        self.center = [pos[0] + self.width / 2, pos[1] + self.height / 2]

    def detect_direction(self, whole_map):
        environment = whole_map.four_neighbors(self.index[0], self.index[1])
        walls = []
        for cell in environment:
            walls.append(whole_map.is_full(list(cell)[0], list(cell)[1]))
        if walls == [True, False, True, True]:
            self.direction = 'right'
        if walls == [False, True, True, True]:
            self.direction = 'left'
        if walls == [True, True, False, True]:
            self.direction = 'up'
        if walls == [True, True, True, False]:
            self.direction = 'down'

    def bounce(self, moving_object):
        global blue_portal_list, orange_portal_list
        if self.direction == 'right':
            moving_object.update_every_point(self.pos[0] + self.width + 1, self.pos[1])
            if self.color == 'blue' and (
                    orange_portal_list[0].direction != 'left' and orange_portal_list[0].direction != 'right'):
                moving_object.vel += math.fabs(moving_object.jump)
            if self.color == 'orange' and (
                    blue_portal_list[0].direction != 'left' and blue_portal_list[0].direction != 'right'):
                moving_object.vel += math.fabs(moving_object.jump)
        if self.direction == 'left':
            moving_object.update_every_point(self.pos[0] - moving_object.size - 1, self.pos[1])
            if self.color == 'blue' and (
                    orange_portal_list[0].direction != 'left' and orange_portal_list[0].direction != 'right'):
                moving_object.vel -= math.fabs(moving_object.jump)
            if self.color == 'orange' and (
                    blue_portal_list[0].direction != 'left' and blue_portal_list[0].direction != 'right'):
                moving_object.vel -= math.fabs(moving_object.jump)
        #            print moving_object.center,moving_object.pos
        if self.direction == 'up':
            moving_object.update_every_point(self.pos[0], self.pos[1] - moving_object.size - 1)
            moving_object.jump = -moving_object.jump
        if self.direction == 'down':
            moving_object.update_every_point(self.pos[0], self.pos[1] + self.height + 1)

    #
    def draw(self, canvas):
        canvas.draw_polygon([self.pos, self.right_top, self.right_bottom, self.left_bottom], 1, self.color, self.color)

    def check_collide(self, moving_object):
        if self.direction == 'right' or self.direction == 'left':
            ##            print moving_object.center, moving_object.pos
            if -(self.width + moving_object.size) / 2 <= (self.center[0] - moving_object.center[0]) and (
                    self.center[0] - moving_object.center[0]) <= (self.width + moving_object.size) / 2:
                return self.pos[1] <= moving_object.pos[1] and self.left_bottom[1] >= moving_object.pos[1]
        if self.direction == 'up' or self.direction == 'down':
            #            print (self.center[1]-moving_object.center[1]),(self.height+moving_object.size)/2
            #            print moving_object.pos[1],(self.height+moving_object.size)/2
            if -(self.height + moving_object.size) / 2 <= (self.center[1] - moving_object.center[1]) and (
                    self.center[1] - moving_object.center[1]) <= (self.height + moving_object.size) / 2:
                return self.pos[0] <= moving_object.pos[0] and self.right_bottom[0] >= moving_object.pos[0]
        else:
            return False


class bullet:
    def __init__(self, color, vel, length, my_man, click_pos):
        self.pos = [my_man.center[0], my_man.center[1]]
        self.click_pos = click_pos
        self.color = color
        self.vel = vel
        self.angle = math.atan((click_pos[1] - self.pos[1]) / (click_pos[0] - self.pos[0] + 0.00001))
        self.end_point = [self.pos[0] - math.cos(self.angle) * length, self.pos[1] - math.sin(self.angle) * length]
        self.direction = 'left'
        self.previous_pos = [my_man.center[0], my_man.center[1]]
        self.previous_end_point = [self.pos[0] - math.cos(self.angle) * length,
                                   self.pos[1] - math.sin(self.angle) * length]
        if click_pos[0] >= self.pos[0]:
            self.direction = 'right'

    def update_previous_pos(self):
        if self.direction == 'right':
            self.previous_pos[0] += math.cos(self.angle) * self.vel
            self.previous_pos[1] += math.sin(self.angle) * self.vel
            self.previous_end_point[0] += math.cos(self.angle) * self.vel
            self.previous_end_point[1] += math.sin(self.angle) * self.vel
        else:
            self.previous_pos[0] -= math.cos(self.angle) * self.vel
            self.previous_pos[1] -= math.sin(self.angle) * self.vel
            self.previous_end_point[0] -= math.cos(self.angle) * self.vel
            self.previous_end_point[1] -= math.sin(self.angle) * self.vel

    def update_pos(self):
        global bullet_list, whole_map
        if self.direction == 'right':
            self.pos[0] += math.cos(self.angle) * self.vel
            self.pos[1] += math.sin(self.angle) * self.vel
            self.end_point[0] += math.cos(self.angle) * self.vel
            self.end_point[1] += math.sin(self.angle) * self.vel
        else:
            self.pos[0] -= math.cos(self.angle) * self.vel
            self.pos[1] -= math.sin(self.angle) * self.vel
            self.end_point[0] -= math.cos(self.angle) * self.vel
            self.end_point[1] -= math.sin(self.angle) * self.vel
        if self.check_collide():
            self.go_back()
            #            print self.check_direction()
            if whole_map.is_soft(self.get_index()[0], self.get_index()[1]):
                self.open_portal()
            bullet_list.remove(self)

    def open_portal(self):
        direction = self.check_direction()
        index = self.get_index()
        color = self.color
        if color == 'blue':
            if direction == 'right':
                blue_portal_list.append(
                    portal([(index[0] + 1) * CELL_SIZE, index[1] * CELL_SIZE], 'blue', PORTAL_SHORT, PORTAL_LONG,
                           'right'))
            if direction == 'left':
                blue_portal_list.append(
                    portal([index[0] * CELL_SIZE - PORTAL_SHORT, index[1] * CELL_SIZE], 'blue', PORTAL_SHORT,
                           PORTAL_LONG, 'left'))
            if direction == 'top':
                blue_portal_list.append(
                    portal([index[0] * CELL_SIZE, index[1] * CELL_SIZE - PORTAL_SHORT], 'blue', PORTAL_LONG,
                           PORTAL_SHORT, 'up'))
            if direction == 'bottom':
                blue_portal_list.append(
                    portal([index[0] * CELL_SIZE, (index[1] + 1) * CELL_SIZE], 'blue', PORTAL_LONG, PORTAL_SHORT,
                           'down'))
            blue_portal_list.pop(0)
        if color == 'orange':
            if direction == 'right':
                orange_portal_list.append(
                    portal([(index[0] + 1) * CELL_SIZE, index[1] * CELL_SIZE], 'orange', PORTAL_SHORT, PORTAL_LONG,
                           'right'))
            if direction == 'left':
                orange_portal_list.append(
                    portal([index[0] * CELL_SIZE - PORTAL_SHORT, index[1] * CELL_SIZE], 'orange', PORTAL_SHORT,
                           PORTAL_LONG, 'left'))
            if direction == 'top':
                orange_portal_list.append(
                    portal([index[0] * CELL_SIZE, index[1] * CELL_SIZE - PORTAL_SHORT], 'orange', PORTAL_LONG,
                           PORTAL_SHORT, 'up'))
            if direction == 'bottom':
                orange_portal_list.append(
                    portal([index[0] * CELL_SIZE, (index[1] + 1) * CELL_SIZE], 'orange', PORTAL_LONG, PORTAL_SHORT,
                           'down'))
            orange_portal_list.pop(0)

    def update(self):
        self.update_pos()
        self.update_previous_pos()

    #        print self.check_collide()
    #        print self.line_equation()

    def check_collide(self):
        global whole_map
        return whole_map.is_full(self.pos[0] // CELL_SIZE, self.pos[1] // CELL_SIZE)

    def go_back(self):
        global whole_map
        if self.direction == 'right':
            while whole_map.is_full(self.get_index()[0], self.get_index()[1]):
                self.pos[0] -= math.cos(self.angle) * 0.01
                self.pos[1] -= math.sin(self.angle) * 0.01
            self.pos[0] += math.cos(self.angle) * 0.01
            self.pos[1] += math.sin(self.angle) * 0.01
        if self.direction == 'left':
            while whole_map.is_full(self.get_index()[0], self.get_index()[1]):
                self.pos[0] += math.cos(self.angle) * 0.01
                self.pos[1] += math.sin(self.angle) * 0.01
            self.pos[0] -= math.cos(self.angle) * 0.01
            self.pos[1] -= math.sin(self.angle) * 0.01

    def get_index(self):
        cell_index = [self.pos[0] // CELL_SIZE, self.pos[1] // CELL_SIZE]
        return cell_index

    def line_equation(self):
        gradient = (self.click_pos[1] - self.pos[1]) / (self.click_pos[0] - self.pos[0] + 0.00001)
        constant = self.pos[1] - gradient * self.pos[0]
        index = self.get_index()
        left_point = [index[0] * CELL_SIZE, index[0] * CELL_SIZE * gradient + constant]
        top_point = [(index[1] * CELL_SIZE - constant) / (gradient + 0.000000001), index[1] * CELL_SIZE]
        right_point = [(index[0] + 1) * CELL_SIZE, (index[0] + 1) * CELL_SIZE * gradient + constant]
        bottom_point = [((index[1] + 1) * CELL_SIZE - constant) / (gradient + 0.000000001), (index[1] + 1) * CELL_SIZE]
        points = [left_point, top_point, right_point, bottom_point]
        return points

    #        if left_point[1]>index[1]*CELL_SIZE and left_point[1]<(index[1]+1)*CELL_SIZE:
    #            return 'left'
    def check_direction(self):
        points = self.line_equation()
        left_point = points[0]
        top_point = points[1]
        right_point = points[2]
        bottom_point = points[3]
        index = self.get_index()
        if self.direction == 'right' and math.sin(self.angle) * self.vel < 0:
            if left_point[1] > index[1] * CELL_SIZE and left_point[1] < (index[1] + 1) * CELL_SIZE:
                return 'left'
            else:
                return 'bottom'
        if self.direction == 'right' and math.sin(self.angle) * self.vel > 0:
            if left_point[1] > index[1] * CELL_SIZE + 1 and left_point[1] < (index[1] + 1) * CELL_SIZE - 1:
                return 'left'
            else:
                return 'top'
        if self.direction == 'left' and math.sin(self.angle) * self.vel > 0:
            if right_point[1] > index[1] * CELL_SIZE and right_point[1] < (index[1] + 1) * CELL_SIZE:
                return 'right'
            else:
                return 'bottom'
        if self.direction == 'left' and math.sin(self.angle) * self.vel < 0:
            if right_point[1] > index[1] * CELL_SIZE and right_point[1] < (index[1] + 1) * CELL_SIZE:
                return 'right'
            else:
                return 'top'

    def draw(self, canvas):
        canvas.draw_line(self.pos, self.end_point, 3, self.color)


class button:
    def __init__(self, index, length, height, gate_list):
        global CELL_SIZE
        self.pos = [index[0] * CELL_SIZE, index[1] * CELL_SIZE - height]
        self.gate = gate_list
        self.center = [self.pos[0] + length / 2, self.pos[1] + height / 2]
        self.collide = False
        self.collide_list = []
        self.length = length
        self.height = height

    def check_collide(self):
        self.collide_list = []
        global my_man, weight_list
        for weight in weight_list:
            self.collide_list.append(detect_collide(self, weight))
        self.collide_list.append(detect_collide(self, my_man))
        self.collide = (True in self.collide_list)

    def draw(self, canvas):
        canvas.draw_polygon(
            [self.pos, [self.pos[0] + self.length, self.pos[1]], [self.pos[0] + self.length, self.pos[1] + self.height],
             [self.pos[0], self.pos[1] + self.height]], 1, 'green', 'green')

    def update(self):
        self.check_collide()
        if self.collide == True:
            for gate in self.gate:
                gate.trigger = True
        if self.collide == False:
            for gate in self.gate:
                gate.trigger = False


class gate:
    def __init__(self, index):
        self.pos = [index[0] * CELL_SIZE, index[1] * CELL_SIZE]
        self.trigger = False
        self.index = index

    def update(self):
        global whole_map
        if self.trigger == False:
            whole_map.set_full(self.index[0], self.index[1])
        if self.trigger == True:
            whole_map.set_empty(self.index[0], self.index[1])

    def draw(self, canvas):
        if self.trigger == False:
            canvas.draw_polygon(
                [self.pos, [self.pos[0] + CELL_SIZE, self.pos[1]], [self.pos[0] + CELL_SIZE, self.pos[1] + CELL_SIZE],
                 [self.pos[0], self.pos[1] + CELL_SIZE]], 1, 'yellow', 'yellow')


class weight(moving_objects):
    def __init__(self, pos, size):
        moving_objects.__init__(self, pos, 0, 0, float(size / 2), size, None, None, None, None)
        self.pick = False
        self.height = size
        self.length = size

    def update(self):
        global my_man
        if self.pick == True:
            self.update_every_point(my_man.center[0] - self.size / 2, my_man.center[1] - self.size / 2)
        else:
            #            self.on_the_ground = self.is_on_the_ground()
            #            print self.center
            moving_objects.update(self)

    def draw(self, canvas):
        canvas.draw_polygon([[self.pos[0], self.pos[1]], [self.pos[0] + self.size, self.pos[1]],
                             [self.pos[0] + self.size, self.pos[1] + self.size],
                             [self.pos[0], self.pos[1] + self.size]], 1, "white", "white")


class exits:
    def __init__(self, index, size, image=None, info=None):
        global CELL_SIZE
        self.index = index
        self.size = size
        self.length = size
        self.height = size
        self.pos = [index[0] * CELL_SIZE, index[1] * CELL_SIZE]
        self.center = [index[0] * CELL_SIZE + size / 2, index[1] * CELL_SIZE + size / 2]
        self.image = None
        self.info = None

    def draw(self, canvas):
        canvas.draw_polygon(
            [self.pos, [self.pos[0] + self.size, self.pos[1]], [self.pos[0] + self.size, self.pos[1] + self.size],
             [self.pos[0], self.pos[1] + self.size]], 1, 'purple', 'purple')


class maps:
    def __init__(self, function):
        self.display = False
        self.function = function

    def create_everything(self):
        self.function


class level_button:
    def __init__(self, pos, number):
        self.pos = pos
        self.width = 70
        self.height = 20
        self.number = number

    def do_something(self):
        global map_indicator, level_menu, start_game, draw_map
        map_indicator = self.number
        draw_map = True
        start_game = True
        level_menu = False

    def draw(self, canvas):
        canvas.draw_polygon(
            [self.pos, [self.pos[0] + self.width, self.pos[1]], [self.pos[0] + self.width, self.pos[1] + self.height],
             [self.pos[0], self.pos[1] + self.height]], 1, 'green', 'green')
        canvas.draw_text('Level ' + str(self.number), [self.pos[0], self.pos[1] + 20], 20, 'white')


def create_wall(start_point, width, height):
    global wall_list, whole_map
    for col in range(height):
        for row in range(width):
            wall_list.append(wall([start_point[0] + row, start_point[1] + col], wall_image, wall_info))
            whole_map.set_full(start_point[0] + row, start_point[1] + col)


def create_soft_wall(start_point, width, height):
    global wall_list, whole_map
    for col in range(height):
        for row in range(width):
            soft_wall_list.append(soft_wall([start_point[0] + row, start_point[1] + col], soft_image, soft_info))
            whole_map.set_soft(start_point[0] + row, start_point[1] + col)


# def create_portal(index,portal):
#    global whole_map
#    previous_index = portal.index
#    whole_map.set_full(previous_index[0],previous_index[1])
#    if portal.color == 'blue':
#        whole_map.set_portal(index[0],index[1])
#    portal.index = index
#

def detect_collide(square, moving_object):
    if math.fabs(square.center[1] - moving_object.center[1]) <= ((square.height + moving_object.size) / 2):
        return square.pos[0] <= moving_object.center[0] and moving_object.center[0] <= (square.pos[0] + square.length)
    else:
        return False


def process_collide(moving_object, whole_map, size):
    global vel_horizontal, CELL_SIZE
    position = moving_object.get_index()
    next_position = moving_object.get_next_index()
    position_1 = moving_object.get_index_2()
    next_position_1 = moving_object.get_next_index_2()
    position_right_top = moving_object.get_index_right_top()
    position_left_bottom = moving_object.get_index_left_bottom()
    next_position_right_top = moving_object.get_next_index_right_top()
    next_position_left_bottom = moving_object.get_next_index_left_bottom()
    a = 1
    #    print position_1,next_position_1
    cells = []
    index = 0
    if next_position[0] < position[0]:
        for row in range(int(position[0]), int(next_position[0] - 1), -1):
            for column in range(int(position[1]), int(position_left_bottom[1] + 1)):
                if whole_map.is_full(row, column):
                    moving_object.pos[0] = CELL_SIZE * (row + 1)
                    moving_object.next_pos[0] = CELL_SIZE * (row + 1)
                    moving_object.center[0] = moving_object.pos[0] + moving_object.size / 2
                    return None

    if next_position_1[0] > position_1[0]:
        for row in range(int(position_right_top[0]), int(next_position_right_top[0] + 1)):
            for column in range(int(position_right_top[1]), int(position_1[1] + 1)):
                if whole_map.is_full(row, column):
                    moving_object.pos[0] = CELL_SIZE * row - size - 1
                    moving_object.next_pos[0] = CELL_SIZE * row - size - 1
                    moving_object.center[0] = moving_object.pos[0] + moving_object.size / 2
                    return None

    if next_position[1] < position[1]:
        for row in range(int(position[0]), int(position_right_top[0] + 1)):
            for column in range(int(position[1]), int(next_position[1] - 1), -1):
                if whole_map.is_full(row, column):
                    moving_object.pos[1] = CELL_SIZE * (column + 1)
                    moving_object.next_pos[1] = CELL_SIZE * (column + 1)
                    moving_object.jump = 0
                    moving_object.center[1] = moving_object.pos[1] + moving_object.size / 2
                    return None

    if next_position_1[1] > position_1[1]:
        for row in range(int(position_left_bottom[0]), int(position_1[0] + 1)):
            for column in range(int(position_left_bottom[1]), int(next_position_left_bottom[1] + 1)):
                if whole_map.is_full(row, column):
                    moving_object.pos[1] = CELL_SIZE * column - size - 1
                    moving_object.next_pos[1] = CELL_SIZE * column - size - 1
                    moving_object.on_the_ground = True
                    moving_object.center[1] = moving_object.pos[1] + moving_object.size / 2
                    return None
    return False


# def draw_main_menu(canvas):


def keydown(key):
    global vel_horizontal, color
    if key == simplegui.KEY_MAP['a']:
        my_man.vel -= vel_horizontal
        my_man.moving_list[0] = True
    elif key == simplegui.KEY_MAP['d']:
        my_man.vel += vel_horizontal
        my_man.moving_list[1] = True
    elif key == simplegui.KEY_MAP['space']:
        #        print my_man.on_the_ground
        if my_man.on_the_ground:
            my_man.on_the_ground = False
            my_man.jump = -2
    elif key == simplegui.KEY_MAP['e']:
        if color == 'blue':
            color = 'orange'
        else:
            color = 'blue'

    elif key == simplegui.KEY_MAP['w']:
        global map_indicator, map_list, win, draw_map
        if detect_collide(exit, my_man):
            if map_indicator < (len(map_list) - 1):
                map_indicator += 1
                draw_map = True
            else:
                win = True

    elif key == simplegui.KEY_MAP['f']:
        my_man.pick()


def keyup(key):
    global vel_horizontal
    if key == simplegui.KEY_MAP['a']:
        my_man.vel += vel_horizontal
        my_man.moving_list[0] = False
    elif key == simplegui.KEY_MAP['d']:
        my_man.vel -= vel_horizontal
        my_man.moving_list[1] = False


def mouse_handler(position):
    global color, menu, start_game, toturial, start_game, level_menu, level_select_buttons, background_music, win
    #    if position[0] == 200:
    #        level_menu = True
    #        menu = False
    #        toturial = False
    if menu:
        if 150 <= position[0] < 200 and 200 <= position[1] <= 350:
            level_menu = True
            menu = False
            toturial = False
        if 300 <= position[0] and position[0] <= 400 and 200 <= position[1] and position[1] <= 350:
            toturial = True
    #    print color
    if start_game:
        if len(bullet_list) < 1:
            bullet_list.append(bullet(color, BULLET_VEL, BULLET_LENGTH, my_man, position))
        if 0 < position[0] < 20 and 0 < position[1] < 20:
            start_game = False
            menu = True
            background_music.rewind()
    if level_menu:
        for level_button in level_select_buttons:
            if level_button.pos[0] <= position[0] <= (level_button.pos[0] + level_button.width) and level_button.pos[
                1] <= position[1] <= (level_button.pos[1] + level_button.height):
                level_button.do_something()
        if 190 < position[0] < 270 and 410 < position[1] < 490:
            level_menu = False
            menu = True
    if win:
        if 160 < position[0] < 310 and 250 < position[1] < 300:
            win = False
            start_game = False
            level_menu = False
            menu = True
            background_music.rewind()


def draw_handler(canvas):
    global start_game, menu, toturial, win, background_image, background_info, map_list, map_indicator, draw_map, color, background_music, logo_image, logo_info, back_image, back_info, win_image, win_info
    # create everything
    if draw_map:
        map_list[map_indicator]()
    #        print map_indicator

    # draw everything
    if level_menu:
        canvas.draw_image(logo_image, logo_info.get_center(), logo_info.get_size(), [250, 120], [350, 200])
        for level_button in level_select_buttons:
            level_button.draw(canvas)
        canvas.draw_image(back_image, back_info.get_center(), back_info.get_size(), [230, 450], [40, 40])

    if menu:
        canvas.draw_image(logo_image, logo_info.get_center(), logo_info.get_size(), [250, 120], [350, 200])
        canvas.draw_text('Start', [150, 300], 30, 'white')
        canvas.draw_text('Tutorial', [300, 300], 30, 'white')
    if toturial:
        canvas.draw_text('"a" and "d" move,"w" enter exit,"e" open portals.', [40, 400], 20, 'white')
        canvas.draw_text('"Space" jump, "f" pick objects,use mouse to shoot', [40, 420], 20, 'white')
        canvas.draw_text('go to the purple square (that is exit)', [40, 440], 20, 'white')

    if start_game:
        canvas.draw_image(background_image, background_info.get_center(), background_info.get_size(),
                          [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2], [CANVAS_WIDTH, CANVAS_HEIGHT])
        my_man.draw(canvas)
        background_music.play()
        for wall in wall_list:
            wall.draw(canvas)
        for soft_wall in soft_wall_list:
            soft_wall.draw(canvas)
        for bullet in bullet_list:
            bullet.draw(canvas)
        for blue_portal in blue_portal_list:
            blue_portal.draw(canvas)
        for orange_portal in orange_portal_list:
            orange_portal.draw(canvas)
        for weight in weight_list:
            weight.draw(canvas)
        for button in button_list:
            button.draw(canvas)
        for gate in gate_list:
            gate.draw(canvas)
        exit.draw(canvas)
        canvas.draw_polygon([[480, 0], [500, 0], [500, 20], [480, 20]], 1, color, color)
        canvas.draw_image(back_image, back_info.get_center(), back_info.get_size(), [10, 10], [20, 20])

        # update everything
        my_man.update()
        for bullet in bullet_list:
            bullet.update()
        for button in button_list:
            button.update()
        for gate in gate_list:
            gate.update()
        #        button_1.update()
        #        button_2.update()
        ##        gate_up.update()
        #        gate_2.update()
        for weight in weight_list:
            weight.update()

    #        canvas.draw_polygon([[480,440],[490,440],[490,450],[480,450]],1,'purple','purple')
    #
    #    if 480<=my_man.pos[0]<=490 and 440<=my_man.pos[1]<=450:
    #        win = True
    if win:
        canvas.draw_image(win_image, win_info.get_center(), win_info.get_size(), [250, 250], [300, 200])
        canvas.draw_text('YOU WIN', [170, 225], 40, 'Black')
        canvas.draw_text('Back to main menu', [160, 300], 25, 'black')


# create everything
whole_map = grid(GRID_HEIGHT, GRID_WIDTH)
# sound
background_music = simplegui.load_sound('https://www.dropbox.com/s/akg5y6khdue3t8u/Darude%20-%20Sandstorm.mp3?dl=1')
# my_man = moving_objects([15,475],0,0,CHARACTER_SIZE,CELL_SIZE)

background_info = image_info([400, 400], [800, 800])
background_image = simplegui.load_image(
    "https://www.dropbox.com/s/8nf1y9zg0hevh68/sf066.bmp7a087b50-1853-4b55-9d69-f2eb0a023a77Original.jpg?dl=1")

wall_info = image_info([205, 205], [410, 410])
wall_image = simplegui.load_image('https://www.dropbox.com/s/zgkuuugyw7qro6n/shiphull.jpg?dl=1')

soft_info = image_info([368, 368], [736, 736])
soft_image = simplegui.load_image(
    'https://www.dropbox.com/s/gqhyqctr5aiqxiv/18938a9d33051ddf1f4441ea72a134ee--space-ship-textures-patterns.jpg?dl=1')

logo_info = image_info([527, 202], [1054, 404])
logo_image = simplegui.load_image('https://www.dropbox.com/s/wl3dx4v5pieajlp/Chopped%20logo.jpg?dl=1')

back_info = image_info([85, 85], [170, 170])
back_image = simplegui.load_image('https://www.dropbox.com/s/jnrx7jrswvi9dqi/unnamed.png?dl=1')

win_info = image_info([104, 66], [207, 131])
win_image = simplegui.load_image('https://www.dropbox.com/s/0dtgy5iaqv7hkk5/modified%20frame.jpg?dl=1')

my_man_info = image_info([74, 82], [15, 40])
my_man_image = simplegui.load_image('https://www.dropbox.com/s/9ikxrnic18hnl06/GiKHlUQ.png?dl=1')
my_man_info_2 = image_info([325, 82], [15, 40])
my_man_image_2 = simplegui.load_image('https://www.dropbox.com/s/uu7ui7y6ayzo9ed/01111733_GiKHlUQ.png?dl=1')
# draw menu
level_0_button = level_button([200, 250], 0)
level_1_button = level_button([200, 280], 1)
level_2_button = level_button([200, 310], 2)
level_3_button = level_button([200, 340], 3)
level_4_button = level_button([200, 370], 4)
level_5_button = level_button([200, 400], 5)
level_select_buttons.extend(
    [level_0_button, level_1_button, level_2_button, level_3_button, level_4_button, level_5_button])


def draw_main_menu(canvas):
    current_menu = 'main_menu'
    canvas.draw_image(logo_image, logo_info.get_center(), logo_info.get_size(), [250, 120], [350, 200])
    start_button = button


# draw map

def initiate():
    global blue_portal_list, orange_portal_list, gate_list, button_list, wall_list, soft_wall_list, weight_list, whole_map, bullet_list
    whole_map = grid(GRID_HEIGHT, GRID_WIDTH)
    blue_portal_list = []
    orange_portal_list = []
    blue_portal = portal([600, 470], 'blue', PORTAL_SHORT, PORTAL_LONG, 'left')
    orange_portal = portal([600, 470], 'orange', PORTAL_SHORT, PORTAL_LONG, 'right')
    blue_portal_list.append(blue_portal)
    orange_portal_list.append(orange_portal)
    gate_list = []
    button_list = []
    wall_list = []
    soft_wall_list = []
    bullet_list = []
    weight_list = []


def map_0():
    global gate_list, button_list, wall_list, soft_list, weight_list, my_man, exit, draw_map, my_man, my_man_image, my_man_info, my_man_image_2, my_man_info_2
    initiate()
    my_man = moving_objects([15, 450], 0, 0, CHARACTER_SIZE, CELL_SIZE, my_man_image, my_man_info, my_man_image_2,
                            my_man_info_2)
    exit = exits([48, 48], CELL_SIZE)
    create_soft_wall([0, 0], 1, GRID_HEIGHT)
    create_soft_wall([0, GRID_HEIGHT - 1], GRID_WIDTH, 1)
    create_soft_wall([GRID_WIDTH - 1, 0], 1, GRID_HEIGHT)
    create_soft_wall([0, 0], GRID_WIDTH, 1)
    create_soft_wall([15, 30], 2, 20)
    create_soft_wall([30, 30], 2, 20)
    draw_map = False


def map_1():
    global gate_list, button_list, wall_list, soft_list, weight_list, my_man, exit, draw_map, my_man, my_man_image, my_man_info, my_man_image_2, my_man_info_2
    initiate()
    my_man = moving_objects([15, 450], 0, 0, CHARACTER_SIZE, CELL_SIZE, my_man_image, my_man_info, my_man_image_2,
                            my_man_info_2)
    exit = exits([9, 28], CELL_SIZE)
    create_wall([0, 0], 1, GRID_HEIGHT)
    create_wall([0, GRID_HEIGHT - 1], GRID_WIDTH, 1)
    create_wall([GRID_WIDTH - 1, 0], 1, GRID_HEIGHT)
    create_wall([0, 0], GRID_WIDTH, 1)
    create_soft_wall([49, 44], 1, 5)
    create_wall([0, 29], 10, 1)
    create_soft_wall([0, 10], 1, 18)
    draw_map = False


def map_2():
    global gate_list, button_list, wall_list, soft_list, weight_list, my_man, exit, draw_map, my_man, my_man_image, my_man_info, my_man_image_2, my_man_info_2
    initiate()
    my_man = moving_objects([15, 190], 0, 0, CHARACTER_SIZE, CELL_SIZE, my_man_image, my_man_info, my_man_image_2,
                            my_man_info_2)
    exit = exits([48, 40], CELL_SIZE)
    create_wall([0, 0], 1, GRID_HEIGHT)
    create_wall([0, GRID_HEIGHT - 3], GRID_WIDTH, 3)
    create_wall([GRID_WIDTH - 1, 0], 1, GRID_HEIGHT)
    create_wall([0, 0], GRID_WIDTH, 1)
    create_wall([0, 26], 6, 2)
    create_wall([37, 41], 12, 6)
    create_wall([21, 0], 1, 40)
    create_soft_wall([0, 25], 6, 1)
    create_soft_wall([1, 28], 1, 19)
    create_soft_wall([2, 46], 35, 1)
    create_soft_wall([37, 41], 1, 6)
    create_soft_wall([38, 41], 11, 1)
    create_soft_wall([20, 1], 1, 39)
    create_soft_wall([22, 1], 1, 39)
    draw_map = False


def map_3():
    global gate_list, button_list, wall_list, soft_list, weight_list, my_man, exit, draw_map, my_man, my_man_image, my_man_info, my_man_image_2, my_man_info_2
    initiate()
    my_man = moving_objects([15, 450], 0, 0, CHARACTER_SIZE, CELL_SIZE, my_man_image, my_man_info, my_man_image_2,
                            my_man_info_2)
    exit = exits([48, 9], CELL_SIZE)
    create_wall([0, 0], 1, GRID_HEIGHT)
    create_wall([0, GRID_HEIGHT - 1], GRID_WIDTH, 1)
    create_wall([GRID_WIDTH - 1, 0], 1, GRID_HEIGHT)
    create_wall([0, 0], GRID_WIDTH, 1)
    create_wall([40, 10], 10, 1)
    create_wall([1, 1], 4, 44)
    create_soft_wall([1, 44], 4, 1)
    create_soft_wall([0, GRID_HEIGHT - 1], GRID_WIDTH, 1)
    draw_map = False


def map_4():
    global gate_list, button_list, wall_list, soft_list, weight_list, my_man, exit, draw_map, my_man, my_man_image, my_man_info, my_man_image_2, my_man_info_2
    initiate()
    my_man = moving_objects([15, 420], 0, 0, CHARACTER_SIZE, CELL_SIZE, my_man_image, my_man_info, my_man_image_2,
                            my_man_info_2)
    exit = exits([48, 7], CELL_SIZE)
    create_wall([0, 0], 1, GRID_HEIGHT)
    create_wall([0, GRID_HEIGHT - 3], GRID_WIDTH, 3)
    create_wall([GRID_WIDTH - 1, 0], 1, GRID_HEIGHT)
    create_wall([0, 0], GRID_WIDTH, 3)
    create_wall([47, 8], 2, 40)
    create_wall([37, 41], 12, 6)
    create_wall([10, 41], 27, 1)
    create_wall([1, 41], 8, 1)
    create_wall([28, 8], 20, 2)
    create_wall([32, 6], 4, 2)
    create_wall([39, 4], 4, 2)
    gate_1 = gate([9, 41])
    gate_2 = gate([9, 40])
    gate_3 = gate([35, 5])
    gate_4 = gate([35, 4])
    gate_list.extend([gate_1, gate_2, gate_3, gate_4])
    button_1 = button([8, 46], BUTTON_LONG, BUTTON_SHORT, [gate_1, gate_2])
    button_2 = button([32, 6], BUTTON_LONG, BUTTON_SHORT, [gate_3, gate_4])
    button_list.extend([button_1, button_2])
    create_soft_wall([1, 3], 48, 1)
    create_soft_wall([1, 46], 36, 1)
    create_soft_wall([37, 42], 1, 5)
    create_soft_wall([10, 40], 37, 1)
    create_soft_wall([1, 40], 8, 1)
    create_soft_wall([32, 6], 4, 2)
    create_soft_wall([39, 4], 1, 2)
    draw_map = False


def map_5():
    global gate_list, button_list, wall_list, soft_list, weight_list, my_man, exit, draw_map, my_man, my_man_image, my_man_info, my_man_image_2, my_man_info_2
    initiate()
    my_man = moving_objects([15, 450], 0, 0, CHARACTER_SIZE, CELL_SIZE, my_man_image, my_man_info, my_man_image_2,
                            my_man_info_2)
    gate_up = gate([7, 4])
    gate_2 = gate([47, 44])
    gate_list.extend([gate_up, gate_2])
    button_1 = button([35, 45], BUTTON_LONG, BUTTON_SHORT, [gate_up])
    button_2 = button([39, 45], BUTTON_LONG, BUTTON_SHORT, [gate_2])
    button_list.extend([button_1, button_2])
    weight_list.append(weight([73, 11], 10))
    exit = exits([48, 44], CELL_SIZE)
    create_wall([0, 0], 1, GRID_HEIGHT)
    create_wall([0, GRID_HEIGHT - 1], GRID_WIDTH, 1)
    create_wall([GRID_WIDTH - 1, 0], 1, GRID_HEIGHT)
    create_wall([0, 0], GRID_WIDTH, 1)
    create_wall([5, 1], 1, 4)
    create_wall([6, 4], 1, 1)
    create_wall([8, 4], 2, 1)
    create_wall([9, 1], 1, 4)
    create_wall([35, 45], 15, 5)
    create_wall([47, 1], 1, 42)
    create_soft_wall([0, 0], 1, GRID_HEIGHT)
    create_soft_wall([0, GRID_HEIGHT - 1], GRID_WIDTH, 1)
    draw_map = False


map_list.extend([map_0, map_1, map_2, map_3, map_4, map_5])

frame = simplegui.create_frame('background', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background('black')
frame.set_draw_handler(draw_handler)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(mouse_handler)

frame.start()