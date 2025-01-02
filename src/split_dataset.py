import os
import pandas as pd
from datasets import load_dataset, DatasetDict

dataset_path = "data/dataset.csv"
output_data_path = "data/splits"

if __name__ == '__main__':
    dataset = load_dataset('csv', data_files=dataset_path)

    # Data division: 70% training, 15% validation, 15% testing
    train_valid_split = dataset['train'].train_test_split(test_size=0.3, seed=42)
    valid_test_split = train_valid_split['test'].train_test_split(test_size=0.5, seed=42)

    final_dataset = DatasetDict({
        'train': train_valid_split['train'],
        'validation': valid_test_split['train'],
        'test': valid_test_split['test']
    })

    os.makedirs(output_data_path, exist_ok=True)
    for split in final_dataset:
        df = pd.DataFrame(final_dataset[split])
        df.to_csv(os.path.join(output_data_path, f"{split}.csv"), index=False)

    print(f"Datasets saved in: {output_data_path}")
