from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score, f1_score
from datasets import load_dataset
from matplotlib import pyplot as plt
import os

fine_tuned_model_input_path = "models/fine_tuned_base_bert"
datasets_path = "data/splits"
output_metrics_path = f"{fine_tuned_model_input_path}/metrics"

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

if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained(fine_tuned_model_input_path)
    model = AutoModelForSequenceClassification.from_pretrained(fine_tuned_model_input_path)

    test_dataset = load_dataset('csv', data_files={ 'test': f'{datasets_path}/test.csv' })['test']
    tokenized_test_dataset = test_dataset.map(preprocess_function, batched=True)

    # Evaluation
    trainer = Trainer(model=model)
    predictions = trainer.predict(tokenized_test_dataset)
    y_pred = predictions.predictions.argmax(axis=1)
    y_true = predictions.label_ids

    # Metrics
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')
    class_report = classification_report(y_true, y_pred, target_names=[f"Class {i}" for i in range(5)])

    # View and save the confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[f"Class {i}" for i in range(5)])
    os.makedirs(output_metrics_path, exist_ok=True)
    confusion_matrix_path = os.path.join(output_metrics_path, "confusion_matrix.png")
    disp.plot()
    plt.savefig(confusion_matrix_path)
    plt.close()

    # Saving metrics to a text file
    metrics_text = f"Accuracy: {accuracy}\nF1-Score (weighted): {f1}\n\nClassification Report:\n{class_report}"
    metrics_file_path = os.path.join(output_metrics_path, "metrics.txt")
    with open(metrics_file_path, 'w', encoding='utf-8') as metrics_file:
        metrics_file.write(metrics_text)
