import streamlit as st

from modules.resume_parser import extract_resume_text
from modules.ats_scoring import calculate_ats_score
from modules.keyword_analyzer import analyze_keywords
from modules.claude_client import analyze_resume_with_claude


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Resume Analyzer")
st.write(
    "Upload your resume and compare it with a job description "
    "using ATS scoring and Claude AI."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Resume Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf", "docx"]
)


# ============================================================
# JOB DESCRIPTION
# ============================================================

st.header("🎯 Job Description")

job_description = st.text_area(
    "Paste the job description",
    height=250,
    placeholder="Paste the complete job description here..."
)


# ============================================================
# RESUME ANALYSIS
# ============================================================

if uploaded_file is None:

    st.info(
        "👈 Upload your PDF or DOCX resume from the sidebar."
    )

else:

    try:

        resume_text = extract_resume_text(
            uploaded_file
        )

        if not resume_text:

            st.error(
                "Could not extract text from the uploaded resume."
            )

        else:

            st.success(
                "Resume uploaded and text extracted successfully."
            )

            # ------------------------------------------------
            # EXTRACTED TEXT
            # ------------------------------------------------

            with st.expander("View Extracted Resume Text"):

                st.text(resume_text)


            # ------------------------------------------------
            # ATS SCORE
            # ------------------------------------------------

            st.header("📊 ATS Score")

            scores = calculate_ats_score(
                resume_text,
                job_description
            )


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "Overall ATS",
                    f"{scores['overall_score']}/100"
                )


            with col2:

                st.metric(
                    "Keywords",
                    f"{scores['keyword_score']}%"
                )


            with col3:

                st.metric(
                    "Skills",
                    f"{scores['skills_score']}%"
                )


            with col4:

                st.metric(
                    "Formatting",
                    f"{scores['formatting_score']}%"
                )


            # ------------------------------------------------
            # SCORE BREAKDOWN
            # ------------------------------------------------

            st.subheader("Score Breakdown")


            st.write(
                f"Keyword Match: {scores['keyword_score']}%"
            )

            st.progress(
                scores["keyword_score"] / 100
            )


            st.write(
                f"Skills Match: {scores['skills_score']}%"
            )

            st.progress(
                scores["skills_score"] / 100
            )


            st.write(
                f"Formatting: {scores['formatting_score']}%"
            )

            st.progress(
                scores["formatting_score"] / 100
            )


            st.write(
                f"Contact Information: "
                f"{scores['contact_score']}%"
            )

            st.progress(
                scores["contact_score"] / 100
            )


            # ------------------------------------------------
            # KEYWORD ANALYSIS
            # ------------------------------------------------

            if job_description.strip():

                st.header("🔎 Keyword Analysis")


                keywords = analyze_keywords(
                    resume_text,
                    job_description
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.subheader(
                        "✅ Matched Keywords"
                    )

                    if keywords["matched"]:

                        for keyword in keywords["matched"]:

                            st.success(keyword)

                    else:

                        st.info(
                            "No matching keywords found."
                        )


                with col2:

                    st.subheader(
                        "❌ Missing Keywords"
                    )

                    if keywords["missing"]:

                        for keyword in keywords["missing"]:

                            st.warning(keyword)

                    else:

                        st.success(
                            "No major missing keywords."
                        )


            # ------------------------------------------------
            # CLAUDE AI
            # ------------------------------------------------

            st.header("🤖 Claude AI Analysis")


            if st.button(
                "Analyze Resume with Claude",
                type="primary"
            ):

                if not job_description.strip():

                    st.warning(
                        "Please paste a job description first."
                    )

                else:

                    try:

                        with st.spinner(
                            "Claude is analyzing your resume..."
                        ):

                            analysis = (
                                analyze_resume_with_claude(
                                    resume_text,
                                    job_description
                                )
                            )


                        # ------------------------------------
                        # SUMMARY
                        # ------------------------------------

                        st.subheader(
                            "Professional Assessment"
                        )

                        st.write(
                            analysis.get(
                                "summary",
                                "No summary generated."
                            )
                        )


                        # ------------------------------------
                        # STRENGTHS
                        # ------------------------------------

                        st.subheader(
                            "💪 Strengths"
                        )

                        strengths = analysis.get(
                            "strengths",
                            []
                        )

                        for item in strengths:

                            st.success(item)


                        # ------------------------------------
                        # WEAKNESSES
                        # ------------------------------------

                        st.subheader(
                            "⚠️ Weaknesses"
                        )

                        weaknesses = analysis.get(
                            "weaknesses",
                            []
                        )

                        for item in weaknesses:

                            st.warning(item)


                        # ------------------------------------
                        # RECOMMENDATIONS
                        # ------------------------------------

                        st.subheader(
                            "💡 Recommendations"
                        )

                        recommendations = analysis.get(
                            "recommendations",
                            []
                        )

                        for item in recommendations:

                            st.info(item)


                        # ------------------------------------
                        # IMPROVED SUMMARY
                        # ------------------------------------

                        st.subheader(
                            "✨ Improved Professional Summary"
                        )

                        st.write(
                            analysis.get(
                                "improved_summary",
                                "No improved summary generated."
                            )
                        )


                    except Exception as e:

                        st.error(
                            f"Claude API Error: {e}"
                        )


    except Exception as e:

        st.error(
            f"Resume processing error: {e}"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Resume Analyzer | Python + Streamlit + Claude AI"
)