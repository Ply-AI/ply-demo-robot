"""PER-01 → CTL-01: mock person detections and the operator view.

Detections are supplied by fixtures, not computer vision or point-cloud clustering.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PerceptionResult:
    person_nearby: bool
    rgb_video_available: bool
    view_available: bool
    source_ref: str


class RgbCamera:
    def __init__(self, config):
        self.config = config

    def observe(self, frame):
        available = frame.get("camera_available", True)
        video = available and "rgb_video" in self.config["outputs"]
        return PerceptionResult(_person_nearby(self.config, frame, available), video, video,
                                self.config["component_ref"])


class Lidar3d:
    """Front 3D LiDAR: people from point clusters, operator view rendered from the point cloud."""

    def __init__(self, config):
        self.config = config

    def observe(self, frame):
        available = frame.get("camera_available", True)
        view = available and "point_cloud" in self.config["outputs"]
        return PerceptionResult(_person_nearby(self.config, frame, available), False, view,
                                self.config["component_ref"])


SENSORS = {"rgb_camera": RgbCamera, "lidar_3d": Lidar3d}


def sensor(config):
    if config["type"] not in SENSORS:
        raise ValueError(f"No sensor adapter for {config['type']}")
    return SENSORS[config["type"]](config)


def _person_nearby(config, frame, available):
    distance = frame.get("person_distance_m")
    return (available and distance is not None
            and 0 <= distance <= config["person_slowdown_distance_m"])
