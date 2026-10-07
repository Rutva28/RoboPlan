"""
RoboPlan - Module E
Expert System

Features:
1. 18 rule-based diagnostic rules
2. Forward chaining
3. Explanation trace
4. Knowledge acquisition
5. JSON-based rule storage
6. Interactive CLI
"""

import json
import os


RULE_FILE = os.path.join(
    os.path.dirname(__file__),
    "rules.json"
)


# ============================================================
# RULE MANAGEMENT
# ============================================================

def load_rules():
    """Load expert rules from JSON."""

    with open(
        RULE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_rules(rules):
    """Save rules back to JSON."""

    with open(
        RULE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            rules,
            file,
            indent=4
        )


# ============================================================
# FORWARD CHAINING
# ============================================================

def forward_chain(facts, rules):
    """
    Apply rules repeatedly.

    A rule fires when all its conditions
    are present in the current facts.
    """

    facts = set(facts)

    fired_rules = []

    diagnoses = []

    changed = True

    while changed:

        changed = False

        for rule in rules:

            rule_id = rule["id"]

            conditions = set(
                rule["conditions"]
            )

            # Avoid firing the same rule twice.
            if rule_id in fired_rules:
                continue

            # Check whether all conditions
            # are available.
            if conditions.issubset(facts):

                fired_rules.append(
                    rule_id
                )

                diagnosis = rule[
                    "diagnosis"
                ]

                diagnoses.append(
                    diagnosis
                )

                print(
                    f"\n[{rule_id}] RULE FIRED"
                )

                print(
                    "Conditions: "
                    + ", ".join(
                        rule["conditions"]
                    )
                )

                print(
                    "Diagnosis: "
                    + diagnosis
                )

                print(
                    "Reason: "
                    + rule["explanation"]
                )

                changed = True

    return diagnoses, fired_rules


# ============================================================
# SENSOR VALUE -> FACT CONVERSION
# ============================================================

def sensor_to_facts(
    weight,
    crack,
    tilt,
    motor_current=0,
    wheel_slip=False,
    battery=100,
    temperature=25,
    obstacle=False
):
    """
    Convert numeric sensor values into
    symbolic expert-system facts.
    """

    facts = set()

    # Weight
    if weight >= 70:
        facts.add("weight_high")

    if weight <= 20:
        facts.add("weight_low")

    # Crack severity
    if crack >= 60:
        facts.add("crack_high")

    # Tilt
    if tilt >= 1:
        facts.add("tilt_high")

    # Motor current
    if motor_current >= 70:
        facts.add("motor_current_high")

    # Wheel
    if wheel_slip:
        facts.add("wheel_slip")

    # Battery
    if battery <= 25:
        facts.add("battery_low")

    # Temperature
    if temperature >= 70:
        facts.add("temperature_high")

    # Obstacle
    if obstacle:
        facts.add("obstacle_detected")

    return facts


# ============================================================
# DIAGNOSIS
# ============================================================

def diagnose(facts):
    """
    Run the expert system.
    """

    rules = load_rules()

    print("\n")
    print("=" * 60)
    print("ROBO PLAN - EXPERT ADVISOR")
    print("=" * 60)

    print("\nInitial Facts:")

    if facts:

        for fact in sorted(facts):
            print(f"  - {fact}")

    else:
        print("  No abnormal facts detected.")

    print("\n")
    print("-" * 60)
    print("EXPLANATION TRACE")
    print("-" * 60)

    diagnoses, fired_rules = forward_chain(
        facts,
        rules
    )

    print("\n")
    print("-" * 60)
    print("FINAL DIAGNOSIS")
    print("-" * 60)

    if diagnoses:

        # Remove duplicate diagnoses
        # while preserving order.
        unique_diagnoses = list(
            dict.fromkeys(diagnoses)
        )

        for number, diagnosis in enumerate(
            unique_diagnoses,
            start=1
        ):

            print(
                f"{number}. {diagnosis}"
            )

    else:

        print(
            "No known problem detected."
        )

    print(
        f"\nRules fired: "
        f"{len(fired_rules)}"
    )

    if fired_rules:

        print(
            "Rule IDs: "
            + ", ".join(fired_rules)
        )

    return diagnoses, fired_rules


# ============================================================
# KNOWLEDGE ACQUISITION
# ============================================================

def add_rule_interactive():
    """
    Add a new expert rule from the CLI.
    """

    print("\n")
    print("=" * 60)
    print("KNOWLEDGE ACQUISITION")
    print("=" * 60)

    rules = load_rules()

    existing_numbers = []

    for rule in rules:

        rule_id = rule["id"]

        if rule_id.startswith("R"):

            try:
                existing_numbers.append(
                    int(rule_id[1:])
                )
            except ValueError:
                pass

    next_number = (
        max(existing_numbers) + 1
        if existing_numbers
        else 1
    )

    rule_id = f"R{next_number:02d}"

    print(
        f"\nNew rule ID: {rule_id}"
    )

    condition_text = input(
        "Enter conditions separated by commas: "
    ).strip()

    diagnosis = input(
        "Enter diagnosis: "
    ).strip()

    explanation = input(
        "Enter explanation: "
    ).strip()

    conditions = [
        item.strip()
        for item in condition_text.split(",")
        if item.strip()
    ]

    if not conditions:
        print(
            "\nERROR: At least one condition "
            "is required."
        )
        return

    if not diagnosis:
        print(
            "\nERROR: Diagnosis is required."
        )
        return

    new_rule = {
        "id": rule_id,
        "conditions": conditions,
        "diagnosis": diagnosis,
        "explanation": explanation
    }

    rules.append(new_rule)

    save_rules(rules)

    print("\nNew rule added successfully!")

    print(
        f"Rule ID: {rule_id}"
    )

    print(
        f"Conditions: {conditions}"
    )

    print(
        f"Diagnosis: {diagnosis}"
    )


# ============================================================
# DEMO
# ============================================================

def demo():

    print("\n")
    print("#" * 60)
    print("ROBOPLAN - MODULE E")
    print("RULE-BASED EXPERT SYSTEM")
    print("#" * 60)

    # Example warehouse situation.
    facts = sensor_to_facts(
        weight=85,
        crack=75,
        tilt=1,
        motor_current=80,
        wheel_slip=True,
        battery=20,
        temperature=75,
        obstacle=True
    )

    diagnose(facts)


# ============================================================
# INTERACTIVE MENU
# ============================================================

def interactive_menu():

    while True:

        print("\n")
        print("=" * 60)
        print("ROBO PLAN EXPERT ADVISOR")
        print("=" * 60)

        print("""
1. Run sample diagnosis
2. Enter sensor values
3. Add a new rule
4. Show all rules
5. Exit
""")

        choice = input(
            "Enter your choice: "
        ).strip()

        # ----------------------------------------------------
        # OPTION 1
        # ----------------------------------------------------

        if choice == "1":

            demo()

        # ----------------------------------------------------
        # OPTION 2
        # ----------------------------------------------------

        elif choice == "2":

            try:

                weight = float(
                    input(
                        "Weight deviation: "
                    )
                )

                crack = float(
                    input(
                        "Crack severity: "
                    )
                )

                tilt = float(
                    input(
                        "Tilt value (0/1): "
                    )
                )

                motor_current = float(
                    input(
                        "Motor current: "
                    )
                )

                wheel_slip = input(
                    "Wheel slip? (y/n): "
                ).lower() == "y"

                battery = float(
                    input(
                        "Battery percentage: "
                    )
                )

                temperature = float(
                    input(
                        "Temperature: "
                    )
                )

                obstacle = input(
                    "Obstacle detected? (y/n): "
                ).lower() == "y"

                facts = sensor_to_facts(
                    weight=weight,
                    crack=crack,
                    tilt=tilt,
                    motor_current=motor_current,
                    wheel_slip=wheel_slip,
                    battery=battery,
                    temperature=temperature,
                    obstacle=obstacle
                )

                diagnose(facts)

            except ValueError:

                print(
                    "\nERROR: Please enter "
                    "valid numeric values."
                )

        # ----------------------------------------------------
        # OPTION 3
        # ----------------------------------------------------

        elif choice == "3":

            add_rule_interactive()

        # ----------------------------------------------------
        # OPTION 4
        # ----------------------------------------------------

        elif choice == "4":

            rules = load_rules()

            print("\n")
            print("=" * 60)
            print("CURRENT KNOWLEDGE BASE")
            print("=" * 60)

            for rule in rules:

                print(
                    f"\n{rule['id']}:"
                )

                print(
                    "  IF "
                    + " AND ".join(
                        rule["conditions"]
                    )
                )

                print(
                    "  THEN "
                    + rule["diagnosis"]
                )

                print(
                    "  WHY "
                    + rule["explanation"]
                )

            print(
                f"\nTotal rules: {len(rules)}"
            )

        # ----------------------------------------------------
        # OPTION 5
        # ----------------------------------------------------

        elif choice == "5":

            print(
                "\nExiting RoboPlan Expert Advisor."
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1-5."
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    interactive_menu()