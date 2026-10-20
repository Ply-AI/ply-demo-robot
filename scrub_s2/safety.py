"""CTL-02/CTL-03: simplified interlock snapshots, never a safety controller.

PER-01 is deliberately absent from the protective-input list. Distances,
braking dynamics, dual-channel diagnostics and restart latching are not modeled.
"""


PROTECTIVE_INPUTS = {
    "e_stop": "CTL-03.1 emergency stop",
    "protective_field": "PER-02 safety LiDAR field occupied",
    "bumper": "PER-04 bumper contact",
    "cliff": "PER-05 drop detected",
}


def stop_reasons(frame, teleoperation_config):
    reasons = [label for signal, label in PROTECTIVE_INPUTS.items() if frame.get(signal, False)]
    if frame["mode"] == "teleoperation":
        if frame.get("heartbeat_age_ms", 0) >= teleoperation_config["heartbeat_timeout_ms"]:
            reasons.append("SF-09 remote heartbeat timeout")
    if frame["mode"] == "setup" and not frame.get("hold_to_run", False):
        reasons.append("Setup hold-to-run released")
    return reasons
