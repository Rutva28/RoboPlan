# RoboPlan – Uncertainty-Aware Warehouse Robot Brain

> An AI-based warehouse robot system that combines planning, uncertainty reasoning, game playing, connectionist models, and an expert system for intelligent warehouse operations.

---

# 📖 About The Project

**RoboPlan** is an implementation-based AI project that simulates the decision-making system of a warehouse robot.

The project combines five major AI areas:

* Planning
* Reasoning under uncertainty
* Adversarial game playing
* Connectionist models
* Expert systems

The system demonstrates how a warehouse robot can plan pallet-stacking operations, reason about uncertain sensor information, compete for a charging dock, recover corrupted patterns and detect sensor anomalies, and diagnose robot faults using a rule-based expert system.

The project also includes an integrated control program that connects the five AI modules into a simulated warehouse workflow.

---

# ✨ Features

## 🧠 Planning

* Classic Goal Stack Planning for Blocks World
* Configurable start and goal states using JSON files
* Nonlinear / constraint-posting planning
* Hierarchical planning for high-level pallet operations
* Reactive execution for disturbances
* Execution trace showing robot actions
* Reactive intervention logging

---

## 🔍 Uncertainty Reasoning

* Nonmonotonic reasoning
* Bayes' theorem and posterior probability
* MYCIN-style Certainty Factors
* Bayesian Network reasoning
* Dempster-Shafer evidence combination
* Fuzzy logic
* Comparison of multiple reasoning methods
* Synthetic warehouse sensor readings

---

## 🎮 Game Playing

* MiniMax algorithm
* Alpha-Beta pruning
* Iterative Deepening Search
* Move ordering
* Node-count comparison
* Search-depth benchmarking
* Matplotlib visualization
* Playable command-line dock contention game

---

## 🔗 Connectionist Models

* Hopfield Network implemented from scratch
* Five 8×8 binary patterns
* 12.5% corrupted-bit associative recall
* Pattern recovery demonstration
* Small recurrent neural network using PyTorch
* Prediction from the last 10 sensor readings
* Held-out anomaly detection evaluation

---

## 🛠️ Expert System

* Rule-based warehouse robot diagnosis
* 18 maintenance and fault-diagnosis rules
* Forward-chaining inference
* Explanation trace
* Rule firing information
* JSON-based knowledge base
* Knowledge acquisition through the command line
* Add new rules without changing the inference engine

---

# 🛠️ Tech Stack

| **Area**               | **Technology**                    |
| ---------------------- | --------------------------------- |
| **Language**           | Python                            |
| **Planning**           | Custom Python planning algorithms |
| **Uncertainty**        | Python, NumPy, Pandas             |
| **Bayesian Reasoning** | Python / Bayesian reasoning       |
| **Fuzzy Logic**        | scikit-fuzzy                      |
| **Game Playing**       | Python, MiniMax, Alpha-Beta       |
| **Visualization**      | Matplotlib                        |
| **Hopfield Network**   | NumPy                             |
| **RNN**                | PyTorch                           |
| **Expert System**      | Custom forward-chaining engine    |
| **Data Storage**       | JSON / CSV                        |

---

# 📂 Project Structure

```text
RoboPlan/
│
├── module_a_planning/
│   ├── plan.py
│   ├── start.json
│   └── goal.json
│
├── module_b_uncertainty/
│   ├── uncertainty.py
│   └── uncertainty_results.csv
│
├── module_c_game/
│   └── dock_game.py
│
├── module_d_connectionist/
│   ├── connectionist.py
│   └── hopfield_recovery.png
│
├── module_e_expert/
│   ├── expert_advisor.py
│   └── rules.json
│
├── main.py
├── plan.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

* Python 3.10 or newer
* pip
* Git
* Internet connection for installing Python dependencies
* PyTorch for the RNN module

---

# 📥 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/RoboPlan.git
cd RoboPlan
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running The Project

## Module A – Planning

Run the planner from the project root:

```powershell
python plan.py --start module_a_planning/start.json --goal module_a_planning/goal.json
```

The planner demonstrates Goal Stack Planning, nonlinear planning, hierarchical planning, and reactive execution.

---

## Module B – Uncertainty Reasoning

Run:

```powershell
python module_b_uncertainty/uncertainty.py
```

The module compares multiple uncertainty-reasoning approaches using the same synthetic warehouse sensor readings.

The generated results are saved as:

```text
module_b_uncertainty/uncertainty_results.csv
```

---

## Module C – Game Playing

Run the dock contention game:

```powershell
python module_c_game/dock_game.py --depth 5
```

Run the search benchmark:

```powershell
python module_c_game/dock_game.py --compare
```

Run the playable version:

```powershell
python module_c_game/dock_game.py --depth 5 --play
```

The module compares MiniMax, Alpha-Beta pruning, and iterative deepening search.

---

## Module D – Connectionist Models

Run:

```powershell
python module_d_connectionist/connectionist.py
```

The Hopfield section demonstrates recovery of a corrupted 8×8 binary pattern.

The RNN section trains a small recurrent neural network using sequences of 10 synthetic sensor readings and reports held-out accuracy.

The Hopfield visualization is saved as:

```text
hopfield_recovery.png
```

---

## Module E – Expert System

Run:

```powershell
python module_e_expert/expert_advisor.py
```

The system provides an interactive menu for:

1. Running a sample diagnosis
2. Entering sensor values
3. Adding a new rule
4. Viewing the knowledge base
5. Exiting the system

The expert-system knowledge base is stored in:

```text
module_e_expert/rules.json
```

New rules can be added through the knowledge-acquisition interface without modifying the Python inference engine.

---

# 🔬 Module Demonstrations

## Module A – Planning

Module A demonstrates AI planning for a Blocks World warehouse pallet using Goal Stack Planning, nonlinear planning, hierarchical planning, and reactive behavior. The planner works with configurable start and goal states and produces an execution trace. The reactive layer can respond to disturbances during execution.

---

## Module B – Reasoning Under Uncertainty

Module B demonstrates different approaches for deciding whether a warehouse pallet or package may be damaged when sensor information is uncertain or conflicting. It implements nonmonotonic reasoning, Bayes, Certainty Factors, Bayesian Network reasoning, Dempster-Shafer evidence combination, and fuzzy logic. The methods are evaluated using the same synthetic sensor readings so their conclusions can be compared.

---

## Module C – Game Playing

Module C models charging-dock contention as an adversarial game between robots. It demonstrates MiniMax, Alpha-Beta pruning, iterative deepening, and move ordering while measuring search nodes. A Matplotlib benchmark can compare search behavior across depths 2–6, and the module also provides a playable command-line game.

---

## Module D – Connectionist Models

Module D demonstrates two connectionist approaches. A Hopfield Network implemented from scratch performs associative recall of corrupted 8×8 binary patterns, while a small PyTorch RNN predicts anomalies from sequences of the last 10 sensor readings. The module reports the Hopfield recovery accuracy and RNN held-out test accuracy.

---

## Module E – Expert System

Module E implements a rule-based maintenance advisor for diagnosing warehouse robot problems from sensor and symptom information. The system contains 18 rules and uses forward chaining to reach conclusions. It also provides an explanation trace and a knowledge-acquisition interface for adding new rules through the JSON knowledge base.

---

# 🔗 Integrated System

The main control program connects the five AI modules into a simulated warehouse-robot workflow.

```text
                    Synthetic Sensor Events
                              │
                              ▼
                 ┌────────────────────────┐
                 │ Module B                │
                 │ Uncertainty Reasoning   │
                 └────────────┬───────────┘
                              │
                              ▼
                    Damage Suspected?
                       │          │
                      No         Yes
                       │          │
                       │          ▼
                       │   ┌────────────────────┐
                       │   │ Module E           │
                       │   │ Expert Diagnosis   │
                       │   └────────────────────┘
                       │
                       ▼
             ┌──────────────────────────┐
             │ Module A                 │
             │ Planning + Reactive      │
             │ Execution                │
             └──────────────────────────┘

             ┌──────────────────────────┐
             │ Module C                 │
             │ Dock Contention          │
             │ MiniMax + Alpha-Beta     │
             └──────────────────────────┘

             ┌──────────────────────────┐
             │ Module D                 │
             │ Hopfield + RNN           │
             │ Anomaly Detection        │
             └──────────────────────────┘
```

Run the complete integrated system with:

```powershell
python main.py
```

The integration generates **50 synthetic warehouse events** and demonstrates the interaction between the different AI modules.

---

# 🧪 Testing

The individual modules can be tested independently using their respective commands.

### Planning

```powershell
python plan.py --start module_a_planning/start.json --goal module_a_planning/goal.json
```

### Uncertainty Reasoning

```powershell
python module_b_uncertainty/uncertainty.py
```

### Game Playing

```powershell
python module_c_game/dock_game.py --compare
```

### Connectionist Models

```powershell
python module_d_connectionist/connectionist.py
```

### Expert System

```powershell
python module_e_expert/expert_advisor.py
```

### Complete Integration

```powershell
python main.py
```

---

# 📊 Example Results

## Planning

```text
GOAL STACK PLANNING

01. UNSTACK(D, C)
02. STACK(A, C)
03. STACK(B, A)
04. STACK(D, B)
05. UNSTACK(G, E)
06. STACK(E, D)
07. STACK(F, E)
08. STACK(G, F)
```

---

## Uncertainty Reasoning

The uncertainty module evaluates synthetic sensor cases containing:

```text
Weight deviation
Crack severity
Tilt
```

Different reasoning methods are compared to identify situations where the sensors disagree.

---

## Game Playing

The game module evaluates search performance at different depths and reports explored nodes for:

```text
MiniMax
Alpha-Beta
Iterative Deepening
```

---

## Connectionist Models

The Hopfield network:

```text
Original Pattern
       ↓
12.5% Corruption
       ↓
Corrupted Pattern
       ↓
Hopfield Network
       ↓
Recovered Pattern
```

The RNN uses:

```text
10 Sensor Readings
        ↓
     RNN Model
        ↓
Anomaly Prediction
        ↓
Held-out Accuracy
```

---

## Expert System

Example diagnostic flow:

```text
High Weight
     +
High Crack
     +
High Tilt
     ↓
Expert Rules
     ↓
Structural Damage Suspected
     ↓
Explanation Trace
```

---

# 🎯 Project Requirements Covered

The project covers the five major AI areas required for the warehouse robot brain:

* **Module A:** Planning and reactive systems
* **Module B:** Reasoning under uncertainty
* **Module C:** Game playing and adversarial search
* **Module D:** Connectionist models and anomaly detection
* **Module E:** Expert systems and knowledge acquisition
* **Integration:** Combined warehouse robot control workflow

---

# 👨‍💻 Author

**Rutva Kikani**

Computer Engineering Student

GitHub: `YOUR_GITHUB_USERNAME`

---

# ⭐ Support

If you found this project useful, consider giving the repository a **⭐ Star** on GitHub.

---

# 📄 License

This project is created for educational and academic purposes.

---
