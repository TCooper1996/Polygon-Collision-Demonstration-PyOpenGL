from OpenGL.GL import *


class Shader:
    def Use(self):
        glUseProgram(self.ID)
        return self

    def Compile(self, vertexSource, fragmentSource):
        #Compile Vertex Shader
        sVertex = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(sVertex, vertexSource)
        glCompileShader(sVertex, "VERTEX")
        #Compile Fragment Shader
        sFragment = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(sFragment, fragmentSource)
        glCompileShader(sFragment, "FRAGMENT")
        #Shader program
        self.ID = glCreateProgram()
        glAttachShader(self.ID, sVertex)
        glAttachShader(self.ID, sFragment)
        glLinkProgram(self.ID)
        self.checkCompileErrors(self.ID, "PROGRAM")
        glDeleteShader(sVertex)
        glDeleteShader(sFragment)

    def SetVector(self, name, value, useShader):
        if useShader:
            self.Use()
        #I am assuming numpy arrays can be accessed using standard notation.
        glUniform3f(glGetUniformLocation(self.ID, name), value[0], value[1], value[2])

    def SetMatrix(self, name, matrix, useShader):
        if useShader:
            self.Use()
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, matrix)

    def SetInteger(self, name, value, useShader):
        if useShader:
            self.Use()
        glUniform1i(glGetUniformLocation(self.ID, name), value)

    def checkCompileErrors(self, _object, _type):
        infoLog = ""
        if _type != "PROGRAM":
            success = glGetShaderiv(_object, GL_COMPILE_STATUS, None)
            if not success:
                glGetShaderInfoLog(_object, 1024, None, infoLog)
                print("ERROR: Compile-time error:\n\tType: {0}\n\t{1}".format(_type, infoLog))

        else:
            success = glGetProgramiv(_object, GL_LINK_STATUS, None)
            if not success:
                glGetProgramInfoLog(_object, 1024, None, infoLog)
                print("ERROR: Link-time error:\n\tType: {0}\n\t{1}".format(_type, infoLog))
