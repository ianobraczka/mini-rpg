"""Items / pickups — extension point for students (not used in core loop yet)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Item:
    """A simple collectible or equipment placeholder for future exercises."""

    name: str
    description: str = ""
