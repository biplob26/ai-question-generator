import streamlit as st
import google.generativeai as genai

# Streamlit পেজ সেটিং
st.set_page_config(page_title="AI Question Paper Generator", layout="wide")

st.title("📝 AI প্রশ্নপত্র জেনারেটর (ফাইল আপলোড ফিচারসহ)")
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
        chapters = st.text_area("অধ্যায়/টপিকসমূহ (যদি ফাইল না দেন)", "অধ্যায় ১: প্রাণিজগতের শ্রেণিবিন্যাস")

    # ফাইল আপলোড অপশন
    st.subheader("📁 ফাইল আপলোড (ঐচ্ছিক)")
    uploaded_file = st.file_uploader(
        "যে অধ্যায় বা বইয়ের ওপর প্রশ্ন বানাতে চান তার PDF বা Text ফাইল আপলোড করুন:", 
        type=["pdf", "txt"]
    )

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
            model = genai.GenerativeModel('gemini-2.5-flash')

            # প্রম্পট তৈরি
            prompt_content = []
            
            # নির্দেশনাবলী
            system_instruction = f"""
            তুমি বাংলাদেশের একজন অভিজ্ঞ শিক্ষক। নিচে দেওয়া তথ্যের ওপর ভিত্তি করে একটি পূর্ণাঙ্গ প্রশ্নপত্র তৈরি করো।

            প্রতিষ্ঠানের নাম: {institution}
            পরীক্ষার নাম: {exam_name}
            শ্রেণি: {class_name} | বিষয়: {subject}
            সময়: {time_limit} | মোট নম্বর: {full_marks}

            নির্দেশনা:
            ১. হেডার হিসেবে প্রতিষ্ঠানের নাম, পরীক্ষার নাম, শ্রেণি, বিষয়, সময় ও নম্বর সুন্দর করে লেখো।
            ২. মোট {mcq_count} টি বহুনির্বাচনী প্রশ্ন (MCQ) তৈরি করো (ক, খ, গ, ঘ অপশনসহ)।
            ৩. মোট {cq_count} টি সৃজনশীল প্রশ্ন (ক, খ, গ, ঘ অংশসহ) তৈরি করো।
            ৪. যদি কোনো ফাইল দেওয়া থাকে, তবে অবশ্যই শতভাগ প্রশ্ন সেই ফাইল/ডকুমেন্টের মূল তথ্যের ওপর ভিত্তি করে তৈরি করবে।
            ৫. আউটপুট সরাসরি প্রিন্ট উপযোগী ক্লিন মার্কডাউন ফরম্যাটে দাও।
            """

            prompt_content.append(system_instruction)

            # ফাইল প্রসেসিং
            if uploaded_file is not None:
                # আপলোড করা ফাইল পড়া
                file_bytes = uploaded_file.read()
                
                # Gemini API-তে পাঠানোর জন্য ফাইল ফরম্যাট তৈরি
                blob = {
                    'mime_type': uploaded_file.type,
                    'data': file_bytes
                }
                prompt_content.append("সংযুক্ত ফাইলের কনটেন্ট:")
                prompt_content.append(blob)
            else:
                prompt_content.append(f"অধ্যায়সমূহ: {chapters}")

            with st.spinner("ফাইল পড়া হচ্ছে এবং প্রশ্ন তৈরি হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন..."):
                response = model.generate_content(prompt_content)
                st.success("✅ প্রশ্নপত্র তৈরি সম্পন্ন হয়েছে!")
                
                # প্রশ্ন ড্যাশবোর্ডে দেখানো
                st.markdown("---")
                st.markdown(response.text)
                
                # ডাউনলোডের সুবিধা
                st.download_button(
                    label="📥 প্রশ্নপত্র ডাউনলোড করুন (Text File)",
                    data=response.text,
                    file_name=f"Question_{class_name}_{subject}.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"একটি সমস্যা হয়েছে: {e}")
