import streamlit as st
import google.generativeai as genai

# Streamlit পেজ সেটিং
st.set_page_config(page_title="AI Question Paper Generator", layout="wide")

st.title("📝 AI প্রশ্নপত্র জেনারেটর")
st.write("সহজেই প্রাতিষ্ঠানিক ও কোচিং পরীক্ষার জন্য নিখুঁত প্রশ্নপত্র তৈরি করুন।")

# সাইডবারে এপিআই কি ইনপুট
with st.sidebar:
    st.header("⚙️ সেটআপ")
    api_key = st.text_input("আপনার Google Gemini API Key দিন:", type="password")
    st.markdown("[ফ্রি API Key পেতে এখানে ক্লিক করুন](https://aistudio.google.com/)")

# ইনপুট ফর্ম
with st.form("question_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        institution = st.text_input("প্রতিষ্ঠানের নাম", "আইডিয়াল স্কুল অ্যান্ড কলেজ")
        exam_name = st.text_input("পরীক্ষার নাম", "অর্ধ-বার্ষিক পরীক্ষা - ২০২৬")
        class_name = st.text_input("শ্রেণি", "৮ম")
        subject = st.text_input("বিষয়", "বিজ্ঞান")
        
    with col2:
        full_marks = st.number_input("মোট নম্বর", value=50, step=5)
        time_limit = st.text_input("সময়", "১ ঘণ্টা ৩০ মিনিট")
        chapters = st.text_area("অধ্যায়/টপিকসমূহ", "অধ্যায় ১: প্রাণিজগতের শ্রেণিবিন্যাস\nঅধ্যায় ২: जीवों বৃদ্ধি ও বংশগতি")

    st.subheader("প্রশ্ন সজ্জা")
    col3, col4 = st.columns(2)
    with col3:
        mcq_count = st.number_input("কয়টি MCQ চান?", value=10, min_value=0)
    with col4:
        cq_count = st.number_input("কয়টি সৃজনশীল/রচনামূলক প্রশ্ন চান?", value=3, min_value=0)

    submit_button = st.form_submit_button("🚀 প্রশ্নপত্র তৈরি করুন")

# এআই দ্বারা প্রশ্ন জেনারেট করা
if submit_button:
    if not api_key:
        st.error("❌ অনুগ্রহ করে সাইডবারে আপনার Gemini API Key দিন।")
    else:
        try:
            genai.configure(api_key=api_key)
            # সঠিক আপডেট করা মডেল নাম
            model = genai.GenerativeModel('gemini-3.6-flash')

            # প্রম্পট ইঞ্জিনিয়ারিং
            prompt = f"""
            তুমি বাংলাদেশের একজন অভিজ্ঞ শিক্ষক। নিচের তথ্য অনুযায়ী একটি পূর্ণাঙ্গ এবং নির্ভুল প্রশ্নপত্র তৈরি করো।

            প্রতিষ্ঠানের নাম: {institution}
            পরীক্ষার নাম: {exam_name}
            শ্রেণি: {class_name} | বিষয়: {subject}
            সময়: {time_limit} | মোট নম্বর: {full_marks}
            অধ্যায়সমূহ: {chapters}

            নির্দেশনা:
            ১. শুরুতে হেডার হিসেবে প্রতিষ্ঠানের নাম, পরীক্ষার নাম, শ্রেণি, বিষয়, সময় এবং নম্বর সুন্দর করে সাজিয়ে লেখো।
            ২. মোট {mcq_count} টি বহুনির্বাচনী প্রশ্ন (MCQ) তৈরি করো। প্রতিটি প্রশ্নের ৪টি অপশন (ক, খ, গ, ঘ) থাকবে।
            ৩. মোট {cq_count} টি সৃজনশীল প্রশ্ন (ক, খ, গ, ঘ অংশসহ) তৈরি করো।
            ৪. প্রশ্নের মান ও জাতীয় শিক্ষাক্রমের ফরম্যাট বজায় রাখো।
            ৫. আউটপুট সরাসরি প্রিন্ট উপযোগী ক্লিন মার্কডাউন ফরম্যাটে দাও।
            """

            with st.spinner("প্রশ্ন তৈরি হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন..."):
                response = model.generate_content(prompt)
                st.success("✅ প্রশ্নপত্র তৈরি সম্পন্ন হয়েছে!")
                
                # প্রশ্ন ড্যাশবোর্ডে দেখানো
                st.markdown("---")
                st.markdown(response.text)
                
                # টেক্সট ডাউনলোডের সুবিধা
                st.download_button(
                    label="📥 প্রশ্নপত্র ডাউনলোড করুন (Text File)",
                    data=response.text,
                    file_name=f"Question_{class_name}_{subject}.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"একটি সমস্যা হয়েছে: {e}")
