"""CTL-04 uses PER-01 RGB video; a range scan is not a video replacement."""


def view_inhibit_reasons(frame, perception, config):
    if frame["mode"] != "teleoperation":
        return []
    if config["requires_rgb_video"] and not perception.rgb_video_available:
        return ["PER-01 RGB view unavailable; remote driving inhibited"]
    if frame.get("video_latency_ms", 0) > config["max_video_latency_ms"]:
        return ["PER-01 video latency exceeds 300 ms"]
    return []


def pick_network(in_range, config):
    """The first configured network in range, so the link prefers the earlier ones."""
    return next((n for n in config["networks"] if n in in_range), None)
