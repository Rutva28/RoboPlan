"""
RoboPlan - Module D
Connectionist Models

Part 1:
    Hopfield Network from scratch
    - Stores 5 binary 8x8 patterns
    - Corrupts one pattern by 12.5%
    - Recovers the original pattern

Part 2:
    Small RNN using PyTorch
    - Uses sequences of 10 sensor readings
    - Predicts whether an anomaly is imminent
    - Reports held-out accuracy

Comparison:
    Hopfield vs RNN
"""

import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt


# ============================================================
# PART 1 - HOPFIELD NETWORK
# ============================================================

class HopfieldNetwork:
    """
    Simple Hopfield Network implemented from scratch.

    Each pattern contains 64 values:
        +1 = ON
        -1 = OFF

    Hebbian learning is used to calculate the weight matrix.
    """

    def __init__(self, n_neurons):
        self.n_neurons = n_neurons

        # Weight matrix
        self.weights = np.zeros(
            (n_neurons, n_neurons),
            dtype=float
        )

    def train(self, patterns):
        """
        Hebbian learning.

        W = sum(pattern * pattern_transpose)

        Diagonal values are kept at zero.
        """

        self.weights.fill(0)

        for pattern in patterns:
            pattern = np.asarray(pattern)

            self.weights += np.outer(pattern, pattern)

        # A neuron should not connect to itself.
        np.fill_diagonal(self.weights, 0)

        # Normalize weights.
        self.weights /= len(patterns)

    def predict(self, pattern, max_iterations=10):
        """
        Recover a corrupted pattern.

        The network updates neurons one by one.
        """

        state = np.asarray(pattern).copy()

        for _ in range(max_iterations):

            old_state = state.copy()

            for i in range(self.n_neurons):

                activation = np.dot(
                    self.weights[i],
                    state
                )

                if activation >= 0:
                    state[i] = 1
                else:
                    state[i] = -1

            # Stop if state no longer changes.
            if np.array_equal(old_state, state):
                break

        return state


def create_patterns():
    """
    Create five 8x8 binary patterns.

    These represent simplified warehouse
    label / visual patterns.
    """

    patterns = []

    # Pattern 1 - X
    p1 = np.array([
        "10000001",
        "01000010",
        "00100100",
        "00011000",
        "00011000",
        "00100100",
        "01000010",
        "10000001"
    ])

    # Pattern 2 - Square
    p2 = np.array([
        "11111111",
        "10000001",
        "10000001",
        "10000001",
        "10000001",
        "10000001",
        "10000001",
        "11111111"
    ])

    # Pattern 3 - Plus
    p3 = np.array([
        "00011000",
        "00011000",
        "00011000",
        "11111111",
        "11111111",
        "00011000",
        "00011000",
        "00011000"
    ])

    # Pattern 4 - Diamond
    p4 = np.array([
        "00011000",
        "00111100",
        "01111110",
        "11111111",
        "11111111",
        "01111110",
        "00111100",
        "00011000"
    ])

    # Pattern 5 - Arrow
    p5 = np.array([
        "00011000",
        "00111100",
        "01111110",
        "11011011",
        "00011000",
        "00011000",
        "00011000",
        "00011000"
    ])

    raw_patterns = [p1, p2, p3, p4, p5]

    for pattern in raw_patterns:

        # Convert characters to integers.
        binary = np.array([
            [int(value) for value in row]
            for row in pattern
        ])

        # Convert:
        # 0 -> -1
        # 1 -> +1
        bipolar = np.where(binary == 1, 1, -1)

        patterns.append(bipolar.flatten())

    return patterns


def corrupt_pattern(pattern, corruption_rate=0.125):
    """
    Flip approximately 12.5% of bits.

    For 64 bits:
        64 * 0.125 = 8 bits
    """

    corrupted = pattern.copy()

    number_to_flip = int(
        len(pattern) * corruption_rate
    )

    rng = np.random.default_rng(42)

    indexes = rng.choice(
        len(pattern),
        size=number_to_flip,
        replace=False
    )

    corrupted[indexes] *= -1

    return corrupted, indexes


def print_pattern(pattern, title):
    """
    Print an 8x8 pattern in the terminal.
    """

    print("\n" + title)
    print("-" * 30)

    grid = pattern.reshape(8, 8)

    for row in grid:

        line = ""

        for value in row:

            if value == 1:
                line += "██"
            else:
                line += "  "

        print(line)


def run_hopfield_demo():
    """
    Complete Hopfield demonstration.
    """

    print("\n")
    print("=" * 60)
    print("PART 1 - HOPFIELD NETWORK")
    print("=" * 60)

    patterns = create_patterns()

    print("\nStored patterns:", len(patterns))
    print("Pattern size: 8 x 8 = 64 neurons")

    # Create network.
    network = HopfieldNetwork(64)

    # Train network.
    network.train(patterns)

    print("Hopfield network trained successfully.")

    # Select pattern 4.
    original = patterns[3]

    # Corrupt 12.5%.
    corrupted, changed_indexes = corrupt_pattern(
        original,
        corruption_rate=0.125
    )

    # Recover pattern.
    recovered = network.predict(
        corrupted,
        max_iterations=10
    )

    print("\nCorrupted bits:", len(changed_indexes))
    print("Corruption rate: 12.5%")

    print_pattern(
        original,
        "ORIGINAL PATTERN"
    )

    print_pattern(
        corrupted,
        "CORRUPTED PATTERN"
    )

    print_pattern(
        recovered,
        "RECOVERED PATTERN"
    )

    # Calculate recovery accuracy.
    recovery_accuracy = np.mean(
        original == recovered
    ) * 100

    print(
        f"\nRecovery accuracy: "
        f"{recovery_accuracy:.2f}%"
    )

    if np.array_equal(original, recovered):
        print("SUCCESS: Original pattern recovered!")
    else:
        print(
            "The network recovered the pattern "
            "partially."
        )

    return {
        "original": original,
        "corrupted": corrupted,
        "recovered": recovered,
        "accuracy": recovery_accuracy
    }


# ============================================================
# PART 2 - RNN
# ============================================================

class SensorRNN(nn.Module):
    """
    Small recurrent neural network.

    Input:
        10 sensor readings

    Output:
        0 = Normal
        1 = Anomaly
    """

    def __init__(
        self,
        input_size=3,
        hidden_size=16,
        num_layers=1
    ):

        super().__init__()

        self.rnn = nn.RNN(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )

        self.fc = nn.Linear(
            hidden_size,
            1
        )

    def forward(self, x):

        output, hidden = self.rnn(x)

        # Use the final time step.
        last_output = output[:, -1, :]

        result = self.fc(last_output)

        return result


def generate_sensor_data(
    total_sequences=200,
    sequence_length=10
):
    """
    Generate synthetic warehouse sensor sequences.

    Each time step has three sensors:

        1. Weight deviation
        2. Crack severity
        3. Tilt

    Label:
        0 = normal
        1 = anomaly
    """

    rng = np.random.default_rng(123)

    X = []
    y = []

    for _ in range(total_sequences):

        # Start with normal readings.
        weight = rng.normal(
            10,
            4,
            sequence_length
        )

        crack = rng.normal(
            10,
            5,
            sequence_length
        )

        tilt = rng.normal(
            5,
            3,
            sequence_length
        )

        label = 0

        # Approximately half the sequences
        # contain an anomaly.
        if rng.random() < 0.5:

            label = 1

            # Increase the final readings.
            weight[-4:] += rng.uniform(
                25,
                50,
                4
            )

            crack[-4:] += rng.uniform(
                30,
                60,
                4
            )

            tilt[-4:] += rng.uniform(
                15,
                30,
                4
            )

        sequence = np.column_stack(
            [
                weight,
                crack,
                tilt
            ]
        )

        X.append(sequence)
        y.append(label)

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    return X, y


def train_rnn():
    """
    Train and evaluate the RNN.
    """

    print("\n")
    print("=" * 60)
    print("PART 2 - RNN SENSOR ANOMALY DETECTION")
    print("=" * 60)

    # Generate data.
    X, y = generate_sensor_data()

    # Normalize features.
    mean = X.mean(
        axis=(0, 1),
        keepdims=True
    )

    std = X.std(
        axis=(0, 1),
        keepdims=True
    )

    X = (X - mean) / (std + 1e-8)

    # Convert to tensors.
    X = torch.tensor(X)
    y = torch.tensor(y)

    # Train/test split.
    split = int(len(X) * 0.8)

    X_train = X[:split]
    y_train = y[:split]

    X_test = X[split:]
    y_test = y[split:]

    print("\nTraining sequences:", len(X_train))
    print("Testing sequences:", len(X_test))
    print("Sequence length:", X.shape[1])
    print("Sensors per timestep:", X.shape[2])

    # Create model.
    model = SensorRNN()

    # Binary classification loss.
    criterion = nn.BCEWithLogitsLoss()

    # Adam optimizer.
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.01
    )

    epochs = 100

    print("\nTraining RNN...")

    for epoch in range(epochs):

        model.train()

        optimizer.zero_grad()

        output = model(
            X_train
        ).squeeze(1)

        loss = criterion(
            output,
            y_train
        )

        loss.backward()

        optimizer.step()

        if (
            (epoch + 1) % 20 == 0
            or epoch == 0
        ):

            print(
                f"Epoch {epoch + 1:3d}/"
                f"{epochs} | "
                f"Loss: {loss.item():.4f}"
            )

    # Evaluate.
    model.eval()

    with torch.no_grad():

        test_output = model(
            X_test
        ).squeeze(1)

        probabilities = torch.sigmoid(
            test_output
        )

        predictions = (
            probabilities >= 0.5
        ).float()

        accuracy = (
            predictions == y_test
        ).float().mean().item() * 100

    print(
        f"\nHeld-out test accuracy: "
        f"{accuracy:.2f}%"
    )

    print(
        "\nRNN purpose:"
        "\n- Reads the last 10 sensor readings."
        "\n- Learns temporal patterns."
        "\n- Predicts whether an anomaly is imminent."
    )

    return model, accuracy


# ============================================================
# COMPARISON
# ============================================================

def print_comparison():

    print("\n")
    print("=" * 60)
    print("HOPFIELD NETWORK VS RNN")
    print("=" * 60)

    print("""
+----------------------+----------------------+----------------------+
| Feature              | Hopfield Network    | RNN                  |
+----------------------+----------------------+----------------------+
| Main purpose         | Pattern recovery    | Sequence prediction  |
| Input                | Binary pattern      | Sensor sequence      |
| Memory               | Associative memory  | Temporal memory      |
| Training             | Hebbian learning    | Gradient descent     |
| Best for             | Noisy label/image   | Time-series sensors  |
| RoboPlan usage       | Recover corrupted   | Predict anomalies    |
|                      | warehouse label     | from sensor history  |
+----------------------+----------------------+----------------------+
""")


# ============================================================
# VISUALIZATION
# ============================================================

def save_visualization(hopfield_result):

    original = hopfield_result["original"]
    corrupted = hopfield_result["corrupted"]
    recovered = hopfield_result["recovered"]

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(9, 3)
    )

    images = [
        original,
        corrupted,
        recovered
    ]

    titles = [
        "Original",
        "Corrupted 12.5%",
        "Recovered"
    ]

    for ax, image, title in zip(
        axes,
        images,
        titles
    ):

        ax.imshow(
            image.reshape(8, 8),
            cmap="gray"
        )

        ax.set_title(title)
        ax.axis("off")

    plt.tight_layout()

    plt.savefig(
        "hopfield_recovery.png",
        dpi=150
    )

    plt.close()

    print(
        "\nSaved visualization:"
        " hopfield_recovery.png"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("#" * 60)
    print("ROBOPLAN - MODULE D")
    print("CONNECTIONIST MODELS")
    print("#" * 60)

    # Part 1
    hopfield_result = run_hopfield_demo()

    # Save Hopfield image.
    save_visualization(
        hopfield_result
    )

    # Part 2
    _, rnn_accuracy = train_rnn()

    # Comparison
    print_comparison()

    print("\n")
    print("=" * 60)
    print("MODULE D COMPLETE")
    print("=" * 60)

    print(
        f"\nFinal Hopfield recovery: "
        f"{hopfield_result['accuracy']:.2f}%"
    )

    print(
        f"Final RNN test accuracy: "
        f"{rnn_accuracy:.2f}%"
    )

    print(
        "\nFiles generated:"
        "\n- hopfield_recovery.png"
    )


if __name__ == "__main__":
    main()