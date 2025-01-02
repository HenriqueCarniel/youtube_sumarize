from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
import torch

model_name = "neuralmind/bert-large-portuguese-cased"
fine_tuned_model_output_path = "models/fine_tuned_large_bert"
datasets_path = "data/splits"

def preprocess_function(examples):
    texts = []
    labels = []

    for i in range(len(examples["summary"])):
        text = f"Resumo: {examples['summary'][i]} Título: {examples['video_title'][i]} Categoria ID: {examples['category_id'][i]}"
        label = examples["engagement_category"][i]
        texts.append(text)
        labels.append(label)

    encoding = tokenizer(texts, padding="max_length", truncation=True, max_length=512)
    encoding["labels"] = labels
    return encoding

def train_and_save_model(tokenized_datasets):
    training_args = TrainingArguments(
        output_dir=f"{fine_tuned_model_output_path}/results",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        eval_strategy="epoch",
        logging_dir=f"{fine_tuned_model_output_path}/logs",
        save_steps=150
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['validation'],
    )
    trainer.train()

    model.save_pretrained(fine_tuned_model_output_path)
    tokenizer.save_pretrained(fine_tuned_model_output_path)

if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=5)
    model.to(device)

    dataset = load_dataset('csv', data_files={
        'train': f'{datasets_path}/train.csv',
        'validation': f'{datasets_path}/validation.csv',
        'test': f'{datasets_path}/test.csv'
    })

    tokenized_datasets = dataset.map(preprocess_function, batched=True)
    train_and_save_model(tokenized_datasets)
