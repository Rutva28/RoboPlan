import json
import random
import copy
import argparse


# ============================================================
# BLOCKS WORLD STATE
# ============================================================

class BlocksWorld:
    def __init__(self, state):
        self.on = state["on"]
        self.clear = set(state.get("clear", []))

    def copy(self):
        return BlocksWorld({
            "on": copy.deepcopy(self.on),
            "clear": list(self.clear)
        })

    def print_state(self):
        print("\nCurrent State:")
        for block, location in self.on.items():
            print(f"  {block} -> {location}")

        print("Clear blocks:", sorted(self.clear))


# ============================================================
# BASIC ACTIONS
# ============================================================

def move_block(state, block, destination):
    """
    Move a block onto another block or onto the table.
    """

    old_location = state.on.get(block)

    # Block must be clear before moving
    if block not in state.clear:
        return False

    # Destination block must be clear
    if destination != "table":
        if destination not in state.clear:
            return False

    # Remove block from old support
    if old_location != "table":
        state.clear.add(old_location)

    # Destination is no longer clear
    if destination != "table":
        state.clear.discard(destination)

    state.on[block] = destination

    # Moving block itself becomes clear
    state.clear.add(block)

    return True


# ============================================================
# GOAL CHECKING
# ============================================================

def goal_reached(state, goal):
    for block, destination in goal["on"].items():
        if state.on.get(block) != destination:
            return False

    return True


# ============================================================
# GOAL STACK PLANNER
# ============================================================

def goal_stack_plan(start_state, goal):
    """
    Simplified Goal Stack Planning for Blocks World.

    The planner repeatedly moves blocks toward their goal positions.
    """

    state = start_state.copy()
    plan = []

    max_iterations = 100

    for _ in range(max_iterations):

        if goal_reached(state, goal):
            break

        progress = False

        for block, destination in goal["on"].items():

            if state.on.get(block) == destination:
                continue

            # If block is not clear, move the block above it
            if block not in state.clear:

                above_block = None

                for b, loc in state.on.items():
                    if loc == block:
                        above_block = b
                        break

                if above_block:
                    move = f"UNSTACK({above_block}, {block})"

                    if move_block(state, above_block, "table"):
                        plan.append(move)
                        progress = True
                        break

            # Destination must be clear
            if destination != "table" and destination not in state.clear:

                above_destination = None

                for b, loc in state.on.items():
                    if loc == destination:
                        above_destination = b
                        break

                if above_destination:

                    move = f"UNSTACK({above_destination}, {destination})"

                    if move_block(state, above_destination, "table"):
                        plan.append(move)
                        progress = True
                        break

            # Try desired move
            if block in state.clear:

                if destination == "table":
                    success = move_block(state, block, "table")

                else:
                    success = move_block(state, block, destination)

                if success:

                    if destination == "table":
                        plan.append(f"MOVE({block}, TABLE)")
                    else:
                        plan.append(f"STACK({block}, {destination})")

                    progress = True
                    break

        if not progress:
            break

    return plan, state


# ============================================================
# NONLINEAR / CONSTRAINT-POSTING PLANNER
# ============================================================

def nonlinear_plan(start_state, goal):
    """
    Least-commitment style planner.

    Instead of strictly solving goals in one fixed order,
    it creates dependencies between required stacking operations.
    """

    operations = []

    # Build required relationships
    for block, destination in goal["on"].items():

        if destination == "table":
            operations.append(
                f"MOVE({block}, TABLE)"
            )
        else:
            operations.append(
                f"STACK({block}, {destination})"
            )

    # Bottom-to-top ordering where necessary
    ordered = []

    visited = set()

    def add_dependency(block):

        if block in visited:
            return

        destination = goal["on"].get(block)

        if destination and destination != "table":
            add_dependency(destination)

        ordered.append(block)
        visited.add(block)

    for block in goal["on"]:
        add_dependency(block)

    plan = []

    for block in ordered:

        destination = goal["on"][block]

        if destination == "table":
            plan.append(f"MOVE({block}, TABLE)")
        else:
            plan.append(f"STACK({block}, {destination})")

    return plan


# ============================================================
# HIERARCHICAL PLANNING
# ============================================================

def load_pallet(pallet_name, blocks):
    """
    High-level operator:

        LoadPallet(P)

    expands into primitive stack actions.
    """

    print(f"\nHIGH LEVEL ACTION: LoadPallet({pallet_name})")

    primitive_actions = []

    for i in range(len(blocks) - 1):

        upper = blocks[i]
        lower = blocks[i + 1]

        primitive_actions.append(
            f"STACK({upper}, {lower})"
        )

    return primitive_actions


# ============================================================
# REACTIVE PLANNING
# ============================================================

def reactive_execution(plan):
    """
    Execute the current plan.

    A random disturbance may knock a box onto the table.
    The robot reacts without restarting the entire planner.
    """

    print("\n========== REACTIVE EXECUTION ==========")

    executed = []

    for step_number, action in enumerate(plan, start=1):

        print(f"\nStep {step_number}: {action}")

        # Simulated random disturbance
        disturbance = random.random() < 0.15

        if disturbance:

            print("!!! DISTURBANCE DETECTED !!!")
            print("A box was knocked over.")
            print("Reactive layer intervening...")

            recovery = "RECOVER_BOX_AND_CONTINUE"

            print(f"Reactive action: {recovery}")

            executed.append(recovery)

        print("Action completed.")
        executed.append(action)

    print("\nReactive execution finished.")

    return executed


# ============================================================
# DISPLAY PLAN
# ============================================================

def print_plan(title, plan):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    if not plan:
        print("No actions required.")
        return

    for i, action in enumerate(plan, start=1):
        print(f"{i:02d}. {action}")

    print(f"\nTotal actions: {len(plan)}")


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="RoboPlan - Blocks World Planner"
    )

    parser.add_argument(
        "--start",
        default="start.json",
        help="Start state JSON file"
    )

    parser.add_argument(
        "--goal",
        default="goal.json",
        help="Goal state JSON file"
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # LOAD FILES
    # --------------------------------------------------------

    with open(args.start, "r") as f:
        start_data = json.load(f)

    with open(args.goal, "r") as f:
        goal_data = json.load(f)

    start_state = BlocksWorld(start_data)

    # --------------------------------------------------------
    # DISPLAY INITIAL STATE
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("ROBO PLAN - MODULE A")
    print("UNCERTAINTY-AWARE WAREHOUSE ROBOT")
    print("=" * 60)

    start_state.print_state()

    # --------------------------------------------------------
    # GOAL STACK PLANNING
    # --------------------------------------------------------

    goal_stack, final_state = goal_stack_plan(
        start_state,
        goal_data
    )

    print_plan(
        "GOAL STACK PLANNING",
        goal_stack
    )

    # --------------------------------------------------------
    # NONLINEAR PLANNING
    # --------------------------------------------------------

    nonlinear = nonlinear_plan(
        start_state,
        goal_data
    )

    print_plan(
        "NONLINEAR / CONSTRAINT-POSTING PLANNING",
        nonlinear
    )

    # --------------------------------------------------------
    # HIERARCHICAL PLANNING
    # --------------------------------------------------------

    hierarchical = load_pallet(
        "P",
        ["G", "F", "E", "D", "B", "A", "C"]
    )

    print_plan(
        "HIERARCHICAL PLAN EXPANSION",
        hierarchical
    )

    # --------------------------------------------------------
    # REACTIVE EXECUTION
    # --------------------------------------------------------

    reactive_execution(goal_stack)

    # --------------------------------------------------------
    # FINAL CHECK
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("MODULE A COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()