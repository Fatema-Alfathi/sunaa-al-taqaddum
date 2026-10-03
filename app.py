import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="صناع التقدم", page_icon="🌟")

st.title("🌟 صناع التقدم")
st.caption("المساعد الإرشادي الذكي لطالبات المدارس - تحت إشراف أ. سنيدة الهاشمي")

# جلب المفتاح مع التنظيف من أي مسافات أو علامات إضافية
api_key = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")

if not api_key:
    st.error("⚠️ لم يتم العثور على GEMINI_API_KEY. يرجى إضافته في إعدادات Secrets.")
    st.stop()

# تهيئة خدمات جوجل جيميناي
try:
    genai.configure(api_key=api_key)
    # استخدام النموذج المعتمد والمستقر للـ API
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction="""أنتِ المساعد الإرشادي الذكي لطالبات المدارس ضمن مبادرة صناع التقدم، بإشراف الأخصائية النفسية (أ. سنيدة الهاشمي).
دوركِ الأساسي:
1. تقديم نصائح لتنظيم الوقت وبناء جداول المذاكرة وتقنية Pomodoro.
2. علاج الشرود الذهني والتشتت وتقوية الذاكرة بأسلوب دافئ ومشجع.
3. في حال وجود مشكلة خاصة أو استشارة نفسية معقدة، وجهي الطالبة فوراً للتواصل المباشر مع الأخصائية النفسية (أ. سنيدة الهاشمي) بالمدرسة."""
    )
except Exception as e:
    st.error(f"خطأ في تهيئة المفتاح: {e}")
    st.stop()

# إدارة ذاكرة المحادثة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال رسائل الطالبات
if prompt := st.chat_input("اكتبي سؤالكِ هنا عزيزتي الطالبة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {e}")
