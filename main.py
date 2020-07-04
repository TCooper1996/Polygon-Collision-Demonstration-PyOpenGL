from OpenGL.GL import *
import glfw

import Game


def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)

    if key >= 0 and key < 1024:
        if action == glfw.PRESS:
            game.Keys[key] = GL_TRUE
        elif action == glfw.RELEASE:
            game.Keys[key] = GL_FALSE


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

game = Game.Game(SCREEN_WIDTH, SCREEN_HEIGHT)


def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
    glfw.window_hint(glfw.SAMPLES, 4)

    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Collision Test", None, None)
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    glLineWidth(2)
    glEnable(GL_MULTISAMPLE)

    deltaTime = float(0.0)
    lastFrame = float(0.0)

    game.Init()

    clearColor = [float(1) for _ in range(4)]

    # Main loop
    while not glfw.window_should_close(window):
        # Maintain time between frames in order to make motion independent of cpu speed.
        # By scaling the magnitude of movement to the loop speed, game time is syncronized with real time.
        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        # Grab keyboard events
        glfw.poll_events()

        # Process input and update screen objects
        game.ProcessInput(deltaTime)
        game.update(deltaTime)

        # Clear screen
        glClearColor(*clearColor)
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw to buffer
        game.render()

        # Swap buffers to show changes
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
