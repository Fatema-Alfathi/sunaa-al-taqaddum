import os
import streamlit as st
from google import genai

st.set_page_config(page_title="صناع التقدم (النسخة الذكية)", page_icon="🌟")

st.title("🌟 صناع التقدم (النسخة الذكية)")
st.caption("المساعد الإرشادي الذكي لطالبات المدارس - تحت إشراف أ. أفراح الكاسبية و أ. سنيدة الهاشمي")

# جلب المفتاح
gemini_api_key = os.environ.get("GEMINI_API_KEY")

if not gemini_api_key:
    st.error("يرجى إدخال GEMINI_API_KEY في الإعدادات.")
    st.stop()

client = genai.Client(api_key=gemini_api_key)

SYSTEM_PROMPT = """أنتِ المساعد الإرشادي الذكي لطالبات المدارس ضمن مبادرة صناع التقدم (النسخة الذكية)، بإشراف الأخصائيات النفسيات (أ. أفراح الكاسبية و أ. سنيدة الهاشمي).
دوركِ الأساسي:
1. تقديم نصائح لتنظيم الوقت وبناء جداول المذاكرة وتقنية Pomodoro.
2. علاج الشرود الذهني والتشتت وتقوية الذاكرة بأسلوب دافئ ومشجع.
3. في حال وجود مشكلة خاصة أو استشارة نفسية معقدة، وجهي الطالبة فوراً للتواصل المباشر مع الأخصائيات النفسيات (أ. أفراح الكاسبية / أ. سنيدة الهاشمي) بالمدرسة."""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتبي سؤالكِ هنا عزيزتي الطالبة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[SYSTEM_PROMPT] + [m["content"] for m in st.session_state.messages],
        )
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
