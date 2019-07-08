from OpenGL.GL import *
from cyglfw3 import *
import Game

def key_callback(window, key, scancode, action, mode):
    if key == KEY_ESCAPE and action == PRESS:
        SetWindowShouldClose(window, GL_TRUE)

    if key >= 0 and key < 1024:
        if action == PRESS:
            game.Keys[key] = GL_TRUE
        elif action == RELEASE:
            game.Keys[key] = GL_FALSE


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

game = Game.Game(SCREEN_WIDTH, SCREEN_HEIGHT)


def main():
    Init()
    WindowHint(CONTEXT_VERSION_MAJOR, 3)
    WindowHint(CONTEXT_VERSION_MINOR, 3)
    WindowHint(OPENGL_PROFILE, OPENGL_CORE_PROFILE)
    WindowHint(RESIZABLE, GL_FALSE)
    WindowHint(SAMPLES, 4)

    window = CreateWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Collision Test", None, None)
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    MakeContextCurrent(window)

    #glewExperimantal = GL_TRUE
    #glewInit()

    SetKeyCallback(window, key_callback)

    glLineWidth(2)
    glEnable(GL_MULTISAMPLE)

    deltaTime = float(0.0)
    lastFrame = float(0.0)

    game.Init()

    clearColor = [float(1) for _ in range(4)]

    while not WindowShouldClose(window):
        currentFrame = GetTime()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame
        PollEvents()

        game.ProcessInput(deltaTime)
        game.update(deltaTime)
        glClearColor(*clearColor)
        glClear(GL_COLOR_BUFFER_BIT)
        game.render()

        SwapBuffers(window)

    Terminate()


if __name__ == "__main__":
    main()
