"""Brake controller: when the electromagnetic brakes clamp after the robot stops."""


def brakes_engaged(moving, stop_reasons, frame, config):
    """Clamp at once on a stop with a reason; after a normal stop, wait engage_delay_ms so the motors settle first."""
    if moving:
        return False
    if stop_reasons:
        return True
    return frame.get("stationary_ms", config["engage_delay_ms"]) >= config["engage_delay_ms"]
