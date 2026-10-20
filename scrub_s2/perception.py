"""PER-01 → CTL-01: mock camera detections and video capability.

Detections are supplied by fixtures, not computer vision. This module is the
primary implementation seam for the future RGB-camera replacement.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PerceptionResult:
    person_nearby: bool
    rgb_video_available: bool
    source_ref: str


class RgbCamera:
    def __init__(self, config):
        if config["type"] != "rgb_camera":
            raise ValueError("Only the RGB baseline is implemented. Add a sensor adapter for a replacement.")
        self.config = config

    def observe(self, frame):
        available = frame.get("camera_available", True)
        distance = frame.get("person_distance_m")
        person_nearby = (available and distance is not None
                         and 0 <= distance <= self.config["person_slowdown_distance_m"])
        return PerceptionResult(
            person_nearby=person_nearby,
            rgb_video_available=available and "rgb_video" in self.config["outputs"],
            source_ref=self.config["component_ref"],
        )
