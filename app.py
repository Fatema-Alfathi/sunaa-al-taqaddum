import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="صناع التقدم", page_icon="🌟")

st.title("🌟 صناع التقدم")
st.caption("المساعد الإرشادي الذكي لطالبات المدارس - تحت إشراف أ. سنيدة الهاشمي")

# جلب المفتاح مع التنظيف من أي مسافات
api_key = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")

if not api_key:
    st.error("⚠️ لم يتم العثور على GEMINI_API_KEY. يرجى إضافته في إعدادات Secrets.")
    st.stop()

# تهيئة خدمات جوجل جيميناي
try:
    genai.configure(api_key=api_key)
    
    # إعدادات السرعة والاختصار
    generation_config = genai.GenerationConfig(
        max_output_tokens=300,  # تقليل طول الإجابة لتسريع الرد
        temperature=0.3         # جعل الردود مباشرة وسريعة
    )

    model = genai.GenerativeModel(
        model_name="gemini-3.8-flash",
        generation_config=generation_config,
        system_instruction="""أنتِ المساعد الإرشادي الذكي لطالبات المدارس ضمن مبادرة صناع التقدم، بإشراف الأخصائية النفسية (أ. سنيدة الهاشمي).

قواعد الرد الأساسية:
1. كن/كوني مُختصراً جداً ومباشراً في الرد دون مقدمات طويلة (أقل من 100 كلمة).
2. قدم نقاط عمل سريعة وواضحة لتنظيم الوقت، جداول المذاكرة، تقنية Pomodoro، وعلاج التشتت والشرود الذهني.
3. استخدم أسلوباً دافئاً ومحفزاً ومناسباً لطالبات المدارس.
4. في حال وجود مشكلة خاصة أو استشارة نفسية معقدة، وجه الطالبة مباشرة وبسطر واحد للتواصل مع الأخصائية النفسية (أ. سنيدة الهاشمي)."""
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
