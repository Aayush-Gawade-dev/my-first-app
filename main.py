import streamlit as st
from google import genai
from dotenv import load_dotenv
import time

st.set_page_config(
    page_title="Aayush's Assistant",  # Name that appears on the browser tab                              # Optional: Emoji or URL to an image/favicon
    layout="wide"                     # Optional: "centered" or "wide"
)

load_dotenv()

client = genai.Client()



# 2. Custom CSS for Background and Header
def apply_custom_styles():
    st.markdown("""
        <style>
        /* Import Futuristic Font */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;800&display=swap');

        /* Root Variables */
        :root {
            --bg-dark: #0A0D14;
            --accent-cyan: #00F2FE;
            --accent-purple: #4FACFE;
            --glass-bg: rgba(16, 22, 34, 0.65);
            --glass-border: rgba(255, 255, 255, 0.08);
            --text-main: #F1F5F9;
            --text-muted: #94A3B8;
        }

        /* Apply Font & Hide Default Streamlit Header Components */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--text-main);
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
            z-index: 100000;
        }

        /* -------------------------------------------------------------
           BACKGROUND STYLE: AI Ambient Deep Gradient + Glow
        ------------------------------------------------------------- */
        .stApp {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(0, 242, 254, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 25%, rgba(79, 172, 254, 0.10) 0%, transparent 40%),
                radial-gradient(circle at 50% 80%, rgba(112, 0, 255, 0.08) 0%, transparent 50%);
            background-attachment: fixed;
        }

        /* -------------------------------------------------------------
           HEADER STYLE: Glassmorphic Floating Header
        ------------------------------------------------------------- */
        .ai-header {
            position: fixed;
            top: 1.25rem;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 1200px;
            height: 75px;
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1.75rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            z-index: 99999;
        }

        .header-brand {
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }

        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
        }

        .brand-text {
            display: flex;
            flex-direction: column;
        }

        .brand-title {
            font-weight: 800;
            font-size: 1.15rem;
            letter-spacing: -0.01em;
            color: #FFFFFF;
            line-height: 1.2;
        }

        .brand-caption {
            font-size: 0.72rem;
            color: var(--text-muted);
            font-weight: 400;
            margin-top: 1px;
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(0, 242, 254, 0.08);
            border: 1px solid rgba(0, 242, 254, 0.2);
            padding: 0.4rem 0.8rem;
            border-radius: 30px;
            font-size: 0.8rem;
            color: var(--accent-cyan);
            font-weight: 600;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent-cyan);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-cyan);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 242, 254, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(0, 242, 254, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 242, 254, 0); }
        }

        /* Adjust Streamlit main container padding */
        .main .block-container {
            padding-top: 7.5rem !important;
            padding-bottom: 3rem !important;
            max-width: 1100px;
        }
        </style>
    """, unsafe_allow_html=True)

# 3. Component Rendering
def render_header():
    st.markdown("""
        <div class="ai-header">
            <div class="header-brand">
                <div class="logo-icon">✈️</div>
                <div class="brand-text">
                    <span class="brand-title">TRAVEL <span style="color: var(--accent-cyan);">ASSISTANT</span></span>
                    <span class="brand-caption">Smart AI-powered trip planning & itineraries</span>
                </div>
            </div>
            <div class="status-badge">
                <div class="pulse-dot"></div>
                <span>AI Core Active</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Main App Execution
apply_custom_styles()
render_header()




    
destination=st.text_input("Where do you want to go")
days=st.number_input("How many days of trip",min_value=1,max_value=30)
budget=st.selectbox(
    "What is your Budget?",
    options=["Luxuary","Mid-Range","Budget"],
    index=None,  # Optional: keeps the input empty until chosen
    placeholder="Choose a Budget..."
)

partner=st.radio("Who are you travelling with",["Family","Solo","Friends"])

if st.button("PLAN"):
    with st.spinner("Creating Plan..."):
            time.sleep(15)
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        system_instruction="You are an experienced travel planner who properly plans tours and vacations when provided details about travel",
        input=f"I want to plan a trip to {destination} for {days} days also my budget type is {budget} and travelling type is {partner} , so plan a perfect trip for me in bullet format.",
        generation_config={
                            "temperature":0.7,
                            "top_k":40,
                            
                        }
    )

    st.success("Here is Your Travel Plan")     
    st.write("\n")              
    st.write(interaction.output_text)