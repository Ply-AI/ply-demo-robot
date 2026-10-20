# Assessment map

Source: [`RA-S2-WGH-01.json`](../RA-S2-WGH-01.json). This index preserves the supplied decisions; it does not re-assess risk.

## Hazard inventory

| Task | Hazard | Event / harm | Source review |
| :--- | :--- | :--- | :--- |
| T01 | HS-01 | The robot drives into a pedestrian crossing its path in the corridor: bruising or a fall, worse for frail patients. | ACCEPT |
| T01 | HS-02 | A child, or a person in a wheelchair or with a walking frame, is not detected because they are below or between the LiDAR beams, and is struck by the robot. | ACCEPT |
| T01 | HS-03 | After a protective stop, the robot stands in a busy corridor and a visitor walks into it or trips over the squeegee. | ACCEPT |
| T01 | HS-04 | The robot drives off the atrium mezzanine edge or down the stairs and falls onto people below: serious or fatal injury. | ACCEPT |
| T01 | HS-05 | Other: during a fire alarm the robot stops in the corridor or in a fire door opening and delays evacuation, or keeps a fire door from closing. | PENDING |
| T02 | HS-06 | A visitor slips on the wet floor behind the robot and falls: fractures are possible for elderly patients. | ACCEPT |
| T02 | HS-07 | A child's fingers or loose clothing are drawn under the splash skirt into the rotating brushes. | ACCEPT |
| T02 | HS-08 | Cleaning solution sprays from the brush deck onto a passer-by's skin or eyes: irritation. | ACCEPT |
| T03 | HS-09 | Detergent concentrate splashes into the cleaner's eyes while filling the solution tank. | PENDING |
| T03 | HS-10 | The cleaner strains their back lifting a full 20 L container to the fill port. | ACCEPT |
| T04 | HS-11 | Thermal runaway of the battery pack while charging: fire and toxic smoke in the service corridor, spreading to the public corridor. | ACCEPT |
| T04 | HS-12 | A child touches the docking station's charging plates while no robot is docked. | ACCEPT |
| T04 | HS-13 | A person's foot or leg is trapped between the robot and the wall while it reverses onto the dock. | PENDING |
| T05 | HS-14 | The robot or its brushes restart while the operator is clearing a blocked brush or pushing the robot: hand or foot injury. | ACCEPT |
| T05 | HS-15 | The operator strains their back pushing the 180 kg robot with the brakes engaged. | ACCEPT |
| T06 | HS-16 | A short circuit while the technician disconnects or inspects the battery pack causes an arc flash or a battery fire: burns. | ACCEPT |
| T06 | HS-17 | The technician cuts a hand on a worn squeegee blade or brush clamp while changing them. | ACCEPT |
| T07 | HS-18 | The remote operator does not see a person beside or behind the robot in the camera view and drives into them. | ACCEPT |
| T07 | HS-19 | The wireless link drops during teleoperation and the robot keeps moving on its last command. | PENDING |
| T09 | HS-20 | The engineer's foot is run over while driving the robot by joystick during mapping. | ACCEPT |

T08 (fixture cleaning) is excluded with justification. T10 (daily pre-use checks) is recorded as having no additional hazards with justification.

## Camera change review

The source links PER-01 directly to HS-01, HS-02 and HS-18 through system-element or safety-function-element references. Membership in those lists does **not** make the RGB camera safety-rated: its component description explicitly says otherwise.

| Hazard | Camera dependency | Evidence named in the source, not supplied here |
| :--- | :--- | :--- |
| HS-01 | Safety LiDAR protective fields scaled to speed stop the robot (STO and brakes) before contact; the bumper stops it on contact. Camera person detection slows the robot to 0.3 m/s near people (early slowdown, not safety-rated). | TR-S2-031 stopping distance test; VAL-S2-012 SF-01/SF-02 validation report; site walk-through 2026-08-26. |
| HS-02 | Camera person detection recognises children, wheelchairs and walking aids and slows the robot to 0.3 m/s within 2 m; the ultrasonic array covers low obstacles; the bumper stops the robot on contact. | VAL-S2-014 person detection test with child-size and wheelchair mannequins (98.6 % detection within 2 m); VAL-S2-012. |
| HS-18 | Teleoperation speed capped at 0.5 m/s; safety LiDAR fields stay active (SF-01); the live front-camera video shows a person-detection overlay; the robot stops if the video lags more than 300 ms. | VAL-S2-018 teleoperation trial (40 runs in the atrium); video latency watchdog test TR-S2-044. |

Direct links are a starting point, not an exhaustive change-impact result. A reviewer should consider the consequences of changed detections, visibility, latency, mounting and loss of the remote video view. HS-03 (a stopped robot becomes an obstacle) is an example of a linked secondary consequence.

## Existing open items

- **HS-05:** Fire-door / evacuation arrangements and site fire-safety sign-off.
- **HS-09:** Refill training and physical validation.
- **HS-13:** Docking rear-bumper re-test.
- **HS-19:** On-site remote-link-loss validation.

Engineering is recorded as `APPROVED`; customer/site release is `PENDING`, with no release date. The mockup does not resolve these items.

## Component cross-reference

[`hardware/bom.csv`](../hardware/bom.csv) contains all 25 components, their original UUIDs and descriptions. [`config/traceability.json`](../config/traceability.json) maps those IDs to source files or inventory-only representations. These are illustrative repository metadata, not a claim about the GitHub integration’s supported file format.
