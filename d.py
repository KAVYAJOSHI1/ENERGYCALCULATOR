import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time

# Page configuration
st.set_page_config(
    page_title="EcoCalc Pro | Energy Calculator",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern glassmorphism and animations
st.markdown("""
<style>
    /* Import Font Awesome CSS at the very top of your custom styles */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin: 1rem 0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: slideIn 0.6s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.25), rgba(255,255,255,0.1));
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.3);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .energy-breakdown {
        background: linear-gradient(145deg, rgba(255,255,255,0.2), rgba(255,255,255,0.05));
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .result-panel {
        background: linear-gradient(145deg, #4CAF50, #45a049);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .result-panel::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .stButton > button {
        background: linear-gradient(145deg, #FF6B6B, #FF8E8E);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 3rem;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .sidebar .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .sidebar {
        background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(20px);
    }
    
    .tip-card {
        background: linear-gradient(145deg, rgba(255,193,7,0.2), rgba(255,193,7,0.1));
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #FFC107;
        transition: all 0.3s ease;
    }
    
    .tip-card:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 20px rgba(255,193,7,0.3);
    }
    
    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .floating-circle {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.1), transparent);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .title-gradient {
        background: linear-gradient(45deg, #667eea, #764ba2, #667eea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stProgress .stProgress-bar {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        border-radius: 10px;
    }
    
    .eco-badge {
        background: linear-gradient(145deg, #2E7D32, #388E3C);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3); }
        to { box-shadow: 0 8px 25px rgba(46, 125, 50, 0.6); }
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .stCheckbox > label {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .stCheckbox > label:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Floating background elements
st.markdown("""
<div class="floating-elements">
    <div class="floating-circle" style="width: 100px; height: 100px; top: 10%; left: 10%; animation-delay: 0s;"></div>
    <div class="floating-circle" style="width: 150px; height: 150px; top: 20%; right: 15%; animation-delay: 1s;"></div>
    <div class="floating-circle" style="width: 80px; height: 80px; bottom: 20%; left: 20%; animation-delay: 2s;"></div>
    <div class="floating-circle" style="width: 120px; height: 120px; bottom: 15%; right: 10%; animation-delay: 3s;"></div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🌿 EcoCalc Pro
        </h1>
        <p style="font-size: 1.3rem; font-weight: 300; margin-bottom: 1rem; opacity: 0.9;">
            Advanced Energy Consumption Calculator
        </p>
        <div class="eco-badge">
            Sustainable Living Made Simple
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'total_energy' not in st.session_state:
    st.session_state.total_energy = 0

# Sidebar with glassmorphism
st.sidebar.markdown("""
<div class="glass-card">
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
<div class="glass-card">
    <h2 style="text-align: center; color: white; margin-bottom: 1.5rem;">
        <i class="fas fa-house-chimney"></i> House Configuration
    </h2>
</div>
""", unsafe_allow_html=True)

BHK = st.sidebar.selectbox("🛏️ BHK Type", [1, 2, 3, 4, 5], index=1)

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    <div class="glass-card">
        <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
            <i class="fas fa-plug"></i> Appliance Configuration
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Base consumption calculation
    fans = min(BHK + 1, 6)
    light = min(BHK + 1, 8)
    
    # Display base appliances with progress bars
    st.markdown(f"""
    <div class="energy-breakdown">
        <h3 style="color: white; margin-bottom: 1rem;"><i class="fas fa-home"></i> Base Appliances ({BHK} BHK)</h3>
        <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
            <div><i class="fas fa-fan"></i> <strong>Ceiling Fans:</strong> {fans} units</div>
            <div><i class="fas fa-lightbulb"></i> <strong>LED Lights:</strong> {light} units</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bars for base appliances
    fan_progress = fans / 6
    light_progress = light / 8
    st.progress(fan_progress, text=f"Fan Usage: {fans}/6 units")
    st.progress(light_progress, text=f"Light Usage: {light}/8 units")
    
    # Additional appliances with modern cards
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: white; text-align: center; margin-bottom: 1.5rem;">
            <i class="fas fa-cogs"></i> Additional Appliances
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        use_ac = st.checkbox("❄️ Air Conditioner", value=False)
        ac_count = 0
        if use_ac:
            ac_count = st.number_input("Number of ACs", min_value=1, max_value=5, value=1, key="ac")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        use_wm = st.checkbox("🌊 Washing Machine", value=False)
        wm_count = 0
        if use_wm:
            wm_count = st.number_input("Number of Washing Machines", min_value=1, max_value=3, value=1, key="wm")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        use_fridge = st.checkbox("🧊 Refrigerator", value=False)
        fridge_count = 0
        if use_fridge:
            fridge_count = st.number_input("Number of Refrigerators", min_value=1, max_value=3, value=1, key="fridge")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        use_tv = st.checkbox("📺 Television", value=False)
        tv_count = 0
        if use_tv:
            tv_count = st.number_input("Number of TVs", min_value=1, max_value=5, value=1, key="tv")
        st.markdown('</div>', unsafe_allow_html=True)

# Calculate energy consumption
base_energy = fans * 0.075 + light * 0.012  # More realistic values
ac_energy = ac_count * 1.5 if use_ac else 0
wm_energy = wm_count * 0.5 if use_wm else 0
fridge_energy = fridge_count * 0.15 if use_fridge else 0
tv_energy = tv_count * 0.1 if use_tv else 0
total_energy = base_energy + ac_energy + wm_energy + fridge_energy + tv_energy

# Results section
with col2:
    st.markdown("""
    <div class="glass-card">
        <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
            <i class="fas fa-chart-line"></i> Live Energy Monitor
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-time metrics with animations
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("🔋 Base Energy", f"{base_energy:.2f} kW", help="Fans + Lights")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if use_ac:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("❄️ AC Energy", f"{ac_energy:.2f} kW", f"+{ac_energy:.2f} kW")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if use_wm:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🌊 Washing Machine", f"{wm_energy:.2f} kW", f"+{wm_energy:.2f} kW")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if use_fridge:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🧊 Refrigerator", f"{fridge_energy:.2f} kW", f"+{fridge_energy:.2f} kW")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if use_tv:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📺 Television", f"{tv_energy:.2f} kW", f"+{tv_energy:.2f} kW")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="result-panel">', unsafe_allow_html=True)
    st.metric("⚡ Total Energy", f"{total_energy:.2f} kW", f"{total_energy - base_energy:.2f} kW")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Energy efficiency indicator
    efficiency = "Excellent" if total_energy < 2 else "Good" if total_energy < 4 else "Average" if total_energy < 6 else "High"
    efficiency_color = "#4CAF50" if efficiency == "Excellent" else "#FFC107" if efficiency == "Good" else "#FF9800" if efficiency == "Average" else "#F44336"
    
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0;">
        <span style="background: {efficiency_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
            Efficiency Rating: {efficiency}
        </span>
    </div>
    """, unsafe_allow_html=True)

# Calculate button with animation
if st.button("🚀 Generate Detailed Report", key="calculate"):
    if name and area:
        st.session_state.calculated = True
        st.session_state.total_energy = total_energy
        
        # Add loading animation
        progress_bar = st.progress(0)
        for i in range(100):
            progress_bar.progress(i + 1)
            time.sleep(0.01)
        
        # Results display
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
                <i class="fas fa-chart-area"></i> Comprehensive Energy Analysis
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Create advanced visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Energy Distribution', 'Monthly Cost Breakdown', 'Efficiency Comparison', 'Carbon Footprint'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "indicator"}]]
        )
        
        # Pie chart for energy breakdown
        labels = ['Base (Fans + Lights)', 'Air Conditioner', 'Washing Machine', 'Refrigerator', 'Television']
        values = [base_energy, ac_energy, wm_energy, fridge_energy, tv_energy]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        fig.add_trace(
            go.Pie(labels=labels, values=values, marker_colors=colors, hole=0.5,
                   hovertemplate='<b>%{label}</b><br>Energy: %{value:.2f} kW<br>Percentage: %{percent}<extra></extra>'),
            row=1, col=1
        )
        
        # Bar chart for monthly cost
        monthly_costs = [v * 24 * 30 * 8 for v in values]  # ₹8 per kWh
        fig.add_trace(
            go.Bar(x=labels, y=monthly_costs, marker_color=colors,
                   hovertemplate='<b>%{x}</b><br>Monthly Cost: ₹%{y:.0f}<extra></extra>'),
            row=1, col=2
        )
        
        # Efficiency comparison
        bhk_data = [1, 2, 3, 4, 5]
        avg_consumption = [1.5, 2.8, 4.2, 5.8, 7.5]
        fig.add_trace(
            go.Scatter(x=bhk_data, y=avg_consumption, mode='lines+markers', name='Average',
                       line=dict(color='#95a5a6', width=3)),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=[BHK], y=[total_energy], mode='markers', name='Your Home',
                       marker=dict(color='#e74c3c', size=15)),
            row=2, col=1
        )
        
        # Carbon footprint indicator
        carbon_footprint = total_energy * 24 * 30 * 0.82  # kg CO2 per month
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=carbon_footprint,
                title={'text': "CO₂ Emissions (kg/month)"},
                delta={'reference': 200},
                gauge={'axis': {'range': [None, 500]},
                       'bar': {'color': "#e74c3c"},
                       'steps': [{'range': [0, 150], 'color': "#2ecc71"},
                                 {'range': [150, 300], 'color': "#f39c12"},
                                 {'range': [300, 500], 'color': "#e74c3c"}],
                       'threshold': {'line': {'color': "red", 'width': 4},
                                     'thickness': 0.75, 'value': 300}}
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="🌟 Advanced Energy Analytics Dashboard",
            showlegend=True,
            height=800,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed summary report
        monthly_cost = total_energy * 24 * 30 * 8
        yearly_cost = monthly_cost * 12
        
        st.markdown(f"""
        <div class="result-panel">
            <h2><i class="fas fa-file-alt"></i> Detailed Energy Report</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem;">
                <div>
                    <h3><i class="fas fa-user"></i> Personal Details</h3>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Age:</strong> {age} years</p>
                    <p><strong>Location:</strong> {area}</p>
                    <p><strong>Housing:</strong> {BHK} BHK {schema}</p>
                </div>
                <div>
                    <h3><i class="fas fa-bolt"></i> Energy Consumption</h3>
                    <p><strong>Total Energy:</strong> {total_energy:.2f} kW</p>
                    <p><strong>Monthly Cost:</strong> ₹{monthly_cost:.0f}</p>
                    <p><strong>Yearly Cost:</strong> ₹{yearly_cost:.0f}</p>
                    <p><strong>CO₂ Emissions:</strong> {carbon_footprint:.0f} kg/month</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Energy saving recommendations
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
                <i class="fas fa-lightbulb"></i> Smart Energy Saving Tips
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        tips = [
            "🌟 Switch to LED bulbs - Save up to 80% on lighting costs",
            "🌡️ Set AC temperature to 24-26°C for optimal efficiency",
            "⏰ Use appliances during off-peak hours (11 PM - 6 AM)",
            "🔌 Unplug electronics when not in use - Eliminate phantom loads",
            "🌿 Use natural ventilation and ceiling fans before AC",
            "💧 Use cold water for washing clothes when possible",
            "🏠 Improve home insulation to reduce cooling/heating needs",
            "☀️ Consider solar panels for renewable energy",
        ]
        
        for i, tip in enumerate(tips):
            st.markdown(f"""
            <div class="tip-card">
                <strong>{tip}</strong>
            </div>
            """, unsafe_allow_html=True)
            
        # Environmental impact
        trees_needed = carbon_footprint / 21  # 1 tree absorbs ~21 kg CO2/year
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color: white; text-align: center;">🌳 Environmental Impact</h3>
            <p style="color: white; text-align: center; font-size: 1.2rem;">
                Your monthly energy consumption produces <strong>{carbon_footprint:.0f} kg</strong> of CO₂.<br>
                You would need <strong>{trees_needed:.0f} trees</strong> to offset this carbon footprint!
            </p>
        </div>
        """, unsafe_allow_html=True)
            
    else:
        st.error("⚠️ Please fill in your name and area to generate the report!")

# Footer with modern design
st.markdown("""
<div style="margin-top: 3rem; text-align: center; color: rgba(255,255,255,0.7); padding: 2rem;">
    <hr style="border: 1px solid rgba(255,255,255,0.2); margin: 2rem 0;">
    <p style="font-size: 1.1rem; margin-bottom: 1rem;">
        🌱 <strong>EcoCalc Pro</strong> - Empowering Sustainable Living
    </p>
    <p style="font-size: 0.9rem;">
        &copy; 2025 EcoCalc Pro. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)