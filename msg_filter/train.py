from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import Dataset

import pandas as pd


MODEL_NAME = "beomi/KcELECTRA-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

train_df = pd.read_table("ratings_train.txt")
test_df = pd.read_table("ratings_test.txt")


train_df = train_df.dropna()
test_df = test_df.dropna()

train_dataset = Dataset.from_pandas(train_df[["document", "label"]])
test_dataset = Dataset.from_pandas(test_df[["document", "label"]])

dataset = {
    "train": train_dataset,
    "test": test_dataset
}

def tokenize(example):
    return tokenizer(example["document"], truncation=True, padding="max_length", max_length=128)

tokenized_train = train_dataset.map(tokenize, batched=True)
tokenized_test = test_dataset.map(tokenize, batched=True)

from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./results",
    save_strategy="epoch",
    num_train_epochs=1,
    per_device_train_batch_size=64,
    per_device_eval_batch_size=64,
    learning_rate=5e-5,
    weight_decay=0.01,
    fp16=True,
    load_best_model_at_end=False,  
    logging_dir="./logs",
    logging_steps=50,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,  
    eval_dataset=tokenized_test,  
    tokenizer=tokenizer,
)

trainer.train()