from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "documentation" / "data-flow-diagram.png"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

steps = [
    "RAW DATASET\n automobileEDA_dirty_training.csv",
    "LOAD DATA\n Read CSV with Pandas",
    "DATA INSPECTION\n Check shape, types, missing values",
    "DATA CLEANING\n Handle duplicates and missing values",
    "DATA TRANSFORMATION\n Standardize dates and create bins",
    "CATEGORICAL ENCODING\n One-Hot Encoding",
    "DATA VALIDATION\n Check rows, columns and duplicates",
    "PROCESSED DATASETS\n automobile_cleaned.csv\n automobile_encoded.csv",
]

fig, ax = plt.subplots(figsize=(12, 16))
ax.set_xlim(0, 12)
ax.set_ylim(0, 18)
ax.axis("off")

positions = [16.5, 14.3, 12.1, 9.9, 7.7, 5.5, 3.3, 1.1]

for i, (label, y) in enumerate(zip(steps, positions)):
    box = FancyBboxPatch(
        (2, y), 8, 1.25,
        boxstyle="round,pad=0.15",
        linewidth=1.5,
        edgecolor="#24527a",
        facecolor="#eaf3f8"
    )
    ax.add_patch(box)
    ax.text(6, y + 0.625, label, ha="center", va="center",
            fontsize=10, fontweight="bold")

    if i < len(steps) - 1:
        ax.annotate(
            "",
            xy=(6, positions[i + 1] + 1.35),
            xytext=(6, y - 0.1),
            arrowprops=dict(arrowstyle="->", lw=1.8)
        )

ax.set_title(
    "AUTOMOBILE DATA ENGINEERING PIPELINE",
    fontsize=16,
    fontweight="bold",
    pad=20
)

plt.tight_layout()
plt.savefig(OUTPUT, dpi=200, bbox_inches="tight")
plt.close()

print(f"Diagram berhasil dibuat: {OUTPUT}")
