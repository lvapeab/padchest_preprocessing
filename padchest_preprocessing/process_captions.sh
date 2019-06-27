#!/usr/bin/env bash

# Renames and splits the files from a dataset in order to fit the preprocessing scripts.
dataset_path=$1
file_suffix=$2
output_dir=$3

mkdir -p ${dataset_path}/${output_dir}

for s in train val test; do
    echo "Processing ${s} split";
    cat ${dataset_path}/${s}${file_suffix} | awk 'BEGIN {FS="\t"} {print $2}' > ${dataset_path}/${output_dir}/${s}_captions.txt
done

echo "Stored captions in ${dataset_path}/${output_dir}"