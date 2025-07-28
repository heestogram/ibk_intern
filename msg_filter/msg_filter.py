from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model = AutoModelForSequenceClassification.from_pretrained("anthj/naviyam-msg")
tokenizer = AutoTokenizer.from_pretrained("anthj/naviyam-msg")



def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}  

    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        probs = outputs.logits.softmax(dim=-1)
        label = "긍정" if probs[0][1] > 0.5 else "부정"
        return label, probs[0][1].item()

print(predict_sentiment("솔직히 별로 큰 돈도 아닌데 ㅃㄹㅃㄹ좀 주세요"))