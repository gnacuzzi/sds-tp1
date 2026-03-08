from dataclasses import dataclass


@dataclass
class Particle:
    id: int
    x: float
    y: float
    radius: float
    property: float = 0.0
    vx: float = 0.0
    vy: float = 0.0