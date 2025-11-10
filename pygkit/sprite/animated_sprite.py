"""Utilities for working with animated sprites."""

from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple, Union

import pygame

FrameSource = Union[str, pygame.Surface, Sequence[pygame.Surface]]


class AnimatedSprite(pygame.sprite.Sprite):
    """A sprite that cycles through a sequence of frames.

    The class is intentionally lightweight and only manages the image used for
    rendering. Logic such as positioning the sprite or handling collisions
    remains the responsibility of the consumer, just like with regular
    ``pygame.sprite.Sprite`` instances.

    Parameters
    ----------
    frames:
        A sequence of ``pygame.Surface`` objects representing the animation
        frames. Alternatively, a path to an image file or a single surface may
        be supplied when ``frame_size`` is provided so that the sprite sheet can
        be sliced automatically.
    frame_size:
        The width and height of the individual frames inside the sprite sheet.
        This is required whenever ``frames`` is a sprite sheet (a string path or
        a surface containing multiple frames).
    frame_durations:
        An optional sequence specifying the duration of each frame in seconds.
        When omitted every frame will use the same duration supplied via
        ``frame_time``.
    frame_time:
        The duration, in seconds, each frame should be displayed when
        ``frame_durations`` is not provided. Defaults to 0.1 seconds.
    loop:
        Whether the animation should loop. When disabled the animation will stop
        on the last frame.
    auto_play:
        If ``True`` the animation will immediately begin playing.
    position:
        The initial top-left position of the sprite's rectangle.
    """

    def __init__(
        self,
        frames: FrameSource,
        *,
        frame_size: Optional[Tuple[int, int]] = None,
        frame_durations: Optional[Sequence[float]] = None,
        frame_time: float = 0.1,
        loop: bool = True,
        auto_play: bool = True,
        position: Tuple[int, int] = (0, 0),
    ) -> None:
        super().__init__()

        self._frames: List[pygame.Surface] = self._normalize_frames(
            frames, frame_size
        )
        if not self._frames:
            raise ValueError("AnimatedSprite requires at least one frame.")

        self._durations = self._normalise_durations(
            frame_durations, frame_time, len(self._frames)
        )
        self.loop = loop
        self._playing = auto_play
        self._frame_index = 0
        self._elapsed = 0.0

        self.image = self._frames[0]
        self.rect = self.image.get_rect(topleft=position)

    @staticmethod
    def _normalize_frames(
        frames: FrameSource, frame_size: Optional[Tuple[int, int]]
    ) -> List[pygame.Surface]:
        if isinstance(frames, (list, tuple)):
            if not all(isinstance(frame, pygame.Surface) for frame in frames):
                raise TypeError("All frames must be pygame.Surface instances.")
            return [frame.copy() for frame in frames]

        if isinstance(frames, pygame.Surface):
            if frame_size is None:
                raise ValueError("frame_size is required when using a sprite sheet.")
            return AnimatedSprite._slice_sprite_sheet(frames, frame_size)

        if isinstance(frames, str):
            if frame_size is None:
                raise ValueError("frame_size is required when using a sprite sheet.")
            sheet = pygame.image.load(frames).convert_alpha()
            return AnimatedSprite._slice_sprite_sheet(sheet, frame_size)

        raise TypeError(
            "frames must be a sequence of Surfaces, a Surface, or a file path."
        )

    @staticmethod
    def _slice_sprite_sheet(
        sprite_sheet: pygame.Surface, frame_size: Tuple[int, int]
    ) -> List[pygame.Surface]:
        frame_width, frame_height = frame_size
        if frame_width <= 0 or frame_height <= 0:
            raise ValueError("frame_size values must be positive integers.")

        sheet_width, sheet_height = sprite_sheet.get_size()
        frames: List[pygame.Surface] = []
        for top in range(0, sheet_height, frame_height):
            if top + frame_height > sheet_height:
                break
            for left in range(0, sheet_width, frame_width):
                if left + frame_width > sheet_width:
                    break
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(
                    sprite_sheet,
                    (0, 0),
                    pygame.Rect(left, top, frame_width, frame_height),
                )
                frames.append(frame)

        return frames

    @staticmethod
    def _normalise_durations(
        frame_durations: Optional[Sequence[float]],
        frame_time: float,
        frame_count: int,
    ) -> List[float]:
        if frame_durations is None:
            if frame_time <= 0:
                raise ValueError("frame_time must be greater than zero.")
            return [frame_time for _ in range(frame_count)]

        durations = list(frame_durations)
        if len(durations) != frame_count:
            raise ValueError("frame_durations must match the number of frames.")
        if any(duration <= 0 for duration in durations):
            raise ValueError("frame_durations must contain positive values.")
        return durations

    @property
    def playing(self) -> bool:
        """Whether the animation is currently playing."""

        return self._playing

    @property
    def frame_index(self) -> int:
        """The index of the currently displayed frame."""

        return self._frame_index

    def play(self) -> None:
        """Resume the animation from the current frame."""

        self._playing = True

    def pause(self) -> None:
        """Pause the animation without resetting the frame index."""

        self._playing = False

    def stop(self) -> None:
        """Stop the animation and rewind to the first frame."""

        self._playing = False
        self._frame_index = 0
        self._elapsed = 0.0
        self.image = self._frames[self._frame_index]

    def reset(self) -> None:
        """Reset the animation to the first frame while preserving play state."""

        self._frame_index = 0
        self._elapsed = 0.0
        self.image = self._frames[self._frame_index]

    def update(self, dt: float) -> None:
        """Advance the animation.

        Parameters
        ----------
        dt:
            The elapsed time in seconds since the last update call.
        """

        if not self._playing or not self._frames:
            return

        self._elapsed += dt

        while self._elapsed >= self._durations[self._frame_index]:
            self._elapsed -= self._durations[self._frame_index]
            self._frame_index += 1

            if self._frame_index >= len(self._frames):
                if self.loop:
                    self._frame_index = 0
                else:
                    self._frame_index = len(self._frames) - 1
                    self._playing = False
                    break

        self.image = self._frames[self._frame_index]

    def set_frame(self, index: int) -> None:
        """Force the sprite to display the frame at ``index``."""

        if not 0 <= index < len(self._frames):
            raise IndexError("Frame index out of range.")

        self._frame_index = index
        self._elapsed = 0.0
        self.image = self._frames[self._frame_index]

    def add_frame(self, frame: pygame.Surface, duration: Optional[float] = None) -> None:
        """Append a new frame to the animation."""

        if not isinstance(frame, pygame.Surface):
            raise TypeError("frame must be a pygame.Surface instance.")

        self._frames.append(frame.copy())
        if duration is None:
            duration = self._durations[-1]
        if duration <= 0:
            raise ValueError("duration must be greater than zero.")
        self._durations.append(duration)

    def set_position(self, position: Tuple[int, int]) -> None:
        """Update the sprite's position."""

        self.rect.topleft = position

    def center_on(self, position: Tuple[int, int]) -> None:
        """Center the sprite on ``position``."""

        self.rect.center = position

    def frames(self) -> Iterable[pygame.Surface]:
        """Return an iterable over the animation frames."""

        return tuple(frame.copy() for frame in self._frames)
