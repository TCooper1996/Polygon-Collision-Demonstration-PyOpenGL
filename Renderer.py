import pyrr
import numpy as np
from OpenGL.GL import *
import GameObject


class Renderer:
    def __init__(self, shader):
        self.shapeBuffers = []
        self.shader = shader
        self.initRenderData()

    def DrawPolygon(self, polygon: GameObject):
        indexArray = GameObject.GameObject.basis_arrays[polygon.sides].indexBuffer

        #Configure VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, polygon.getVertices(), GL_DYNAMIC_DRAW)
        #Configure IBO
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.IBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexArray, GL_DYNAMIC_DRAW)

        self.shader.Use()

        finalModel = pyrr.matrix44.create_identity(np.float32)
        self.shader.SetMatrix("model", finalModel, False)  # False parameter is a guess

        self.shader.SetVector("spriteColor", polygon.color, False)  # False parameter is a guess

        glBindVertexArray(self.quadVAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.IBO)
        glDrawElements(GL_LINES, len(indexArray), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def initRenderData(self):
        self.quadVAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.IBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.IBO)

        glBindVertexArray(self.quadVAO)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(GLfloat), None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
