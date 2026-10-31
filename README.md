# Automobile Data Engineering Pipeline

## 1. Project Overview

This project implements a reusable data engineering pipeline using Python and Pandas to clean, transform, and prepare a dirty automobile dataset for further analysis.

The pipeline processes raw automobile transaction data through several stages:

1. Data loading
2. Data inspection
3. Data cleaning
4. Data transformation
5. Categorical encoding
6. Data validation
7. Exporting processed datasets

## 2. Project Structure

```text
data-pipeline-assignment/
│
├── data/
│   ├── raw/
│   │   └── automobileEDA_dirty_training.csv
│   │
│   └── processed/
│       ├── automobile_cleaned.csv
│       └── automobile_encoded.csv
│
├── notebooks/
│   └── 01_data_inspection.ipynb
│
├── src/
│   └── pipeline.py
│
├── documentation/
│   └── data-flow-diagram.png
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 3. Dataset Description

The project uses `automobileEDA_dirty_training.csv` as the raw input dataset.

Initial dataset dimensions:

- Rows: 205
- Columns: 30

The dataset contains automobile attributes such as manufacturer, body style, engine specifications, horsepower, fuel system, and price.

## 4. Data Cleaning

The following cleaning operations are implemented:

### Duplicate Removal

Duplicate records are removed using Pandas `drop_duplicates()`.

- Initial rows: 205
- Duplicate records removed: 4
- Final rows: 201

### Missing Value Handling

Missing values are handled using appropriate strategies:

| Column | Method |
|---|---|
| `stroke` | Median imputation |
| `horsepower` | Median imputation |
| `price` | Median imputation |
| `num-of-doors` | Mode based on `body-style` |
| `make` | Replaced with `unknown` |
| `transaction_date` | Original missing values retained |

The median values used:

- Stroke: 3.29
- Horsepower: 95.0
- Price: 10270.0

Missing transaction dates are retained because their original values cannot be reliably inferred.

### Date Standardization

The transaction date column contains multiple date formats. A custom function standardizes supported formats into a datetime column named `transaction_date_clean`.

### Categorical Standardization

Text categories such as `make` and `body-style` are normalized by trimming whitespace and converting text to lowercase.

## 5. Data Transformation

### Horsepower Binning

The `horsepower` column is categorized into three groups:

| Category | Range |
|---|---|
| Low | 0–100 |
| Medium | Greater than 100–150 |
| High | Greater than 150 |

The resulting distribution:

| Category | Records |
|---|---:|
| Low | 110 |
| Medium | 61 |
| High | 30 |

### Categorical Encoding

Categorical features are converted into numerical columns using One-Hot Encoding with `pandas.get_dummies()`.

The fuel type representation is already available as binary columns named `diesel` and `gas` in the cleaned dataset.

## 6. Pipeline Validation

The pipeline performs validation after processing.

Latest execution results:

| Validation | Result |
|---|---:|
| Initial rows | 205 |
| Processed rows | 201 |
| Cleaned columns | 31 |
| Encoded columns | 86 |
| Remaining duplicate rows | 0 |
| Missing transaction dates | 2 |

The remaining missing values are limited to the original transaction date and its derived datetime column.

## 7. Output Files

The pipeline generates two processed datasets:

- `automobile_cleaned.csv`: cleaned and transformed dataset.
- `automobile_encoded.csv`: dataset with categorical features converted into numerical columns.

## 8. Requirements

- Python 3
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter

Dependencies are listed in `requirements.txt`.

## 9. How to Run the Pipeline

Clone the repository and move into the project directory.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python -u src/pipeline.py
```

The processed datasets will be saved automatically in `data/processed/`.

## 10. ETL Workflow

```text
Raw Automobile Dataset
          |
          v
      Load Data
          |
          v
    Data Inspection
          |
          v
     Data Cleaning
          |
          v
  Data Transformation
          |
          v
 Categorical Encoding
          |
          v
   Data Validation
          |
          v
  Processed CSV Files
```

## 11. Conclusion

This project demonstrates a reusable data preparation pipeline using Python and Pandas. The pipeline handles duplicate records, missing values, inconsistent date formats, categorical standardization, numerical imputation, feature binning, and categorical encoding.

The final datasets are prepared for further exploratory data analysis and machine learning workflows.
