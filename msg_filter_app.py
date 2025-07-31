# msg_filter_app.py
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from lime.lime_text import LimeTextExplainer
import numpy as np



MAX_LEN = 100
MIN_LEN = 15

@st.cache_resource
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

if st.button("🏠Home으로 돌아가기"):
    st.session_state.page = "main"

st.title("📌 감사 메시지 필터링 테스트")



user_input = st.text_area(
    "수혜자가 보낸 감사 메시지", 
    height=150,
    max_chars=MAX_LEN,
    key="message_input"
)

# 글자 수 카운터 표시 (우측 하단에)
char_count = len(user_input)
# st.markdown(
#     f"<div style='text-align: right; color: gray;'>{char_count}/{MAX_LEN}</div>", 
#     unsafe_allow_html=True
# )

if st.button("✔️ 검사하기"):
    if char_count < MIN_LEN:
        st.warning(f"메시지는 최소 {MIN_LEN}자 이상 입력해주세요.")
    else:
        label, prob = predict_sentiment(user_input)

        if label == "긍정" and prob >= 0.82:
            st.success(f"✅ 메시지에 문제 없어 보여요! (긍정 확률: {prob:.2f})")
        else:
            st.error(f"🚫 주의! 부적절한 표현일 수 있습니다. (긍정 확률: {prob:.2f})")

            st.markdown("### ✅ 문제가 될만한 부분을 바꿔봐요!")
            explainer = LimeTextExplainer(class_names=["부정", "긍정"], char_level=False)

            explanation = explainer.explain_instance(
                user_input,
                model_predict_proba,
                num_features=10,
                num_samples=300
            )
            

            # 부정적인 영향을 준 단어만 추출
            negative_words = {
                word: weight
                for word, weight in explanation.as_list(label=1)
                if weight < 0
            }

            # 부정 단어가 없을 경우 예외 처리
            if not negative_words:
                st.info("📘 부정적인 단어가 명확히 드러나진 않아요.")
            else:
                # 원문 텍스트에서 부정 단어 강조
                highlighted_text = user_input
                for word in sorted(negative_words, key=len, reverse=True):
                    highlighted_text = highlighted_text.replace(
                        word, f"<mark style='background-color: #FF9999'>{word}</mark>"
                    )

                st.markdown("#### 📝 부정적인 영향을 준 단어 하이라이팅")
                st.markdown(f"<div style='line-height:1.6;'>{highlighted_text}</div>", unsafe_allow_html=True)