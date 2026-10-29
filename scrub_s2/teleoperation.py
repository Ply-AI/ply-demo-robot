"""CTL-04 streams the PER-01 operator view: RGB video, or a point-cloud render."""


def view_inhibit_reasons(frame, perception, config):
    if frame["mode"] != "teleoperation":
        return []
    if not perception.view_available or (config["requires_rgb_video"] and not perception.rgb_video_available):
        return ["PER-01 operator view unavailable; remote driving inhibited"]
    if frame.get("video_latency_ms", 0) > config["max_video_latency_ms"]:
        return ["PER-01 video latency exceeds 300 ms"]
    return []
