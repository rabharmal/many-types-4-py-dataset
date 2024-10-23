#!/bin/bash

# Step 1: Clone the dataset
python -m repo_cloner -i data/mypy-dependents-by-stars.json -o repos

# Step 2: Reset the commits
./scripts/reset_commits.sh data/ManyTypes4PyDataset.spec repos

# Step 3: Generate duplicate tokens
cd4py --p repos --ot tokens --od manytypes4py_dataset_duplicates.jsonl.gz --d 1024

# Step 4: Collect duplicate files
python3 scripts/collect_dupes.py manytypes4py_dataset_duplicates.jsonl.gz manytypes4py_dup_files.txt

# Step 5: Process the dataset
python3 scripts/process_dataset.py repos manytypes4py_dup_files.txt /path/to/new_dataset

# Step 6: Split dataset
python3 scripts/split_dataset.py /path/to/new_dataset manytypes4py_split.csv

# Step 7: Run libsa4py
libsa4py process --p /path/to/new_dataset --o /path/to/output --s manytypes4py_split.csv --j [WORKERS COUNT]

# Step 8: Create a tar file
tar -czvf /path/to/output.tar.gz /path/to/dataset_artifacts