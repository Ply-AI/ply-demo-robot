# Demo: replace the camera, surface the consequences

## The story

“This is the S2 hospital scrubber. Its repository and risk assessment describe the
same robot. An engineer replaces the front camera with a navigation LiDAR. The
change looks small in GitHub. Ply helps the reviewer find the assumptions and
evidence that need another look.”

The repository starts at the RGB-camera baseline. No replacement adapter or
pre-applied LiDAR change is included.

## Before presenting

1. Commit and push this baseline to the demo repository when ready. Include the
   original assessment export, which was originally an untracked file.
2. Connect the repository using the integration’s actual setup flow. This project
   does not provide a webhook, GitHub App, or fabricated integration service.
3. Load the supplied assessment through the integration’s supported workflow.
   Confirm the system is **Ply Scrub S2** and the camera is **PER-01**.
4. Run `python3 tools/check.py` and `python3 -m scrub_s2`.
5. Keep the camera description and HS-01 / HS-02 / HS-18 available for comparison.

The base revision should still contain the original camera. Create the proposed
change on a separate branch when you perform the demo. Do not merge it before
showing the integration’s review flow.

## A concrete change brief

Use this as the engineering request during the demo:

> Replace PER-01, the front RGB camera, with a non-safety-rated navigation LiDAR
> connected to CTL-01. Add a mock range-sensor adapter and update the configuration,
> component inventory and relevant tests. Make the loss of camera-based person
> detection and RGB video explicit. Inhibit remote driving while no reviewed
> replacement operator view is available; do not treat range data as RGB video.
> Keep the existing PER-02 safety scanner, safety input wiring, CTL-02 firmware
> and CTL-04 wireless hardware unchanged. Update the design documentation and
> identify assessment review candidates without automatically editing or
> approving the supplied risk assessment.

The new navigation LiDAR’s model, optical properties, coverage and interface are
deliberately unspecified. Choose illustrative values during the change, label
them as assumptions, and make them reviewable. Do not infer that any new LiDAR
has person recognition, equivalent coverage or a safety rating.

## Files that make a useful pull request

| File | Change to discuss |
| :--- | :--- |
| [`config/robot.json`](../config/robot.json) | PER-01 type, geometry, outputs and video dependencies |
| [`scrub_s2/perception.py`](../scrub_s2/perception.py) | Replace camera-derived semantics with a range-data adapter |
| [`scrub_s2/controller.py`](../scrub_s2/controller.py) | Decide how autonomy behaves without person classification |
| [`scrub_s2/teleoperation.py`](../scrub_s2/teleoperation.py) | Keep remote movement inhibited without an operator view |
| [`hardware/bom.csv`](../hardware/bom.csv) | Changed PER-01 description, with an explicit relationship to its prior assessment identity |
| [`fixtures/scenarios.json`](../fixtures/scenarios.json) and [`tests/`](../tests/) | Representative range inputs, lost capabilities, preserved protective stops |
| [`docs/architecture.md`](architecture.md) | Explain the new behavior and outstanding review work |

The BOM currently mirrors the assessment. After the proposed hardware change,
update its description and the baseline-specific inventory test deliberately;
preserve the relationship to the original component UUID so reviewers can trace
what changed. Do not rewrite the source assessment merely to make a test pass.

## What the reviewer should notice

| Review candidate | Why the camera replacement matters |
| :--- | :--- |
| **HS-01** · pedestrian collision | The current design relies on camera-driven early slowdown. Revisit the new perception behavior and its evidence. |
| **HS-02** · children and mobility aids | The source credits recognition of children, wheelchairs and walking aids. A range scan does not establish equivalent performance. |
| **HS-18** · remote recovery collision | The remote operator loses RGB video and the person overlay. A substitute view and its latency behavior need explicit design and review. |
| Related effects | Consider changed blind spots, mounting, laser characteristics and stationary-obstacle consequences such as HS-03. These are questions, not automatically established hazards. |

The existing safety LiDAR continues to exist. The camera replacement does not
automatically require a safety PLC program change when it remains a non-safety
input to CTL-01. The resulting robot behavior and assessment assumptions still
need review. Distinguishing these two points is a useful part of the demo.

The exported camera UUID is `bbcf188b-8f12-491b-9e7d-5db4b8660d9d`.
Run `python3 -m scrub_s2 --trace PER-01` to resolve its direct hazard links from
the original export. This helper uses explicit references only; it is not the
GitHub integration’s impact-analysis engine.

## A short presentation sequence

1. **Show the robot.** Open the README hero and point out the two separate sensors.
2. **Show the baseline.** Run the `person-ahead` and `remote-recovery` scenarios.
3. **Show the change.** Open the camera-to-LiDAR pull request and its focused diff.
4. **Show the integration.** Inspect the actual detected component and hazard
   connections. Present the rows above as review expectations, not guaranteed output.
5. **Show the decision.** Explain what evidence needs revisiting and why code checks
   alone cannot approve the changed robot.

Existing pending items (HS-05, HS-09, HS-13 and HS-19) predate this change. Keep
them distinct from new review work. The site release is still pending.
