# Abstract
This is an exercise in OpenGl which applies principals from linear algebra to implement a basic 2D collision detection system.

## Dependencies
You will need:
* python3
* pyOpenGL
* glfw
* numpy
* pyrr

```shell
pip3 install PyOpenGL PyOpenGL_accelerate glfw numpy pyrr
```

## Use
```shell
python3 main.py
```

## Controls
Use the up and down arrow keys to move forwards and backwards, and the left and right keys to rotate.
Hitting the spacebar toggles between controlling each shape.
As you move around, you'll see that you are blocked upon colliding with the other shapes.
