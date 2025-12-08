"""Example showing how to use :class:`pygkit.sprite.AnimatedSprite`."""

import os
import tempfile

import pygame

from pygkit.sprite import AnimatedSprite

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
FPS = 60
FRAME_SIZE = (64, 64)


# Helper to build some simple animation frames without any assets
def build_sprite_sheet() -> str:
    """Create a temporary sprite sheet and return its file path."""

    num_frames = 12
    body_color = "#22d3ee"
    outline_color = "#0f172a"

    frames: list[pygame.Surface] = []
    for i in range(num_frames):
        surface = pygame.Surface(FRAME_SIZE, pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        angle = (360 / num_frames) * i
        center = pygame.Vector2(surface.get_rect().center)

        # Build a diamond and rotate it slightly each frame
        base_points = [
            pygame.Vector2(0, -22),
            pygame.Vector2(20, 0),
            pygame.Vector2(0, 22),
            pygame.Vector2(-20, 0),
        ]
        points = [center + point.rotate(angle) for point in base_points]

        pygame.draw.polygon(surface, body_color, points)
        pygame.draw.polygon(surface, outline_color, points, width=4)

        # Add a highlight that tracks the top tip as it rotates
        tip = center + pygame.Vector2(0, -22).rotate(angle)
        glow_radius = 8
        pygame.draw.circle(surface, "#67e8f9", tip, glow_radius)
        pygame.draw.circle(surface, "#ffffff", tip, glow_radius - 3)

        frames.append(surface)

    # Combine frames into a simple horizontal sprite sheet
    sheet_width = FRAME_SIZE[0] * len(frames)
    sheet = pygame.Surface((sheet_width, FRAME_SIZE[1]), pygame.SRCALPHA)
    for i, frame in enumerate(frames):
        sheet.blit(frame, (i * FRAME_SIZE[0], 0))

    handle = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    pygame.image.save(sheet, handle.name)
    handle.close()
    return handle.name


class Game:
    """Minimal example that animates a sprite and lets you pause with SPACE."""

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AnimatedSprite example")
        self.clock = pygame.time.Clock()

        self._sheet_path = build_sprite_sheet()
        self.sprite = AnimatedSprite(
            self._sheet_path,
            frame_size=FRAME_SIZE,
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
        try:
            while True:
                dt = self.clock.tick(FPS) / 1000  # seconds

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

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
        finally:
            self._cleanup()

    def _draw_instructions(self) -> None:
        font = pygame.font.Font(None, 28)
        status = "playing" if self.sprite.playing else "paused"
        text = font.render(f"Space toggles animation ({status})", True, "#e2e8f0")
        self.screen.blit(text, (20, SCREEN_HEIGHT - 40))

    def _cleanup(self) -> None:
        pygame.quit()
        if hasattr(self, "_sheet_path") and os.path.exists(self._sheet_path):
            try:
                os.remove(self._sheet_path)
            except OSError:
                pass


if __name__ == "__main__":
    Game().run()
