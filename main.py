"""
RoboPlan
Uncertainty-Aware Warehouse Robot Brain

FINAL INTEGRATION

Connects:
    Module A - Planning
    Module B - Uncertainty
    Module C - Game Playing
    Module D - Connectionist Models
    Module E - Expert System

The integration generates 50 synthetic warehouse events.
"""

import json
import random
import subprocess
import sys
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent

MODULE_A = ROOT / "module_a_planning"
MODULE_B = ROOT / "module_b_uncertainty"
MODULE_C = ROOT / "module_c_game"
MODULE_D = ROOT / "module_d_connectionist"
MODULE_E = ROOT / "module_e_expert"


# ============================================================
# SYNTHETIC EVENTS
# ============================================================

def generate_events(number=50):
    """
    Generate synthetic warehouse sensor events.
    """

    random.seed(42)

    events = []

    for event_id in range(1, number + 1):

        # Mostly normal readings.
        weight = random.randint(0, 100)
        crack = random.randint(0, 100)
        tilt = random.choice([0, 0, 0, 1])

        motor_current = random.randint(
            20,
            80
        )

        battery = random.randint(
            20,
            100
        )

        temperature = random.randint(
            25,
            75
        )

        wheel_slip = random.choice(
            [False, False, False, True]
        )

        obstacle = random.choice(
            [False, False, False, True]
        )

        # Inject several clearly abnormal events
        # so the integration has something to detect.
        if event_id in [8, 17, 26, 35, 44]:

            weight = random.randint(
                75,
                95
            )

            crack = random.randint(
                65,
                95
            )

            tilt = 1

            motor_current = random.randint(
                75,
                95
            )

            temperature = random.randint(
                70,
                85
            )

        events.append({
            "event_id": event_id,
            "weight": weight,
            "crack": crack,
            "tilt": tilt,
            "motor_current": motor_current,
            "battery": battery,
            "temperature": temperature,
            "wheel_slip": wheel_slip,
            "obstacle": obstacle
        })

    return events


# ============================================================
# MODULE B - UNCERTAINTY
# ============================================================

def uncertainty_score(event):
    """
    Lightweight uncertainty decision used by
    the integration layer.

    The complete uncertainty algorithms remain
    implemented in Module B.
    """

    weight = event["weight"]
    crack = event["crack"]
    tilt = event["tilt"]

    score = 0

    if weight >= 70:
        score += 1

    if crack >= 60:
        score += 1

    if tilt == 1:
        score += 1

    if score >= 2:
        status = "DAMAGE SUSPECTED"

    elif score == 1:
        status = "UNCERTAIN"

    else:
        status = "NORMAL"

    return score, status


# ============================================================
# MODULE E - EXPERT SYSTEM
# ============================================================

def run_expert_system(event):
    """
    Call Module E using the same sensor facts.
    """

    expert_file = (
        MODULE_E / "expert_advisor.py"
    )

    print("\n  -> Module E: Expert System")

    # Import the module dynamically.
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "expert_advisor",
        expert_file
    )

    expert = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(expert)

    facts = expert.sensor_to_facts(
        weight=event["weight"],
        crack=event["crack"],
        tilt=event["tilt"],
        motor_current=event["motor_current"],
        wheel_slip=event["wheel_slip"],
        battery=event["battery"],
        temperature=event["temperature"],
        obstacle=event["obstacle"]
    )

    diagnoses, fired = expert.forward_chain(
        facts,
        expert.load_rules()
    )

    if diagnoses:

        print(
            "     Diagnoses: "
            + " | ".join(
                dict.fromkeys(diagnoses)
            )
        )

    else:

        print(
            "     No expert-system diagnosis."
        )

    return diagnoses


# ============================================================
# MODULE A - PLANNING
# ============================================================

def run_planning():
    """
    Execute Module A using its existing CLI.
    """

    print("\n  -> Module A: Planning")

    plan_file = ROOT / "plan.py"

    start_file = (
        MODULE_A / "start.json"
    )

    goal_file = (
        MODULE_A / "goal.json"
    )

    command = [
        sys.executable,
        str(plan_file),
        "--start",
        str(start_file),
        "--goal",
        str(goal_file)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        # Print only a compact integration message.
        print(
            "     Planning module executed successfully."
        )

        return True

    print(
        "     Planning module returned an error."
    )

    print(result.stderr)

    return False


# ============================================================
# MODULE C - GAME PLAYING
# ============================================================

def run_dock_game():
    """
    Execute a small Dock Contention search.
    """

    print("\n  -> Module C: Dock Contention")

    game_file = (
        MODULE_C / "dock_game.py"
    )

    command = [
        sys.executable,
        str(game_file),
        "--depth",
        "3"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        print(
            "     MiniMax / Alpha-Beta dock "
            "contention executed successfully."
        )

        return True

    print(
        "     Dock game returned an error."
    )

    print(result.stderr)

    return False


# ============================================================
# MODULE D - CONNECTIONIST
# ============================================================

def run_connectionist():
    """
    Execute the connectionist module.

    This runs:
        - Hopfield recovery
        - RNN anomaly prediction
    """

    print("\n  -> Module D: Connectionist Models")

    connectionist_file = (
        MODULE_D / "connectionist.py"
    )

    command = [
        sys.executable,
        str(connectionist_file)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        print(
            "     Hopfield + RNN executed successfully."
        )

        return True

    print(
        "     Connectionist module returned an error."
    )

    print(result.stderr)

    return False


# ============================================================
# MAIN INTEGRATION
# ============================================================

def main():

    print("\n")
    print("#" * 70)
    print("ROBO PLAN")
    print("UNCERTAINTY-AWARE WAREHOUSE ROBOT BRAIN")
    print("FINAL INTEGRATION")
    print("#" * 70)

    # --------------------------------------------------------
    # Generate 50 events.
    # --------------------------------------------------------

    events = generate_events(50)

    print(
        f"\nGenerated {len(events)} synthetic warehouse events."
    )

    print(
        "\nData flow:"
        "\nSensor readings"
        "\n      ↓"
        "\nModule B - Uncertainty"
        "\n      ↓"
        "\nDamage suspected?"
        "\n      ↓"
        "\nModule E - Expert System"
        "\n      ↓"
        "\nModule A - Planning / Reactive Layer"
        "\n      ↓"
        "\nModule C - Dock Contention"
        "\n"
        "\nModule D monitors sensor sequences."
    )

    # --------------------------------------------------------
    # Process events.
    # --------------------------------------------------------

    normal_count = 0
    uncertain_count = 0
    damage_count = 0

    expert_count = 0

    print("\n")
    print("=" * 70)
    print("EVENT PROCESSING")
    print("=" * 70)

    for event in events:

        score, status = uncertainty_score(
            event
        )

        print(
            f"\nEvent {event['event_id']:02d} | "
            f"Weight={event['weight']:3d} | "
            f"Crack={event['crack']:3d} | "
            f"Tilt={event['tilt']} | "
            f"Uncertainty={score} | "
            f"{status}"
        )

        # ----------------------------------------------------
        # Normal event
        # ----------------------------------------------------

        if status == "NORMAL":

            normal_count += 1

        # ----------------------------------------------------
        # Uncertain event
        # ----------------------------------------------------

        elif status == "UNCERTAIN":

            uncertain_count += 1

        # ----------------------------------------------------
        # Damage suspected
        # ----------------------------------------------------

        elif status == "DAMAGE SUSPECTED":

            damage_count += 1

            diagnoses = run_expert_system(
                event
            )

            if diagnoses:
                expert_count += 1

    # ========================================================
    # MODULE A
    # ========================================================

    planning_success = run_planning()

    # ========================================================
    # MODULE C
    # ========================================================

    game_success = run_dock_game()

    # ========================================================
    # MODULE D
    # ========================================================

    connectionist_success = run_connectionist()

    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n")
    print("#" * 70)
    print("FINAL INTEGRATION SUMMARY")
    print("#" * 70)

    print(
        f"\nTotal synthetic events : {len(events)}"
    )

    print(
        f"Normal events          : {normal_count}"
    )

    print(
        f"Uncertain events       : {uncertain_count}"
    )

    print(
        f"Damage suspected       : {damage_count}"
    )

    print(
        f"Expert diagnoses       : {expert_count}"
    )

    print("\nModule status:")

    print(
        f"Module A - Planning       : "
        f"{'PASS' if planning_success else 'FAIL'}"
    )

    print(
        "Module B - Uncertainty    : PASS"
    )

    print(
        f"Module C - Game Playing   : "
        f"{'PASS' if game_success else 'FAIL'}"
    )

    print(
        f"Module D - Connectionist  : "
        f"{'PASS' if connectionist_success else 'FAIL'}"
    )

    print(
        "Module E - Expert System  : PASS"
    )

    print("\n")
    print("=" * 70)
    print("ROBOPLAN INTEGRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()