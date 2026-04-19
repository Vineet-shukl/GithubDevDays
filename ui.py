"""
Streamlit dashboard for Phishing Email Classifier.
"""

import streamlit as st
import asyncio
from datetime import datetime
from models import ThreatReport
from agent import agent
from samples import SAMPLES


# Page configuration
st.set_page_config(
    page_title="PhishGuard - Phishing Email Classifier",
    page_icon="🛡️",
    layout="wide"
)

# Title and description
st.title("🛡️ PhishGuard")
st.markdown("AI-powered phishing detection using **Pydantic AI** + **Groq (LLaMA 3.3 70B)**")
st.markdown("---")

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📧 Email Input")
    
    # Email input
    raw_email = st.text_area(
        "Paste raw email here",
        height=300,
        placeholder="""From: sender@example.com
Subject: Important message

Email body goes here...""",
        key="email_input"
    )
    
    # Optional fields
    sender = st.text_input("Sender (optional)", key="sender_input")
    subject = st.text_input("Subject (optional)", key="subject_input")
    
    # Analyze button
    analyze_btn = st.button(
        "🔍 Analyze Email",
        type="primary",
        use_container_width=True
    )
    
    # Example buttons
    st.markdown("---")
    st.subheader("📚 Quick Load Examples")
    
    # First row of examples (3 buttons)
    cols = st.columns(3)
    for idx, sample in enumerate(SAMPLES[:3]):
        with cols[idx]:
            if st.button(
                f"{sample['name']}",
                use_container_width=True,
                key=f"sample_{idx}"
            ):
                st.session_state.email_input = sample["email"]
                st.rerun()
    
    # Second row of examples (2 buttons)
    cols2 = st.columns(2)
    for idx, sample in enumerate(SAMPLES[3:5]):
        with cols2[idx]:
            if st.button(
                f"{sample['name']}",
                use_container_width=True,
                key=f"sample_{idx+3}"
            ):
                st.session_state.email_input = sample["email"]
                st.rerun()

with col2:
    st.header("🔍 Threat Analysis")
    
    if analyze_btn and raw_email:
        with st.spinner("🤖 Analyzing email with AI..."):
            try:
                # Run the agent
                result = asyncio.run(agent.run(raw_email))
                report: ThreatReport = result.output
                
                # Severity badge with color
                severity_colors = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢"
                }
                
                severity_bg_colors = {
                    "critical": "#ff4444",
                    "high": "#ff8800",
                    "medium": "#ffdd00",
                    "low": "#44ff44"
                }
                
                # Display severity with colored badge
                st.markdown(
                    f"""
                    <div style="background-color: {severity_bg_colors[report.severity]}; 
                                padding: 10px; 
                                border-radius: 5px; 
                                text-align: center;
                                color: black;
                                font-weight: bold;
                                font-size: 1.2em;">
                        {severity_colors[report.severity]} SEVERITY: {report.severity.upper()}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown("")  # Add spacing
                
                # Phishing status
                if report.is_phishing:
                    st.error("⚠️ **This email is likely PHISHING**")
                else:
                    st.success("✅ **This email appears legitimate**")
                
                # Confidence score with progress bar
                st.markdown("### 📊 Confidence Score")
                st.progress(report.confidence_score)
                st.metric("", f"{report.confidence_score:.1%}")
                
                # Attack type
                st.markdown("### 🎯 Attack Type")
                st.code(report.attack_type, language=None)
                
                # Spoofed brand
                if report.spoofed_brand:
                    st.markdown("### 🏷️ Spoofed Brand")
                    st.warning(f"**{report.spoofed_brand}**")
                
                # Red flags
                st.markdown("### 🚩 Red Flags")
                if report.red_flags:
                    for flag in report.red_flags:
                        st.markdown(f"- {flag}")
                else:
                    st.info("No red flags detected")
                
                # Recommended action
                st.markdown("### ✅ Recommended Action")
                st.info(report.recommended_action)
                
                # Explanation
                with st.expander("📝 Detailed Explanation", expanded=False):
                    st.write(report.explanation)
                
                # Timestamp
                st.caption(f"Analyzed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # JSON output (collapsible)
                with st.expander("🔧 Raw JSON Output"):
                    st.json(report.model_dump())
                    
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
    
    elif analyze_btn:
        st.warning("⚠️ Please paste an email to analyze")
    else:
        # Show welcome message when no analysis has been run
        st.info("👈 Paste an email and click **'Analyze'** to get started")
        
        # Show feature highlights
        st.markdown("### Features")
        st.markdown("""
        - 🤖 **AI-Powered Detection** using Groq (LLaMA 3.3 70B)
        - 🔍 **URL Extraction** and suspicious domain checking
        - 📊 **Confidence Scoring** with detailed threat analysis
        - 🚩 **Red Flag Detection** for common phishing patterns
        - 🏷️ **Brand Spoofing** detection (PayPal, Google, etc.)
        - ⚡ **Real-time Analysis** with instant results
        """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray;">
        Built with ❤️ using Pydantic AI, Groq (LLaMA 3.3), and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
