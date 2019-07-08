from collections import defaultdict, namedtuple
import pyrr
import numpy as np

bufferData = namedtuple("bufferData", "vertexBuffer indexBuffer")
colorData = {"RED": np.array([1, 0, 0], dtype=np.float32),
             "BLACK": np.array([0, 0, 0], dtype=np.float32),
             "GREEN": np.array([0, 1, 0], dtype=np.float32),
             }


class GameObject:
    basis_arrays = {}

    def __init__(self, sides, radius, pos):
        self.sides = sides
        self.radius = radius
        self.pos = pos
        self.color = colorData["BLACK"]
        self.velocity = 5
        self.Rotation = 0
        self.__vertexArray = np.array([])
        self.initBufferData()
        #  This bool indicates whether the polygon has been moved. If true, getFinalVertices must be called again.
        self.changed = True

    def Draw(self, renderer):
        renderer.DrawPolygon(self)

    def SetColor(self, color):
        self.color = colorData[color]

    def initBufferData(self):
        # Define size of vertex and index array
        # VertexArraySize is initially self.sides * 2 + 2 and filled with 2 coordinates.
        # The final result is a flat list of x y values
        vertexArraySize = self.sides * 2 + 2  # Do not change this to accommodate 3 floats per vertex! Insertion below
        indexArraySize = self.sides * 2 + 2
        # Create vertex array
        funcs = {0: np.cos, 1: np.sin}
        vertices = [self.radius * funcs[i % 2](2 * np.pi * (i // 2) / self.sides)
                             for i in range(vertexArraySize)]
        vertices[-2], vertices[-1] = 0, 0  # Set last vertex as origin
        # Create index array
        indices = np.array([(i + 1) // 2 for i in range(indexArraySize)], dtype=np.uint32)
        # Connect last vertex to origin, then connect last vertex to first real vertex
        indices[-4], indices[-3], indices[-2], indices[-1] = (indexArraySize // 2 - 2), 0, 0, (indexArraySize // 2) - 1
        GameObject.basis_arrays[self.sides] = bufferData(vertices, indices)

    # This method takes the basis vertices, adds the z dimension (necessary for transformation math), performs the trans
    # /formation, and then removes the z dimension.
    def calcFinalVertices(self, xOffset=0, yOffset=0, rOffset=0):
        modelTran = pyrr.matrix44.create_from_translation(np.array([self.pos[0] + xOffset, self.pos[1] + yOffset, 0],
                                                                   dtype=np.float32))
        modelRot = pyrr.matrix44.create_from_axis_rotation(np.array([0, 0, 1],
                                                                    dtype=np.float32), self.Rotation + rOffset)
        finalModel = pyrr.matrix44.multiply(modelRot, modelTran)

        #  Copy basis arrays (which are actually lists) to local var to avoid mutation.
        vertexList = GameObject.basis_arrays[self.sides].vertexBuffer.copy()
        #  Add 0 to every third position to add a z axis
        for i in range(len(vertexList) // 2):  # VertexArraySize // 2 because that is our number of vertices
            vertexList.insert(i * 3 + 2, 0)
        vertexArray = np.array(vertexList, dtype=np.float32)
        #  Resize array so that each item in vertexArray is a vec3
        vertexArray = np.resize(vertexArray, (len(vertexArray) // 3, 3))
        #  Apply transformation matrix on each vector
        vertexArray = [pyrr.matrix44.apply_to_vector(finalModel, vertexArray[i]) for i in range(self.sides + 1)]
        #  Remove the dummy z values
        vertexArray = [vector[0:2] for vector in vertexArray]
        #  Flatten list of arrays and return
        return np.array(vertexArray).flatten()

    def getVertices(self):
        if self.changed:
            self.__vertexArray = self.calcFinalVertices()
            self.changed = False
        return self.__vertexArray

    def setVertices(self, vertices):
        self.__vertexArray = vertices

    def addPosition(self, x, y, a):
        self.pos[0] += x
        self.pos[1] += y
        self.Rotation += a
