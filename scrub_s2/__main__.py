import argparse
import json

from .assessment import component_hazards, read_json, summary
from .controller import simulate


def main():
    parser = argparse.ArgumentParser(description="Ply Scrub S2 • software mockup only")
    parser.add_argument("--scenario", default="all", help="Fixture name, or all (default)")
    parser.add_argument("--list", action="store_true", help="List available fixture snapshots")
    parser.add_argument("--assessment", action="store_true", help="Summarize the supplied assessment")
    parser.add_argument("--trace", metavar="COMPONENT", help="Find directly linked hazards, e.g. PER-01")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()
    fixtures = read_json("fixtures/scenarios.json")
    if args.list:
        print("\n".join(frame["name"] for frame in fixtures))
        return
    if args.assessment or args.trace:
        try:
            result = (component_hazards(read_json("RA-S2-WGH-01.json")["assessment"], args.trace)
                      if args.trace else summary())
        except ValueError as error:
            parser.error(str(error))
        print(json.dumps(result, indent=2))
        return
    selected = [f for f in fixtures if args.scenario in ("all", f["name"])]
    if not selected:
        parser.error("Unknown scenario. Use --list to see available snapshots.")
    config = read_json("config/robot.json")
    results = [simulate(config, frame) for frame in selected]
    if args.json:
        print(json.dumps(results, indent=2))
        return
    print("\n  PLY / SCRUB S2    ·    HOSPITAL VARIANT H    ·    SIMULATION ONLY\n")
    print(f"  {'SCENARIO':<24} {'STATE':<10} {'SPEED':>8} {'BRUSHES':>10}")
    print("  " + "─" * 57)
    for result in results:
        print(f"  {result['scenario']:<24} {result['state']:<10} "
              f"{result['speed_mps']:>5.1f} m/s {result['brushes_rpm']:>6} rpm")
        for reason in result["stop_reasons"]:
            print(f"    ↳ {reason}")
    print("\n  PER-01 RGB camera → CTL-01 main computer")
    print("  PER-02 safety LiDAR → CTL-02 safety PLC (separate path)\n")


if __name__ == "__main__":
    main()
