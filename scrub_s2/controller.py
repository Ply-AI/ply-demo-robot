"""Compute one illustrative command from fixture inputs; issue no hardware I/O."""

import math

from .perception import RgbCamera
from .safety import stop_reasons
from .teleoperation import view_inhibit_reasons


def simulate(config, frame):
    mode = frame["mode"]
    if mode not in config["speed_limits_mps"]:
        raise ValueError(f"Unknown mode: {mode}")
    requested = frame.get("requested_speed_mps", config["speed_limits_mps"][mode])
    if not isinstance(requested, (int, float)) or not math.isfinite(requested) or requested < 0:
        raise ValueError("Requested speed must be a finite, non-negative number")
    perception = RgbCamera(config["perception"]).observe(frame)
    reasons = stop_reasons(frame, config["teleoperation"])
    reasons += view_inhibit_reasons(frame, perception, config["teleoperation"])
    # A demo design choice: missing camera input holds autonomous movement.
    # This is not a validated safeguard claimed by the supplied assessment.
    if mode == "autonomous" and not frame.get("camera_available", True):
        reasons.append("PER-01 camera unavailable; autonomous demo held")
    speed = min(requested, config["speed_limits_mps"][mode])
    if perception.person_nearby:
        speed = min(speed, config["perception"]["person_slowdown_speed_mps"])
    if reasons:
        speed = 0.0
    moving = speed > 0
    return {
        "scenario": frame["name"],
        "mode": mode,
        "state": "STOPPED" if reasons else ("SLOWDOWN" if perception.person_nearby and moving
                                           else "MOVING" if moving else "IDLE"),
        "speed_mps": speed,
        "brushes_rpm": config["cleaning"]["brush_speed_rpm"]
        if moving and mode == "autonomous" and frame.get("cleaning", False)
        and not frame.get("deck_lifted", False) else 0,
        "brakes_engaged": not moving,
        "rgb_video_available": perception.rgb_video_available,
        "person_slowdown": perception.person_nearby,
        "stop_reasons": reasons,
        "simulated": True,
    }
