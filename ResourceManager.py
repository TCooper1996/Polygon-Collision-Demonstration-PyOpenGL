from OpenGL.GL import *
import Shader


class ResourceManager:
    Shaders = {}
    @staticmethod
    def LoadShader(vShaderFile, fShaderFile, gShaderFile, name):
        ResourceManager.Shaders[name] = ResourceManager.loadShaderFromFile(vShaderFile, fShaderFile)
        return ResourceManager.Shaders[name]

    @staticmethod
    def GetShader(name):
        return ResourceManager.Shaders[name]

    @staticmethod
    def Clear():
        for s in ResourceManager.Shaders:
            glDeleteProgram(s.second.ID)

    @staticmethod
    def loadShaderFromFile(vShaderFile, fShaderFile):
        try:
            with open(vShaderFile, 'r')as file:
                vertexCode = file.read()
            with open(fShaderFile, 'r')as file:
                fragmentCode = file.read()
        except FileNotFoundError:
            print("ERROR: Failed to read vertex/fragment shader")

        #vShaderCode = vertexCode.c_str() Not sure if shader.compile needs a c string.
        #fShaderCode = fragmentCode.c_str()
        shader = Shader.Shader()
        shader.Compile(vertexCode, fragmentCode)
        return shader


