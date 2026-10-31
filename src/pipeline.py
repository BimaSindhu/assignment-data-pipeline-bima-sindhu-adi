
import pandas as pd
from pathlib import Path

# ==========================================
# 1. PROJECT PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "automobileEDA_dirty_training.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "automobile_cleaned.csv"
)
ENCODED_OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "automobile_encoded.csv"
)


# ==========================================
# 2. LOAD DATA
# ==========================================

def load_data(file_path=RAW_FILE):
    """Membaca dataset CSV mentah."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"File dataset tidak ditemukan: {file_path}"
        )

    df = pd.read_csv(file_path)

    print("Dataset berhasil dimuat.")
    print("Jumlah baris:", len(df))
    print("Jumlah kolom:", len(df.columns))

    return df


# ==========================================
# 3. CLEAN TRANSACTION DATE
# ==========================================

def clean_transaction_date(date_value):
    """Menyeragamkan beberapa format tanggal."""

    if pd.isna(date_value):
        return pd.NaT

    date_value = str(date_value).strip()

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%d-%b-%Y"
    ]

    for fmt in formats:
        try:
            return pd.to_datetime(
                date_value,
                format=fmt
            )
        except ValueError:
            continue

    return pd.NaT


# ==========================================
# 4. DATA CLEANING
# ==========================================

def clean_data(df):
    """Membersihkan missing values, duplikat,
    kategori, dan format tanggal."""

    df_clean = df.copy()

    # Hapus kolom bantuan jika ada
    df_clean = df_clean.drop(
        columns=["make_normalized", "transaction_date_clean"],
        errors="ignore"
    )

    # Normalisasi kategori
    categorical_columns = [
        "make",
        "body-style",
        "num-of-doors"
    ]

    for column in categorical_columns:
        df_clean[column] = (
            df_clean[column]
            .astype("string")
            .str.strip()
            .str.lower()
        )

    # Membersihkan tanggal
    df_clean["transaction_date_clean"] = (
        df_clean["transaction_date"]
        .apply(clean_transaction_date)
    )

    # Menghapus duplikat
    rows_before = len(df_clean)

    df_clean = df_clean.drop_duplicates(
        keep="first"
    ).copy()

    rows_after = len(df_clean)

    print("\nDuplikat dihapus:", rows_before - rows_after)

    # Mengisi missing num-of-doors berdasarkan body-style
    door_mode = (
        df_clean.groupby("body-style")["num-of-doors"]
        .agg(
            lambda x: (
                x.mode().iloc[0]
                if not x.mode().empty
                else pd.NA
            )
        )
    )

    missing_doors = df_clean["num-of-doors"].isna()

    df_clean.loc[missing_doors, "num-of-doors"] = (
        df_clean.loc[missing_doors, "body-style"]
        .map(door_mode)
    )

    # Merek yang tidak diketahui
    df_clean["make"] = (
        df_clean["make"].fillna("unknown")
    )

    # Mengisi missing value numerik dengan median
    numeric_columns = [
        "stroke",
        "horsepower",
        "price"
    ]

    for column in numeric_columns:
        median_value = df_clean[column].median()

        df_clean[column] = (
            df_clean[column].fillna(median_value)
        )

        print(
            f"Median {column}: {median_value}"
        )

    return df_clean


# ==========================================
# 5. DATA TRANSFORMATION
# ==========================================

def transform_data(df):
    """Membuat kategori horsepower."""

    df_transformed = df.copy()

    bins = [
        0,
        100,
        150,
        float("inf")
    ]

    labels = [
        "Low",
        "Medium",
        "High"
    ]

    df_transformed["horsepower-binned"] = pd.cut(
        df_transformed["horsepower"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return df_transformed

# ==========================================
# 6. CATEGORICAL ENCODING
# ==========================================

def encode_categorical_data(df):
    """Mengubah seluruh kolom kategorikal menjadi One-Hot Encoding."""

    df_encoded = df.copy()

    categorical_columns = [
        "make",
        "aspiration",
        "num-of-doors",
        "body-style",
        "drive-wheels",
        "engine-location",
        "engine-type",
        "fuel-system",
        "fuel-type",
        "num-of-cylinders",
        "horsepower-binned"
    ]

    # Hanya gunakan kolom yang memang tersedia
    categorical_columns = [
        col for col in categorical_columns
        if col in df_encoded.columns
    ]

    print("\nKolom yang di-encode:")
    print(categorical_columns)

    df_encoded = pd.get_dummies(
        df_encoded,
        columns=categorical_columns,
        dtype=int
    )

    print("\nEncoding berhasil.")
    print("Jumlah kolom setelah encoding:", len(df_encoded.columns))

    return df_encoded


# ==========================================
# 6. SAVE PROCESSED DATA
# ==========================================

def save_data(df, file_path=OUTPUT_FILE):
    """Menyimpan dataset hasil pipeline."""

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        file_path,
        index=False
    )

    print("\nDataset berhasil disimpan:")
    print(file_path)


# ==========================================
# 7. RUN COMPLETE PIPELINE
# ==========================================

def run_pipeline():

    print("================================")
    print("AUTOMOBILE DATA PIPELINE")
    print("================================")

    # 1. Load
    df = load_data()

    # 2. Cleaning
    df_clean = clean_data(df)

    # 3. Transformation
    df_final = transform_data(df_clean)

    # 4. Encoding
    df_encoded = encode_categorical_data(df_final)

    # 5. Save cleaned dataset
    save_data(df_final)

    # 6. Save encoded dataset
    save_data(
        df_encoded,
        ENCODED_OUTPUT_FILE
    )

    # 7. Final validation
    print("\n===== FINAL VALIDATION =====")

    print("Jumlah baris:", len(df_final))
    print("Jumlah kolom cleaned:", len(df_final.columns))
    print("Jumlah kolom encoded:", len(df_encoded.columns))
    print("Jumlah duplikat:", df_final.duplicated().sum())

    print("\nMissing values:")
    print(
        df_final.isnull().sum()[
            df_final.isnull().sum() > 0
        ]
    )

    print("\nDistribusi horsepower-binned:")
    print(df_final["horsepower-binned"].value_counts())

    print("\nPIPELINE SELESAI!")

# ==========================================
# 8. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":
    run_pipeline()