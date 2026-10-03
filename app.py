import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="صناع التقدم", page_icon="🌟")

st.title("🌟 صناع التقدم")
st.caption("المساعد الإرشادي الذكي لطالبات المدارس - تحت إشراف أ. سنيدة الهاشمي")

# جلب المفتاح مع تنظيفه من أي مسافات مخفية
gemini_api_key = os.environ.get("GEMINI_API_KEY", "").strip()

if not gemini_api_key:
    st.error("يرجى إدخال GEMINI_API_KEY في إعدادات Secrets.")
    st.stop()

# تهيئة العميل
client = genai.Client(api_key=gemini_api_key)

SYSTEM_PROMPT = """أنتِ المساعد الإرشادي الذكي لطالبات المدارس ضمن مبادرة صناع التقدم، بإشراف الأخصائية النفسية (أ. سنيدة الهاشمي).
دوركِ الأساسي:
1. تقديم نصائح لتنظيم الوقت وبناء جداول المذاكرة وتقنية Pomodoro.
2. علاج الشرود الذهني والتشتت وتقوية الذاكرة بأسلوب دافئ ومشجع.
3. في حال وجود مشكلة خاصة أو استشارة نفسية معقدة، وجهي الطالبة فوراً للتواصل المباشر مع الأخصائية النفسية (أ. سنيدة الهاشمي) بالمدرسة."""

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات الطالبة
if prompt := st.chat_input("اكتبي سؤالكِ هنا عزيزتي الطالبة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # إعداد محتوى الحوار
        contents = [m["content"] for m in st.session_state.messages]
        
        # تكوين الإعدادات مع إرسال SYSTEM_PROMPT كـ system_instruction
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7
        )

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=config,
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("حدث خطأ أثناء الاتصال بالخدمة. يرجى التأكد من صحة مفتاح GEMINI_API_KEY.")
