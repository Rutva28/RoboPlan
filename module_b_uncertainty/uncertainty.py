"""
RoboPlan - Module B
Reasoning Under Uncertainty

Methods implemented:
1. Nonmonotonic reasoning
2. Bayes theorem
3. Certainty Factors
4. Bayesian Network
5. Dempster-Shafer Theory
6. Fuzzy Logic
"""

import math
import numpy as np
import pandas as pd


# ============================================================
# SYNTHETIC SENSOR DATA
# ============================================================

TEST_CASES = [
    {
        "case": 1,
        "weight_deviation": 5,
        "crack_severity": 0,
        "tilt": 0
    },
    {
        "case": 2,
        "weight_deviation": 25,
        "crack_severity": 20,
        "tilt": 0
    },
    {
        "case": 3,
        "weight_deviation": 55,
        "crack_severity": 60,
        "tilt": 1
    },
    {
        "case": 4,
        "weight_deviation": 80,
        "crack_severity": 90,
        "tilt": 1
    },
    {
        "case": 5,
        "weight_deviation": 35,
        "crack_severity": 10,
        "tilt": 0
    },
    {
        "case": 6,
        "weight_deviation": 10,
        "crack_severity": 75,
        "tilt": 0
    },
    {
        "case": 7,
        "weight_deviation": 70,
        "crack_severity": 15,
        "tilt": 1
    },
    {
        "case": 8,
        "weight_deviation": 45,
        "crack_severity": 45,
        "tilt": 0
    },
    {
        "case": 9,
        "weight_deviation": 20,
        "crack_severity": 5,
        "tilt": 1
    },
    {
        "case": 10,
        "weight_deviation": 90,
        "crack_severity": 95,
        "tilt": 1
    }
]


# ============================================================
# HELPER
# ============================================================

def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


# ============================================================
# 1. NONMONOTONIC REASONING
# ============================================================

def nonmonotonic_reasoning(weight, crack, tilt):
    """
    Default rule:

        Normally boxes are NOT damaged.

    New evidence can retract this default conclusion.
    """

    # Initial default assumption
    verdict = "Not Damaged"

    # New evidence can defeat the default
    if tilt == 1:
        verdict = "Damaged"

    if crack >= 70:
        verdict = "Damaged"

    if weight >= 70:
        verdict = "Damaged"

    return verdict


def demonstrate_nonmonotonicity():
    print("\n" + "=" * 70)
    print("1. NONMONOTONIC REASONING DEMONSTRATION")
    print("=" * 70)

    print("Initial knowledge:")
    print("  Rule: Normally boxes are undamaged.")
    print("  Conclusion: Not Damaged")

    print("\nNew fact added:")
    print("  Tilt sensor = TRIGGERED")

    print("\nPrevious conclusion is retracted.")
    print("New conclusion: Damaged")


# ============================================================
# 2. BAYESIAN REASONING
# ============================================================

def bayes_posterior(weight, crack, tilt):
    """
    P(Damaged | Evidence)

    We estimate likelihoods from sensor severity.
    """

    prior_damaged = 0.20
    prior_not_damaged = 0.80

    # Weight sensor likelihood
    p_weight_damaged = 0.10 + 0.85 * (weight / 100)
    p_weight_normal = 0.80 - 0.55 * (weight / 100)

    # Crack sensor likelihood
    p_crack_damaged = 0.10 + 0.85 * (crack / 100)
    p_crack_normal = 0.80 - 0.55 * (crack / 100)

    # Tilt likelihood
    if tilt == 1:
        p_tilt_damaged = 0.85
        p_tilt_normal = 0.20
    else:
        p_tilt_damaged = 0.20
        p_tilt_normal = 0.85

    numerator = (
        prior_damaged
        * p_weight_damaged
        * p_crack_damaged
        * p_tilt_damaged
    )

    denominator = numerator + (
        prior_not_damaged
        * p_weight_normal
        * p_crack_normal
        * p_tilt_normal
    )

    posterior = numerator / denominator

    return clamp(posterior)


# ============================================================
# 3. CERTAINTY FACTORS
# ============================================================

def cf_weight(weight):
    return clamp((weight - 20) / 80)


def cf_crack(crack):
    return clamp((crack - 10) / 90)


def cf_tilt(tilt):
    return 0.75 if tilt == 1 else 0.0


def combine_cf(cf1, cf2):
    """
    MYCIN-style parallel positive CF combination.
    """

    return cf1 + cf2 * (1 - cf1)


def certainty_factor(weight, crack, tilt):

    weight_cf = cf_weight(weight)
    crack_cf = cf_crack(crack)
    tilt_cf = cf_tilt(tilt)

    combined = combine_cf(weight_cf, crack_cf)
    combined = combine_cf(combined, tilt_cf)

    return clamp(combined)


# ============================================================
# 4. BAYESIAN NETWORK
# ============================================================

def bayesian_network(weight, crack, tilt):
    """
    Small Bayesian-network style model:

        SensorNoise -> WeightReading
        CrackVisible -> Damaged
        Tilt -> Damaged

    Exact enumeration is used for the hidden variables.
    """

    # Prior probabilities
    p_damage = 0.20

    # Evidence likelihoods
    weight_damage = 0.10 + 0.85 * weight / 100
    weight_normal = 0.80 - 0.55 * weight / 100

    crack_damage = 0.10 + 0.85 * crack / 100
    crack_normal = 0.80 - 0.55 * crack / 100

    if tilt:
        tilt_damage = 0.85
        tilt_normal = 0.20
    else:
        tilt_damage = 0.20
        tilt_normal = 0.85

    # Joint probability for Damaged
    damaged_probability = (
        p_damage
        * weight_damage
        * crack_damage
        * tilt_damage
    )

    # Joint probability for Not Damaged
    not_damaged_probability = (
        (1 - p_damage)
        * weight_normal
        * crack_normal
        * tilt_normal
    )

    result = damaged_probability / (
        damaged_probability + not_damaged_probability
    )

    return clamp(result)


# ============================================================
# 5. DEMPSTER-SHAFER THEORY
# ============================================================

def sensor_mass(weight, crack, tilt):
    """
    Basic probability assignment:

        {Damaged}
        {NotDamaged}
        {Damaged, NotDamaged} = Uncertain
    """

    damage_evidence = (
        0.45 * weight / 100
        + 0.35 * crack / 100
        + 0.20 * tilt
    )

    damage_evidence = clamp(damage_evidence)

    damaged_mass = 0.15 + 0.70 * damage_evidence
    not_damaged_mass = 0.75 - 0.60 * damage_evidence

    # Keep some mass as uncertainty
    uncertain_mass = 1 - damaged_mass - not_damaged_mass

    uncertain_mass = max(0.05, uncertain_mass)

    total = (
        damaged_mass
        + not_damaged_mass
        + uncertain_mass
    )

    damaged_mass /= total
    not_damaged_mass /= total
    uncertain_mass /= total

    return {
        "D": damaged_mass,
        "N": not_damaged_mass,
        "U": uncertain_mass
    }


def combine_dempster(m1, m2):
    """
    Dempster's rule of combination.
    """

    conflict = (
        m1["D"] * m2["N"]
        + m1["N"] * m2["D"]
    )

    denominator = 1 - conflict

    if denominator <= 0:
        return {
            "D": 0.0,
            "N": 0.0,
            "U": 1.0
        }

    result = {
        "D": (
            m1["D"] * m2["D"]
            + m1["D"] * m2["U"]
            + m1["U"] * m2["D"]
        ) / denominator,

        "N": (
            m1["N"] * m2["N"]
            + m1["N"] * m2["U"]
            + m1["U"] * m2["N"]
        ) / denominator,

        "U": (
            m1["U"] * m2["U"]
        ) / denominator
    }

    return result


def dempster_shafer(weight, crack, tilt):

    weight_mass = sensor_mass(weight, 0, 0)
    crack_mass = sensor_mass(0, crack, 0)
    tilt_mass = sensor_mass(0, 0, tilt)

    combined = combine_dempster(
        weight_mass,
        crack_mass
    )

    combined = combine_dempster(
        combined,
        tilt_mass
    )

    # Belief in damaged
    belief = combined["D"]

    # Plausibility = belief + uncertainty
    plausibility = combined["D"] + combined["U"]

    return belief, plausibility


# ============================================================
# 6. FUZZY LOGIC
# ============================================================

def triangular_membership(x, left, center, right):

    if x <= left or x >= right:
        return 0.0

    if x == center:
        return 1.0

    if x < center:
        return (x - left) / (center - left)

    return (right - x) / (right - center)


def weight_memberships(value):

    low = max(0, min(1, (40 - value) / 40))

    medium = triangular_membership(
        value, 20, 50, 80
    )

    high = max(0, min(1, (value - 60) / 40))

    return {
        "low": low,
        "medium": medium,
        "high": high
    }


def crack_memberships(value):

    none = max(0, min(1, (20 - value) / 20))

    minor = triangular_membership(
        value, 10, 35, 60
    )

    major = max(0, min(1, (value - 45) / 55))

    return {
        "none": none,
        "minor": minor,
        "major": major
    }


def fuzzy_damage_score(weight, crack, tilt):

    wm = weight_memberships(weight)
    cm = crack_memberships(crack)

    # Fuzzy rules
    rule1 = wm["low"] * cm["none"]
    rule2 = wm["medium"] * cm["minor"]
    rule3 = wm["high"]
    rule4 = cm["major"]
    rule5 = wm["medium"] * cm["major"]

    if tilt == 1:
        rule6 = 0.75
    else:
        rule6 = 0.0

    # Consequent damage scores
    scores = [
        (rule1, 10),
        (rule2, 40),
        (rule3, 80),
        (rule4, 85),
        (rule5, 95),
        (rule6, 75)
    ]

    numerator = sum(
        strength * score
        for strength, score in scores
    )

    denominator = sum(
        strength
        for strength, _ in scores
    )

    if denominator == 0:
        return 0.0

    return numerator / denominator


# ============================================================
# COMPLETE CASE ANALYSIS
# ============================================================

def analyze_case(case):

    weight = case["weight_deviation"]
    crack = case["crack_severity"]
    tilt = case["tilt"]

    nonmono = nonmonotonic_reasoning(
        weight,
        crack,
        tilt
    )

    bayes = bayes_posterior(
        weight,
        crack,
        tilt
    )

    cf = certainty_factor(
        weight,
        crack,
        tilt
    )

    bn = bayesian_network(
        weight,
        crack,
        tilt
    )

    ds_belief, ds_plausibility = dempster_shafer(
        weight,
        crack,
        tilt
    )

    fuzzy = fuzzy_damage_score(
        weight,
        crack,
        tilt
    )

    return {
        "Case": case["case"],
        "Weight": weight,
        "Crack": crack,
        "Tilt": "Triggered" if tilt else "Normal",
        "Nonmonotonic": nonmono,
        "Bayes": bayes,
        "CF": cf,
        "BN": bn,
        "DS Belief": ds_belief,
        "DS Plausibility": ds_plausibility,
        "Fuzzy": fuzzy
    }


# ============================================================
# DISAGREEMENT ANALYSIS
# ============================================================

def identify_disagreements(results):

    print("\n" + "=" * 70)
    print("DISAGREEMENT ANALYSIS")
    print("=" * 70)

    disagreements = []

    for result in results:

        bayes_verdict = result["Bayes"] >= 0.50
        cf_verdict = result["CF"] >= 0.50
        bn_verdict = result["BN"] >= 0.50
        fuzzy_verdict = result["Fuzzy"] >= 50

        decisions = [
            bayes_verdict,
            cf_verdict,
            bn_verdict,
            fuzzy_verdict
        ]

        if len(set(decisions)) > 1:

            disagreements.append(result["Case"])

            print(
                f"Case {result['Case']}: methods disagree."
            )

            print(
                "  Reason: Bayesian methods use probability, "
                "while CF and fuzzy logic use different confidence "
                "and membership calculations."
            )

    if len(disagreements) >= 2:
        print(
            f"\nRequirement satisfied: "
            f"{len(disagreements)} disagreement cases found."
        )
    else:
        print(
            "\nOnly a small number of disagreements were found."
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("ROBO PLAN - MODULE B")
    print("REASONING UNDER UNCERTAINTY")
    print("=" * 70)

    # --------------------------------------------------------
    # Nonmonotonic demonstration
    # --------------------------------------------------------

    demonstrate_nonmonotonicity()

    # --------------------------------------------------------
    # Analyze all 10 cases
    # --------------------------------------------------------

    results = []

    for case in TEST_CASES:
        result = analyze_case(case)
        results.append(result)

    dataframe = pd.DataFrame(results)

    # --------------------------------------------------------
    # Display main comparison
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("10 SENSOR CASE COMPARISON")
    print("=" * 70)

    display_columns = [
        "Case",
        "Weight",
        "Crack",
        "Tilt",
        "Nonmonotonic",
        "Bayes",
        "CF",
        "BN",
        "DS Belief",
        "DS Plausibility",
        "Fuzzy"
    ]

    print(
        dataframe[display_columns].to_string(
            index=False,
            formatters={
                "Bayes": "{:.3f}".format,
                "CF": "{:.3f}".format,
                "BN": "{:.3f}".format,
                "DS Belief": "{:.3f}".format,
                "DS Plausibility": "{:.3f}".format,
                "Fuzzy": "{:.2f}".format
            }
        )
    )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    dataframe.to_csv(
        "uncertainty_results.csv",
        index=False
    )

    print(
        "\nResults saved to: uncertainty_results.csv"
    )

    # --------------------------------------------------------
    # Disagreement analysis
    # --------------------------------------------------------

    identify_disagreements(results)

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("MODULE B COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()