import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from lime.lime_text import LimeTextExplainer
import numpy as np
from pprint import pprint



MAX_LEN = 100
MIN_LEN = 15


def load_model():
    model = AutoModelForSequenceClassification.from_pretrained("anthj/naviyam-msg")
    tokenizer = AutoTokenizer.from_pretrained("anthj/naviyam-msg")
    return model, tokenizer

model, tokenizer = load_model()

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}  
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        probs = outputs.logits.softmax(dim=-1)
        label = "긍정" if probs[0][1] > 0.5 else "부정"
        return label, probs[0][1].item()

def model_predict_proba(texts):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs.to(model.device))
        probs = torch.softmax(outputs.logits, dim=-1).cpu().numpy()
    return probs

user_input = "잘 먹긴 했는데, 빨리 좀 보내주시면 안되나요 개별로네요 진짜"

label, prob = predict_sentiment(user_input)

explainer = LimeTextExplainer(class_names=["부정", "긍정"], char_level=False)

explanation = explainer.explain_instance(
    user_input,
    model_predict_proba,
    num_features=10,
    num_samples=1000
)

print(explanation.available_labels())
print("-------------------")
print(explanation.as_list(label=1))