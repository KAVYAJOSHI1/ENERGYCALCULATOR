import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import time
from datetime import datetime, timedelta
import calendar

# Page configuration
st.set_page_config(
    page_title="EcoCalc Pro | Advanced Energy Calculator",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with advanced modern design
st.markdown("""
<style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --danger-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --dark-gradient: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.8);
        --shadow-light: 0 8px 32px rgba(0, 0, 0, 0.1);
        --shadow-heavy: 0 20px 60px rgba(0, 0, 0, 0.2);
    }
    
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(0,0,0,0.3), rgba(0,0,0,0.1));
        backdrop-filter: blur(30px);
        border-radius: 30px;
        padding: 4rem 2rem;
        text-align: center;
        color: var(--text-primary);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.1);
        box-shadow: var(--shadow-heavy);
        animation: heroFloat 6s ease-in-out infinite;
    }
    
    @keyframes heroFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, rgba(255,255,255,0.1) 0deg, transparent 60deg, rgba(255,255,255,0.1) 120deg, transparent 180deg, rgba(255,255,255,0.1) 240deg, transparent 300deg, rgba(255,255,255,0.1) 360deg);
        animation: rotate 20s linear infinite;
        opacity: 0.3;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #fff, #f0f0f0, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: titleShine 3s ease-in-out infinite;
    }
    
    @keyframes titleShine {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(25px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-light);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.6s ease;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: var(--shadow-heavy);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.25), rgba(255,255,255,0.1));
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.3);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
        transition: all 0.4s ease;
        transform: translate(-50%, -50%);
        border-radius: 50%;
    }
    
    .metric-card:hover::after {
        width: 300px;
        height: 300px;
    }
    
    .metric-card:hover {
        transform: scale(1.05) rotate(1deg);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    .appliance-scheduler {
        background: linear-gradient(145deg, rgba(255,255,255,0.2), rgba(255,255,255,0.05));
        backdrop-filter: blur(25px);
        border-radius: 25px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: var(--shadow-light);
    }
    
    .day-toggle {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        color: var(--text-primary);
        user-select: none;
    }
    
    .day-toggle:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .day-toggle.active {
        background: var(--success-gradient);
        border-color: rgba(79, 172, 254, 0.5);
        color: white;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
    }
    
    .day-toggle.inactive {
        background: var(--danger-gradient);
        border-color: rgba(250, 112, 154, 0.5);
        color: white;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(250, 112, 154, 0.3);
    }
    
    .result-panel {
        background: var(--success-gradient);
        color: white;
        padding: 2.5rem;
        border-radius: 25px;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(79, 172, 254, 0.3);
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .result-panel::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: resultPulse 4s ease-in-out infinite;
    }
    
    @keyframes resultPulse {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.3; }
        50% { transform: scale(1.1) rotate(180deg); opacity: 0.6; }
    }
    
    .stButton > button {
        background: var(--secondary-gradient);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 3rem;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        transform: translate(-50%, -50%);
        border-radius: 50%;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 20px 50px rgba(240, 147, 251, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(1);
    }
    
    .floating-particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        animation: float 15s infinite linear;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    .energy-wave {
        position: relative;
        overflow: hidden;
    }
    
    .energy-wave::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(79, 172, 254, 0.3), transparent);
        animation: wave 2s infinite;
    }
    
    @keyframes wave {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .efficiency-badge {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: badgeGlow 3s ease-in-out infinite;
        border: 2px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    @keyframes badgeGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(79, 172, 254, 0.3); }
        50% { box-shadow: 0 0 30px rgba(79, 172, 254, 0.6); }
    }
    
    .appliance-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .appliance-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .appliance-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }
    
    .schedule-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .tip-card {
        background: linear-gradient(145deg, rgba(255,193,7,0.2), rgba(255,193,7,0.1));
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #FFC107;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .tip-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #FFC107, #FFE082);
        animation: tipGlow 2s ease-in-out infinite;
    }
    
    @keyframes tipGlow {
        0%, 100% { box-shadow: 0 0 10px rgba(255, 193, 7, 0.5); }
        50% { box-shadow: 0 0 20px rgba(255, 193, 7, 0.8); }
    }
    
    .tip-card:hover {
        transform: translateX(10px);
        box-shadow: 0 10px 30px rgba(255, 193, 7, 0.3);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-item {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-item:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .progress-ring {
        width: 120px;
        height: 120px;
        margin: 0 auto 1rem;
        position: relative;
    }
    
    .progress-ring svg {
        transform: rotate(-90deg);
    }
    
    .progress-ring-circle {
        stroke: rgba(255, 255, 255, 0.2);
        stroke-width: 8;
        fill: transparent;
        r: 50;
        cx: 60;
        cy: 60;
    }
    
    .progress-ring-progress {
        stroke: #4facfe;
        stroke-width: 8;
        fill: transparent;
        r: 50;
        cx: 60;
        cy: 60;
        stroke-dasharray: 314;
        stroke-dashoffset: 314;
        transition: stroke-dashoffset 0.5s ease;
    }
    
    .sidebar {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        border-radius: 0 25px 25px 0;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .sidebar .stNumberInput > div > div > input,
    .sidebar .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .sidebar .stCheckbox > label {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .sidebar .stCheckbox > label:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.02);
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in-left {
        animation: slideInLeft 0.6s ease-out;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .slide-in-right {
        animation: slideInRight 0.6s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .bounce-in {
        animation: bounceIn 0.8s ease-out;
    }
    
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .data-table {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .data-table th {
        background: rgba(255, 255, 255, 0.2);
        color: var(--text-primary);
        font-weight: 600;
        padding: 1rem;
        text-align: center;
    }
    
    .data-table td {
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-secondary);
        padding: 0.75rem;
        text-align: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .data-table tr:hover td {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .loading-spinner {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-top: 4px solid #4facfe;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--success-gradient);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: slideInNotification 0.3s ease-out;
    }
    
    @keyframes slideInNotification {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
</style>
""", unsafe_allow_html=True)

# Floating particles animation
particles_html = """
<div class="floating-particles">
""" + "".join([f'<div class="particle" style="left: {np.random.randint(0, 100)}%; animation-delay: {np.random.randint(0, 15)}s; animation-duration: {np.random.randint(10, 20)}s;"></div>' for _ in range(50)]) + """
</div>
"""
st.markdown(particles_html, unsafe_allow_html=True)

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'total_energy' not in st.session_state:
    st.session_state.total_energy = 0
if 'appliance_schedule' not in st.session_state:
    st.session_state.appliance_schedule = {
        'ac': [True] * 7,
        'washing_machine': [True] * 7,
        'refrigerator': [True] * 7,
        'television': [True] * 7
    }

# Hero Section
st.markdown("""
<div class="hero-section fade-in">
    <div class="hero-content">
        <h1 class="hero-title">
            🌿 EcoCalc Pro
        </h1>
        <p style="font-size: 1.4rem; font-weight: 400; margin-bottom: 2rem; opacity: 0.9;">
            Advanced Energy Consumption Calculator with Smart Scheduling
        </p>
        <div class="efficiency-badge">
            <i class="fas fa-leaf"></i> Sustainable Living Made Smart
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced glassmorphism
st.sidebar.markdown("""
<div class="glass-card slide-in-left">
    <h2 style="text-align: center; color: white; margin-bottom: 1.5rem;">
        <i class="fas fa-user-circle"></i> Personal Information
    </h2>
</div>
""", unsafe_allow_html=True)

name = st.sidebar.text_input("🏷️ Full Name", placeholder="Enter your full name")
age = st.sidebar.number_input("📅 Age", min_value=18, max_value=100, value=25)
area = st.sidebar.text_input("📍 Location", placeholder="City, State, Country")
schema = st.sidebar.selectbox("🏘️ Housing Type", ["Apartment", "Independent House", "Villa", "Flat"])

st.sidebar.markdown("""
<div class="glass-card slide-in-left">
    <h2 style="text-align: center; color: white; margin-bottom: 1.5rem;">
        <i class="fas fa-house-chimney"></i> House Configuration
    </h2>
</div>
""", unsafe_allow_html=True)

BHK = st.sidebar.selectbox("🛏️ BHK Type", [1, 2, 3, 4, 5], index=1)

# Days of the week
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    <div class="glass-card slide-in-left">
        <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
            <i class="fas fa-plug"></i> Appliance Configuration
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Base consumption calculation
    fans = min(BHK + 1, 6)
    light = min(BHK + 1, 8)
    
    # Display base appliances with enhanced progress bars
    st.markdown(f"""
    <div class="appliance-scheduler fade-in">
        <h3 style="color: white; margin-bottom: 1rem; text-align: center;">
            <i class="fas fa-home"></i> Base Appliances ({BHK} BHK)
        </h3>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="appliance-icon">🌀</div>
                <div class="stat-value">{fans}</div>
                <div class="stat-label">Ceiling Fans</div>
            </div>
            <div class="stat-item">
                <div class="appliance-icon">💡</div>
                <div class="stat-value">{light}</div>
                <div class="stat-label">LED Lights</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced progress visualization
    fan_progress = fans / 6
    light_progress = light / 8
    
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <span style="color: white; font-weight: 600;">Fan Usage</span>
            <span style="color: white; font-weight: 600;">{fans}/6</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 12px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #4facfe, #00f2fe); height: 100%; width: {fan_progress*100}%; border-radius: 10px; transition: width 0.5s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <span style="color: white; font-weight: 600;">Light Usage</span>
            <span style="color: white; font-weight: 600;">{light}/8</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 12px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #43e97b, #38f9d7); height: 100%; width: {light_progress*100}%; border-radius: 10px; transition: width 0.5s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="appliance-scheduler fade-in">
        <h3 style="color: white; margin-bottom: 1rem; text-align: center;">
            <i class="fas fa-bolt"></i> Other Appliances
        </h3>
    </div>
    """, unsafe_allow_html=True)

    # Dictionary to store appliance details: {Appliance: [Power (Watts), Default Daily Hours]}
    appliances_data = {
        "Air Conditioner": [1500, 8, "ac", "fas fa-fan"],
        "Washing Machine": [2000, 2, "washing_machine", "fas fa-washer"],
        "Refrigerator": [150, 24, "refrigerator", "fas fa-refrigerator"],
        "Television": [100, 6, "television", "fas fa-tv"],
        "Microwave Oven": [1000, 0.5, "microwave_oven", "fas fa-microwave"],
        "Water Heater": [2000, 1, "water_heater", "fas fa-hot-tub"],
        "Computer/Laptop": [75, 8, "computer", "fas fa-laptop"],
        "Iron": [1000, 0.2, "iron", "fas fa-shirt"],
        "Toaster": [900, 0.1, "toaster", "fas fa-bread-slice"],
        "Hair Dryer": [1800, 0.1, "hair_dryer", "fas fa-wind"]
    }

    appliances = {}
    for i, (appliance_name, (power, default_hours, key, icon)) in enumerate(appliances_data.items()):
        col_app_1, col_app_2, col_app_3 = st.columns([1, 1, 2])
        with col_app_1:
            st.markdown(f'<div class="appliance-card bounce-in"><div class="appliance-icon"><i class="{icon}"></i></div><h4 style="color: white; text-align: center;">{appliance_name}</h4></div>', unsafe_allow_html=True)
        with col_app_2:
            # Ensure the key for number_input is unique
            appliances[appliance_name] = st.number_input(f"Power (Watts) for {appliance_name}", min_value=1, value=power, key=f"{key}_power_{i}")
        with col_app_3:
            st.markdown(f'<p style="color: white; margin-bottom: 0.5rem;">Daily Usage (hours)</p>', unsafe_allow_html=True)
            # Ensure the key for slider is unique
            usage_hours = st.slider(f"Daily Usage (hours) for {appliance_name}", min_value=0.0, max_value=24.0, value=float(default_hours), step=0.1, key=f"{key}_hours_{i}")
            
            # Smart scheduling for selected appliances
            if key in st.session_state.appliance_schedule:
                st.markdown(f'<p style="color: white; margin-top: 1rem; margin-bottom: 0.5rem;">Schedule for {appliance_name}</p>', unsafe_allow_html=True)
                cols_days = st.columns(7)
                for j, day in enumerate(days):
                    with cols_days[j]:
                        # Use a unique key for the button to avoid conflicts
                        button_clicked = st.button(f"{day[:3]}", key=f"{key}_day_button_{j}_{i}", help=f"Toggle {appliance_name} on/off for {day}")
                        if button_clicked:
                            st.session_state.appliance_schedule[key][j] = not st.session_state.appliance_schedule[key][j]
                            # Rerun to update the button's visual state immediately
                            st.rerun() 
                        
                        is_active = st.session_state.appliance_schedule[key][j]
                        # This markdown is for the visual toggle, not the button itself
                        st.markdown(f'<div class="day-toggle {"active" if is_active else "inactive"}">{day[:3]}</div>', unsafe_allow_html=True)
                appliances[appliance_name] = (appliances[appliance_name], usage_hours)
            else:
                appliances[appliance_name] = (appliances[appliance_name], usage_hours)
        st.markdown("---")


with col2:
    st.markdown("""
    <div class="glass-card slide-in-right">
        <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
            <i class="fas fa-dollar-sign"></i> Cost and Tariff
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    cost_per_unit = st.number_input("💸 Cost per Unit (INR/kWh)", min_value=0.1, value=7.5, step=0.1)
    
    st.markdown("""
    <div class="glass-card slide-in-right">
        <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
            <i class="fas fa-sun"></i> Solar Panel Information (Optional)
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    has_solar = st.checkbox("☀️ Do you have solar panels?", False)
    solar_panel_capacity = 0.0
    daily_sunlight_hours = 0.0
    if has_solar:
        solar_panel_capacity = st.number_input("⚡ Solar Panel Capacity (kWp)", min_value=0.1, value=3.0, step=0.1)
        daily_sunlight_hours = st.number_input("⏳ Average Daily Sunlight Hours", min_value=1.0, max_value=12.0, value=5.0, step=0.1)

    st.markdown("""
    <div class="glass-card slide-in-right">
        <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
            <i class="fas fa-chart-line"></i> Historical Data Insights
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload your past electricity bill data (CSV)", type="csv")
    historical_data = None
    if uploaded_file is not None:
        try:
            historical_data = pd.read_csv(uploaded_file)
            st.success("CSV file uploaded successfully!")
            st.dataframe(historical_data.head(), use_container_width=True)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

# Calculation Logic
def calculate_energy_consumption(fans, light, appliances, days, appliance_schedule):
    total_daily_energy = 0
    detailed_consumption = {}
    
    # Base appliances
    # Assuming avg fan power 75W, avg LED light 10W
    total_daily_energy += (fans * 75 * 12) / 1000  # 12 hours usage for fans
    detailed_consumption["Ceiling Fans"] = (fans * 75 * 12) / 1000
    total_daily_energy += (light * 10 * 8) / 1000   # 8 hours usage for lights
    detailed_consumption["LED Lights"] = (light * 10 * 8) / 1000

    for appliance_name, (power, hours) in appliances.items():
        daily_appliance_energy = 0
        
        # Check if the appliance is in the schedule and calculate average daily usage
        key = None
        if appliance_name == "Air Conditioner": key = "ac"
        elif appliance_name == "Washing Machine": key = "washing_machine"
        elif appliance_name == "Refrigerator": key = "refrigerator"
        elif appliance_name == "Television": key = "television"
        
        if key and key in appliance_schedule:
            active_days_count = sum(1 for status in appliance_schedule[key] if status)
            if active_days_count > 0:
                # Average daily hours based on schedule
                avg_daily_hours = (hours * active_days_count) / 7
                daily_appliance_energy = (power * avg_daily_hours) / 1000
            else:
                daily_appliance_energy = 0 # Appliance is not used on any day
        else:
            daily_appliance_energy = (power * hours) / 1000
            
        total_daily_energy += daily_appliance_energy
        detailed_consumption[appliance_name] = daily_appliance_energy
            
    return total_daily_energy, detailed_consumption

# Buttons for calculation and reset
st.markdown("---")
col_calc_btn, col_reset_btn = st.columns([1, 1])

with col_calc_btn:
    # Use st.button directly for cleaner interaction
    if st.button("Calculate Consumption", key="calculate_button", help="Click to calculate your energy consumption"):
        st.session_state.calculated = True
        st.rerun() # Rerun to trigger the calculation and display results

with col_reset_btn:
    # Use st.button directly for cleaner interaction
    if st.button("Reset", key="reset_button", help="Click to reset all inputs and calculations"):
        st.session_state.calculated = False
        st.session_state.total_energy = 0
        st.session_state.appliance_schedule = {
            'ac': [True] * 7,
            'washing_machine': [True] * 7,
            'refrigerator': [True] * 7,
            'television': [True] * 7
        }
        st.rerun() # Rerun the app to reset all inputs

if st.session_state.calculated:
    st.markdown("""
    <div class="loading-spinner"></div>
    <p style="text-align: center; color: white; margin-top: 1rem;">Calculating your energy footprint...</p>
    """, unsafe_allow_html=True)
    time.sleep(1) # Simulate calculation time

    total_daily_energy_kwh, detailed_consumption = calculate_energy_consumption(fans, light, appliances, days, st.session_state.appliance_schedule)

    # Solar energy generation
    daily_solar_generation = 0
    if has_solar:
        daily_solar_generation = solar_panel_capacity * daily_sunlight_hours
    
    net_daily_energy_kwh = total_daily_energy_kwh - daily_solar_generation
    net_monthly_energy_kwh = net_daily_energy_kwh * 30.44  # Average days in a month
    
    monthly_bill = net_monthly_energy_kwh * cost_per_unit
    
    st.session_state.total_energy = net_monthly_energy_kwh # Update session state

    st.markdown("---")
    st.markdown("""
    <div class="result-panel bounce-in">
        <h2 style="color: white; margin-bottom: 1.5rem;"><i class="fas fa-chart-bar"></i> Your Energy Report</h2>
    """, unsafe_allow_html=True)

    col_result_1, col_result_2, col_result_3 = st.columns(3)
    with col_result_1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: var(--text-primary);">Daily Consumption</h3>
            <p style="font-size: 2.5rem; font-weight: 700; color: var(--text-primary); margin-top: 0.5rem;">{net_daily_energy_kwh:.2f} kWh</p>
            <p style="color: var(--text-secondary);">Estimated per day</p>
        </div>
        """, unsafe_allow_html=True)
    with col_result_2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: var(--text-primary);">Monthly Consumption</h3>
            <p style="font-size: 2.5rem; font-weight: 700; color: var(--text-primary); margin-top: 0.5rem;">{net_monthly_energy_kwh:.2f} kWh</p>
            <p style="color: var(--text-secondary);">Estimated per month</p>
        </div>
        """, unsafe_allow_html=True)
    with col_result_3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: var(--text-primary);">Estimated Monthly Bill</h3>
            <p style="font-size: 2.5rem; font-weight: 700; color: var(--text-primary); margin-top: 0.5rem;">₹ {monthly_bill:.2f}</p>
            <p style="color: var(--text-secondary);">Based on your inputs</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="glass-card slide-in-left">
        <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
            <i class="fas fa-chart-pie"></i> Detailed Appliance Breakdown
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Prepare data for Plotly pie chart
    appliance_df = pd.DataFrame(detailed_consumption.items(), columns=['Appliance', 'Daily_Consumption_kWh'])
    
    # Exclude items with zero consumption for cleaner visualization
    appliance_df = appliance_df[appliance_df['Daily_Consumption_kWh'] > 0]

    if not appliance_df.empty:
        fig_pie = px.pie(appliance_df, values='Daily_Consumption_kWh', names='Appliance',
                         title='Daily Energy Consumption by Appliance',
                         color_discrete_sequence=px.colors.sequential.RdPu,
                         hole=0.4)
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=24,
            title_x=0.5,
            legend_title_font_color='white'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No appliance consumption data to display for the pie chart.")

    # Bar chart for daily consumption
    fig_bar = px.bar(appliance_df, x='Appliance', y='Daily_Consumption_kWh',
                     title='Daily Energy Consumption per Appliance',
                     color='Appliance',
                     color_discrete_sequence=px.colors.sequential.Viridis)
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=24,
        title_x=0.5,
        xaxis_title="Appliance",
        yaxis_title="Daily Consumption (kWh)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <div class="glass-card slide-in-left">
        <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
            <i class="fas fa-lightbulb"></i> Eco-Tips for Energy Saving
        </h2>
    </div>
    """, unsafe_allow_html=True)

    eco_tips = [
        "Unplug electronics when not in use to avoid phantom load.",
        "Use natural light as much as possible to reduce lighting needs.",
        "Ensure your refrigerator coils are clean and not blocked for optimal efficiency.",
        "Wash clothes in cold water and only when you have a full load.",
        "Set your AC to a comfortable but energy-efficient temperature (e.g., 24-26°C).",
        "Consider switching to energy-efficient appliances with high star ratings.",
        "Insulate your home properly to reduce heating and cooling costs.",
        "Take shorter showers to save hot water and energy.",
        "Use LED bulbs throughout your home; they consume significantly less energy.",
        "Regularly clean or replace air filters in your AC unit for better performance."
    ]

    for i, tip in enumerate(eco_tips):
        st.markdown(f'<div class="tip-card fade-in"><i class="fas fa-info-circle" style="color: #FFC107; margin-right: 10px;"></i> {tip}</div>', unsafe_allow_html=True)

    # Historical Data Analysis (if uploaded)
    if historical_data is not None:
        st.markdown("---")
        st.markdown("""
        <div class="glass-card slide-in-left">
            <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
                <i class="fas fa-history"></i> Historical Consumption Analysis
            </h2>
        </div>
        """, unsafe_allow_html=True)

        try:
            # Assuming 'Date' and 'Consumption_kWh' columns exist
            historical_data['Date'] = pd.to_datetime(historical_data['Date'])
            historical_data = historical_data.sort_values('Date')

            fig_hist = px.line(historical_data, x='Date', y='Consumption_kWh',
                               title='Historical Electricity Consumption',
                               labels={'Consumption_kWh': 'Consumption (kWh)'},
                               line_shape="spline", render_mode="svg")
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=24,
                title_x=0.5,
                xaxis_title="Date",
                yaxis_title="Consumption (kWh)"
            )
            st.plotly_chart(fig_hist, use_container_width=True)

            st.markdown("""
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">
                        <i class="fas fa-calendar-alt"></i>
                        {:.2f} kWh
                    </div>
                    <div class="stat-label">Average Monthly Historical</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">
                        <i class="fas fa-chart-line"></i>
                        {:.2f} kWh
                    </div>
                    <div class="stat-label">Min Monthly Historical</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">
                        <i class="fas fa-chart-line"></i>
                        {:.2f} kWh
                    </div>
                    <div class="stat-label">Max Monthly Historical</div>
                </div>
            </div>
            """.format(historical_data['Consumption_kWh'].mean(),
                       historical_data['Consumption_kWh'].min(),
                       historical_data['Consumption_kWh'].max()), unsafe_allow_html=True)

        except KeyError:
            st.warning("Please ensure your CSV has 'Date' and 'Consumption_kWh' columns for historical analysis.")
        except Exception as e:
            st.error(f"An error occurred during historical data analysis: {e}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-top: 3rem;">
        Made with ❤️ by Kavya Joshi | &copy; 2025 EcoCalc Pro. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

    # Simple notification when calculation is done
    st.markdown("""
    <div class="notification slide-in-notification">
        <i class="fas fa-check-circle" style="margin-right: 10px;"></i> Calculation Complete!
    </div>
    """, unsafe_allow_html=True)
