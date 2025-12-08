# Pygkit

A collection of modular add-ons and utilities for Pygame, designed to streamline and enhance game development with easy-to-use features.

**Note**: This library is still in the early stages of development, and as such, certain functionality may change with updates.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

Pygkit is currently in early development and cannot yet be installed via PyPi. To install it, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the base folder of your local clone in the terminal.
3. Type `python -m pip install -e .` to install it (replacing `python` with the appropriate name for the Python version to which you wish to install the library—on Windows usually `py.exe`, and on Mac/Linux usually `python3`).

## Usage

To use Pygkit in your Pygame project, simply import the desired module(s) and use them alongside your existing Pygame code. Here's an example of importing and using the debug module:

```python
import pygame
import pygkit

### Pygame setup here ###

debug_overlay = pygkit.debug.DebugOverlay()

while True: 

    ### Game loop logic here ###

    debug_overlay.draw(
        position="topright",
        background_enabled=False,
        test_message="This is a test message."
    )
```

The library also includes an `AnimatedSprite` helper for managing sprite
animations. Frames can come from a list of `pygame.Surface` objects or from a
sprite sheet, while the `update` method advances the animation using the elapsed
time in seconds:

```python
import pygame
from pygkit.sprite import AnimatedSprite

pygame.init()
clock = pygame.time.Clock()

frames = [pygame.Surface((32, 32), pygame.SRCALPHA) for _ in range(4)]
sprite = AnimatedSprite(frames, frame_time=0.1)

running = True
while running:
    dt = clock.tick(60) / 1000  # seconds
    sprite.update(dt)
```

See `examples/animated_sprite_example.py` for a runnable demonstration that
shows basic playback controls.

## Modules

Pygkit will be designed to work alongside Pygame, providing additional functionality through various modules. Here are a few of the planned modules:

- **Sprite**: Sprite sheet helpers including an animated sprite class.
- **AI**: Tools and algorithms to help you create engaging game AI.
- **GUI**: Components for creating menus, text boxes, and other user interface elements.
- **Debug**: Various debug overlays that can be used to display real-time game information during development.
- *And more to come!*

## Examples

You can find examples showcasing how to use Pygkit's features in various scenarios in the `examples` folder of the repository.

## Contributing

We welcome contributions to Pygkit! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information on how to get started.

## License

This project is licensed under the GNU LGPL version 2.1 License. See the [LICENSE](LICENSE) file for details.
