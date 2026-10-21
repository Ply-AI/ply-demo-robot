"""CTL-04 → CTL-01/CTL-02: over-the-air software updates over the hospital Wi-Fi.

Manifests and payloads are supplied by fixtures; nothing is downloaded or flashed.
"""

import hashlib


def pending_updates(config, installed, manifest):
    """Return the manifest entries newer than what is installed, per target."""
    ota = config["ota"]
    if not ota["enabled"]:
        return []
    return [entry for entry in manifest["updates"]
            if entry["target"] in ota["targets"]
            and _version(entry["version"]) > _version(installed[entry["target"]])]


def can_install(config, robot_state):
    """Updates install only while the robot is docked and idle."""
    return all(robot_state.get(condition, False) for condition in config["ota"]["install_requires"])


def verify(entry, payload):
    """Reject a payload whose SHA-256 does not match the manifest."""
    return hashlib.sha256(payload).hexdigest() == entry["sha256"]


def apply(config, installed, entry, payload, robot_state):
    if not can_install(config, robot_state):
        raise RuntimeError("Robot must be docked and idle to install updates")
    if not verify(entry, payload):
        raise ValueError(f"Checksum mismatch for {entry['target']} {entry['version']}")
    return {**installed, entry["target"]: entry["version"]}


def _version(text):
    return tuple(int(part) for part in text.split("."))
