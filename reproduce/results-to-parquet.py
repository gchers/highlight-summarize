"""Convert HuggingFace Dataset results to Parquet, stripping HF dataset columns.
The merge key (question_id for repliqa, id for bioasq) is preserved for later re-merging.

Writes one file per generation model and dataset, holding the ratings of every judge in
JUDGE_MODELS: `results/<gen-model>/<dataset>/<dataset>_results_processed.parquet`.

Parquet preserves Python types (lists, arrays) natively.
"""

import os
from utils import load_all_results

RESULTS_DIRS = ["results/gpt-4.1-mini", "results/gpt-5.4"]
JUDGE_MODELS = ["gpt-4.1-mini", "gpt-5.4"]

# Columns from HuggingFace datasets to drop (keep only evaluation results + merge key)
HF_COLUMNS = {
    "repliqa": [
        "document_id",
        "document_topic",
        "document_path",
        "document_extracted",
        "question",
        "answer",
        "long_answer",
    ],
    "bioasq": ["question", "answer", "document_extracted"],
}

for results_dir in RESULTS_DIRS:
    merged = {}
    for judge in JUDGE_MODELS:
        results = load_all_results(results_dir, f"judgement-{judge}")
        for dataset_name, dataset_results in results.items():
            print(f"Processing: {results_dir} {dataset_name} (judge: {judge})")
            df = dataset_results.to_pandas()

            # Determine which HF columns to drop based on dataset type
            hf_cols = HF_COLUMNS.get(
                "repliqa" if "repliqa" in dataset_name else "bioasq", []
            )
            df = df.drop(columns=[c for c in hf_cols if c in df.columns])

            if dataset_name not in merged:
                merged[dataset_name] = df
                continue
            # Judgements only add rating columns, so rows must line up with the first judge's.
            base = merged[dataset_name]
            shared = [c for c in df.columns if c in base.columns]
            if not df[shared].equals(base[shared]):
                raise ValueError(
                    f"{results_dir}/{dataset_name}: judge {judge} rows differ."
                )
            merged[dataset_name] = base.join(df.drop(columns=shared))

    for dataset_name, df in merged.items():
        df.to_parquet(
            os.path.join(
                results_dir, dataset_name, f"{dataset_name}_results_processed.parquet"
            ),
            index=False,
            compression="zstd",
            compression_level=9,
        )
