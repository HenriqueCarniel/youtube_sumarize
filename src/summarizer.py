import csv
import re
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

input_csv = "data/videos.csv"
output_csv = "data/videos_with_summaries.csv"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
model.to(device)

WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))

def chunk_text(text, max_length=512):
    input_ids = tokenizer(
        [WHITESPACE_HANDLER(text)],
        return_tensors="pt",
        truncation=False
    )["input_ids"]

    num_tokens = len(input_ids[0])
    chunks = []
    start = 0

    while start < num_tokens:
        end = min(start + max_length, num_tokens)
        chunk = input_ids[0][start:end].unsqueeze(0)
        chunks.append(chunk)
        start = end

    if len(chunks[-1][0]) < max_length:
        padding_length = max_length - len(chunks[-1][0])
        padding = torch.zeros((1, padding_length), dtype=torch.long)
        chunks[-1] = torch.cat([chunks[-1], padding], dim=1)
    
    return chunks

def generate_summary(chunks, max_length=256):
    summaries = []
    for chunk in chunks:
        chunk = chunk.to(device)
        output_ids = model.generate(
            input_ids=chunk,
            max_length=max_length,
            no_repeat_ngram_size=2,
            num_beams=6
        )[0]
        summary = tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )
        summaries.append(summary)
    return " ".join(summaries)

def process_csv_row(row):
    try:
        if row["transcription"] and not row["summary"]:
            text = row["transcription"]
            chunks = chunk_text(text, max_length=512)
            summary = generate_summary(chunks, max_length=256)
            row["summary"] = summary
    except Exception as e:
        print(f"Error processing row: {e}")
    return row

def update_csv_with_summaries(input_csv, output_csv):
    with open(input_csv, mode="r", encoding="utf-8") as infile, \
         open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        rows = list(reader)
        for row in tqdm(rows, total=len(rows), desc="Processing Rows"):
            updated_row = process_csv_row(row)
            writer.writerow(updated_row)

if __name__ == '__main__':
    update_csv_with_summaries(input_csv, output_csv)
    print(f"Updated CSV with summaries saved at: {output_csv}")
