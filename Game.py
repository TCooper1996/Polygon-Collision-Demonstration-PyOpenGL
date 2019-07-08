from cyglfw3 import *
import pyrr
import numpy
from ResourceManager import *
from Renderer import *


class Game:

    def __init__(self, width, height):
        self.Keys = [False] * 1024
        self.Width = width
        self.Height = height
        self.PLAYER_VELOCITY = 500
        self.gameObjects = [GameObject.GameObject(i + 3, 50, [100 + i * 200, 300]) for i in range(3)]
        self.selected = self.gameObjects[0]
        self.selected.SetColor("RED")
        self.keyLocked = False

    def Init(self):
        ResourceManager.LoadShader("vertex.glsl", "fragment.glsl", None, "sprite")
        self.renderer = Renderer(ResourceManager.GetShader("sprite"))
        projection = pyrr.matrix44.create_orthogonal_projection(float(0), float(self.Width), float(0), float(self.Height), float(-1), float(1))
        ResourceManager.GetShader("sprite").Use().SetInteger("sprite", 0, False)  # Assuming false?
        ResourceManager.GetShader("sprite").SetMatrix("projection", projection, False)  # Assuming false?

    def ProcessInput(self, dt):
        velocity = self.PLAYER_VELOCITY * dt
        next_x, next_y = 0, 0
        walk = self.Keys[KEY_W] != self.Keys[KEY_S]
        turn = self.Keys[KEY_A] != self.Keys[KEY_D]
        if walk or turn:
            turn_angle = float(0.1) if turn else 0
            if self.Keys[KEY_D]: turn_angle *= -1
            if self.Keys[KEY_S]: velocity *= -1
            if walk:
                nextX = numpy.cos(self.selected.Rotation) * velocity
                nextY = numpy.sin(self.selected.Rotation) * velocity

            new_vertices = self.selected.calcFinalVertices(xOffset=next_x, yOffset=next_y, rOffset=turn_angle)
            collisions = [self.checkOverlap(new_vertices, other.getVertices())
                          for other in self.gameObjects if self.selected != other]
            if not any(collisions):
                self.selected.setVertices(new_vertices)
                self.selected.addPosition(next_x, next_y, turn_angle)

        if self.Keys[KEY_SPACE] and not self.keyLocked:
            #  Set current _object to black before setting next object
            self.selected.SetColor("BLACK")
            if self.selected == self.gameObjects[0]:
                self.selected = self.gameObjects[1]
            elif self.selected == self.gameObjects[1]:
                self.selected = self.gameObjects[2]
            else:
                self.selected = self.gameObjects[0]

            #  Set new_object to red
            self.selected.SetColor("RED")
            self.keyLocked = True
        if not self.Keys[KEY_SPACE]:
            self.keyLocked = False

    def update(self, dt):
        self.DoCollisionsSAT()

    def render(self):
        for g in self.gameObjects:
            g.Draw(self.renderer)


    # Returns bool defined by collision
    def checkOverlap(self, p1Vertices, p2Vertices):
        # Closure returns list of normalized np vectors
        def obtainAxes(vertices):
            vertSize = len(vertices)
            axes = []
            #  Compare every pair of vertices
            for i in range(0, vertSize, 2):
                # Get first vector using slice, + 2 due to exclusive upper bound
                vec1 = np.array(vertices[i:i+2])
                # Slicing is avoided here due to cases like vertices[6:0]
                vec2 = np.array([vertices[(i + 2) % vertSize], vertices[(i + 3) % vertSize]])
                # Subtract vectors to get their edge
                edge = vec1 - vec2
                # Get orthogonal vector
                edge = [edge[1], -edge[0]]
                # Normalize
                edge = edge / np.linalg.norm(edge)
                axes.append(edge)
            return axes

        # Closure returns a tuple of the min and max values projected on the axis
        def projectVertices(axis, vertices):
            min_ = np.dot(axis, vertices[:2])
            max_ = min_
            for i in range(0, len(vertices), 2):
                product = np.dot(axis, vertices[i:i + 2])
                if product < min_:
                    min_ = product
                elif product > max_:
                    max_ = product
            return min_, max_
        #  This is the main code for checkOverlap
        #  The final (origin) vertex must be removed
        p1Vertices = p1Vertices[:-2]
        p2Vertices = p2Vertices[:-2]
        axes1 = obtainAxes(p1Vertices)
        axes2 = obtainAxes(p2Vertices)
        for axis in axes1 + axes2:
            min1, max1 = projectVertices(axis, p1Vertices)
            min2, max2 = projectVertices(axis, p2Vertices)

            if not (min2 <= min1 <= max2 or min2 <= max1 <= max2
                    or min1 <= min2 <= max1 or min1 <= max2 <= max1):
                return False
        return True

    def DoCollisionsSAT(self):
        for polygon in self.gameObjects:
            if polygon != self.selected:
                polygon.SetColor("BLACK")
            else:
                polygon.SetColor("RED")
        for i in range(len(self.gameObjects)):
            polygon1 = self.gameObjects[i]
            polygon2 = self.gameObjects[(i + 1) % len(self.gameObjects)]
            if polygon1 != polygon2 and self.checkOverlap(polygon1.getVertices(), polygon2.getVertices()):
                polygon1.SetColor("GREEN")
                polygon2.SetColor("GREEN")

