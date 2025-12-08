"""Example showing how to use :class:`pygkit.sprite.AnimatedSprite`."""

import sys
import pygame

from pygkit.sprite import AnimatedSprite

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
FPS = 60
FRAME_SIZE = (64, 64)


# Helper to build some simple animation frames without any assets
def build_frames() -> list[pygame.Surface]:
    """Create a set of colored frames for demonstration purposes."""

    palette = [
        "#f08080",  # light coral
        "#f4a460",  # sandy brown
        "#ffd700",  # gold
        "#90ee90",  # light green
        "#87cefa",  # light sky blue
        "#dda0dd",  # plum
    ]

    frames: list[pygame.Surface] = []
    for i, color in enumerate(palette):
        surface = pygame.Surface(FRAME_SIZE, pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        # Draw a colored square with a contrasting outline that moves slightly
        rect = surface.get_rect().inflate(-12, -12)
        rect.move_ip(i % 6 - 3, (i * 2) % 8 - 4)
        pygame.draw.rect(surface, color, rect, border_radius=8)
        pygame.draw.rect(surface, "#1a1a1a", rect, width=3, border_radius=8)

        # Draw a small highlight that orbits around the center to show motion
        angle = (i / len(palette)) * 360
        offset = pygame.Vector2(18, 0).rotate(angle)
        highlight_center = surface.get_rect().center + offset
        pygame.draw.circle(surface, "#ffffff", highlight_center, 6)

        frames.append(surface)

    return frames


class Game:
    """Minimal example that animates a sprite and lets you pause with SPACE."""

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AnimatedSprite example")
        self.clock = pygame.time.Clock()

        frames = build_frames()
        self.sprite = AnimatedSprite(
            frames,
            frame_time=0.12,
            loop=True,
            auto_play=True,
            position=(
                SCREEN_WIDTH // 2 - FRAME_SIZE[0] // 2,
                SCREEN_HEIGHT // 2 - FRAME_SIZE[1] // 2,
            ),
        )
        self.sprites = pygame.sprite.Group(self.sprite)

    def run(self) -> None:
        while True:
            dt = self.clock.tick(FPS) / 1000  # seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Toggle the animation on and off
                    if self.sprite.playing:
                        self.sprite.pause()
                    else:
                        self.sprite.play()

            self.sprites.update(dt)

            self.screen.fill("#0f172a")
            self.sprites.draw(self.screen)

            # Simple text instructions
            self._draw_instructions()

            pygame.display.flip()

    def _draw_instructions(self) -> None:
        font = pygame.font.Font(None, 28)
        status = "playing" if self.sprite.playing else "paused"
        text = font.render(f"Space toggles animation ({status})", True, "#e2e8f0")
        self.screen.blit(text, (20, SCREEN_HEIGHT - 40))


if __name__ == "__main__":
    Game().run()
