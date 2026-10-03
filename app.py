import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="صناع التقدم", page_icon="🌟")

st.title("🌟 صناع التقدم")
st.caption("المساعد الإرشادي الذكي لطالبات المدارس - تحت إشراف أ. سنيدة الهاشمي")

# جلب المفتاح مع التنظيف
api_key = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")

if not api_key:
    st.error("⚠️ لم يتم العثور على GEMINI_API_KEY. يرجى إضافته في إعدادات Secrets.")
    st.stop()

# تهيئة خدمات جوجل جيميناي
try:
    genai.configure(api_key=api_key)
    
    # إعدادات السرعة والاختصار
    generation_config = genai.GenerationConfig(
        max_output_tokens=250,  # إجابة قصيرة وسريعة
        temperature=0.3         # ردود مباشرة
    )

    model = genai.GenerativeModel(
        model_name="gemini-3.8-flash",
        generation_config=generation_config,
        system_instruction="""أنتِ المساعد الإرشادي الذكي لطالبات المدارس ضمن مبادرة صناع التقدم، بإشراف الأخصائية النفسية (أ. سنيدة الهاشمي).

قواعد الرد:
1. كن/كوني مُختصراً جداً ومباشراً في الرد (أقل من 80 كلمة).
2. قدم خطوات عملية وواضحة فوراً (نقاط رئيسية).
3. استخدم أسلوباً دافئاً ومحفزاً يناسب طالبات المدارس.
4. في حال وجود مشكلة خاصة أو استشارة نفسية معقدة، وجه الطالبة بسطر واحد للتواصل مع الأخصائية النفسية (أ. سنيدة الهاشمي)."""
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
            # إظهار مؤشر "جاري التفكير" للطالبة أثناء معالجة الرد
            with st.spinner("جاري التفكير في أفضل نصيحة لكِ... 💭✨"):
                response = st.session_state.chat.send_message(prompt)
                
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {e}")
