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
    
    # إعدادات متوازنة للردود (شرح وافٍ وسريع في نفس الوقت)
    generation_config = genai.GenerationConfig(
        max_output_tokens=800,  # مساحة كافية للشرح والتفصيل
        temperature=0.5         # إجابات دقيقة وواضحة
    )

    model = genai.GenerativeModel(
        model_name="gemini-3.8-flash",
        generation_config=generation_config,
        system_instruction="""أنتِ المساعد الإرشادي الذكي لطالبات المدارس ضمن مبادرة صناع التقدم، بإشراف الأخصائية النفسية (أ. سنيدة الهاشمي).

أسلوب الرد والتوجيه:
1. قدمي إجابات واضحة ومفصلة بأسلوب دافئ، مشجع، ومناسب لطالبات المدارس.
2. عند الحديث عن تنظيم الوقت أو علاج التشتت، وضحي الخطوات بشكل عملي مع أمثلة تبسيطية (مثل شرح تقنية Pomodoro، كيفية كتابة قائمة المهام To-Do List، أو أساليب تقوية الذاكرة).
3. قسمي الإجابة إلى نقاط رئيسية وعناوين فرعية مرتبة ليسهل على الطالبة قراءتها واستيعابها.
4. في حال وجود مشكلة خاصة أو استشارة نفسية/اجتماعية معقدة، وجهي الطالبة بلطف للتواصل المباشر مع الأخصائية النفسية (أ. سنيدة الهاشمي) بالمدرسة."""
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
            # إظهار رسالة التفكير بشكل لطيف أثناء المعالجة
            with st.spinner("جاري تحليل سؤالكِ وإعداد إجابة مميزة لكِ... 💭✨"):
                response = st.session_state.chat.send_message(prompt)
                
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {e}")
