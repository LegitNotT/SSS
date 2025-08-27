import streamlit as st
import json
import os
from datetime import datetime, time
import pandas as pd
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="SSS Jewelry Calculator",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling and mobile responsiveness
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #1e3a8a;
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: transparent;
        border-radius: 8px;
        color: #93c5fd;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .price-card {
        background: linear-gradient(135deg, #1e3a8a, #1d4ed8);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .result-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 15px 0;
    }
    
    .calculation-preview {
        background-color: #f9fafb;
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        text-align: center;
        color: #6b7280;
        margin: 10px 0;
    }
    
    .material-toggle {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    
    .history-item {
        background-color: #f9fafb;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #1e3a8a;
    }
    
    .wages-item {
        background-color: #f9fafb;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid transparent;
    }
    
    .wages-item.selected {
        background-color: #eff6ff;
        border-color: #1e3a8a;
    }
    
    .header-title {
        background: linear-gradient(135deg, #1e3a8a, #1d4ed8);
        color: white;
        padding: 15px 20px;
        border-radius: 15px;
        text-align: left;
        margin-bottom: 20px;
    }
    
    .header-title h1 {
        font-size: 32px;
        font-weight: bold;
        margin: 0;
    }
    
    .header-title h1 .small {
        font-size: 20px;
        font-weight: 500;
    }
    
    /* GST Toggle Enhancement */
    .gst-section {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .gst-label {
        font-size: 18px;
        font-weight: 600;
        color: #1e3a8a;
    }
    
    /* Enhanced toggle styling */
    div[data-testid="stToggle"] > div {
        transform: scale(1.3);
    }
    
    div[data-testid="stNumberInput"] > div > div > input {
        font-size: 18px;
        text-align: center;
        font-family: monospace;
        padding: 12px;
    }
    
    /* Number pad improvements for mobile */
    .number-pad-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 20px 0;
        max-width: 300px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .number-btn {
        aspect-ratio: 1;
        min-height: 60px;
        font-size: 20px;
        font-weight: 700;
        border-radius: 12px;
        transition: all 0.1s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .number-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .peacock-green {
        background-color: #006a50 !important;
        color: white !important;
    }
    
    .peacock-green:hover {
        background-color: #004d3a !important;
    }
    
    /* Price input styling */
    .price-input-section {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.1), rgba(29, 78, 216, 0.1));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(30, 58, 138, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* Custom button styling */
    .stButton > button {
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
    }
    
    /* Force number pad to stay in 3 columns on mobile */
    @media (max-width: 768px) {
        .main > div {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .number-pad-grid {
            display: grid !important;
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 10px;
            max-width: 280px;
        }
        
        .number-btn {
            min-height: 55px;
            font-size: 18px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding-left: 10px;
            padding-right: 10px;
            height: 45px;
            font-size: 14px;
        }
        
        .header-title {
            padding: 10px 15px;
        }
        
        .header-title h1 {
            font-size: 28px;
        }
        
        .header-title h1 .small {
            font-size: 18px;
        }
        
        .gst-label {
            font-size: 16px;
        }
    }
    
    /* Ensure columns don't break on small screens */
    @media (max-width: 640px) {
        .element-container .row-widget.stSelectbox,
        .element-container .row-widget.stNumberInput {
            width: 100% !important;
        }
        
        /* Force grid layout even on smallest screens */
        .stColumns > div[data-testid="column"] {
            width: calc(33.333% - 8px) !important;
            min-width: 80px !important;
        }
    }
    
    /* Remove extra spacing in wages section */
    .element-container {
        margin-bottom: 8px !important;
    }
    
    .stMarkdown {
        margin-bottom: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Data persistence functions
def load_data(key: str, default_value):
    """Load data from session state or file"""
    if key not in st.session_state:
        try:
            if os.path.exists(f"{key}.json"):
                with open(f"{key}.json", "r") as f:
                    st.session_state[key] = json.load(f)
            else:
                st.session_state[key] = default_value
        except:
            st.session_state[key] = default_value
    return st.session_state[key]

def save_data(key: str, value):
    """Save data to session state and file"""
    st.session_state[key] = value
    try:
        with open(f"{key}.json", "w") as f:
            json.dump(value, f)
    except:
        pass

def check_daily_price_input():
    """Check if daily price input is needed"""
    last_input_date = load_data("last_input_date", "")
    today = datetime.now().strftime("%Y-%m-%d")
    current_hour = datetime.now().hour
    
    return (not last_input_date or 
            last_input_date != today or 
            (current_hour >= 8 and last_input_date != today))

def initialize_session_state():
    """Initialize all session state variables"""
    
    # Prices
    if "prices" not in st.session_state:
        st.session_state.prices = {
            "goldWithoutGST": 0.0,
            "goldWithGST": 0.0,
            "silverWithoutGST": 0.0,
            "silverWithGST": 0.0
        }
    
    # Load saved prices if available
    saved_prices = load_data("daily_prices", st.session_state.prices)
    st.session_state.prices.update(saved_prices)
    
    # Calculator state
    if "weight" not in st.session_state:
        st.session_state.weight = ""
    if "material" not in st.session_state:
        st.session_state.material = "gold"
    if "include_gst" not in st.session_state:
        st.session_state.include_gst = True
    if "result" not in st.session_state:
        st.session_state.result = None
    
    # Wages list
    default_wages = [{"id": 1, "srNo": 1, "material": "Default", "rate": 1000}]
    st.session_state.wages_list = load_data("wages_list", default_wages)
    
    if "selected_wage" not in st.session_state:
        st.session_state.selected_wage = st.session_state.wages_list[0]
    
    # History
    st.session_state.history = load_data("history", [])
    
    # Show initial input flag
    if "show_initial_input" not in st.session_state:
        st.session_state.show_initial_input = check_daily_price_input()

def daily_price_input():
    """Show daily price input screen"""
    st.markdown('<div class="header-title"><h1>Good Morning!</h1><p>Please enter today\'s prices</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="price-input-section">', unsafe_allow_html=True)
        st.markdown("### Gold Prices")
        gold_without_gst = st.number_input("Gold Price (without GST) ₹/gram", 
                                          value=None if st.session_state.prices["goldWithoutGST"] == 0 else st.session_state.prices["goldWithoutGST"],
                                          placeholder="Enter gold price without GST",
                                          min_value=0.0, step=0.01, key="gold_no_gst_input")
        
        gold_with_gst = st.number_input("Gold Price (with GST) ₹/gram", 
                                       value=None if st.session_state.prices["goldWithGST"] == 0 else st.session_state.prices["goldWithGST"],
                                       placeholder="Enter gold price with GST",
                                       min_value=0.0, step=0.01, key="gold_gst_input")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="price-input-section">', unsafe_allow_html=True)
        st.markdown("### Silver Prices")
        silver_without_gst = st.number_input("Silver Price (without GST) ₹/gram", 
                                            value=None if st.session_state.prices["silverWithoutGST"] == 0 else st.session_state.prices["silverWithoutGST"],
                                            placeholder="Enter silver price without GST",
                                            min_value=0.0, step=0.01, key="silver_no_gst_input")
        
        silver_with_gst = st.number_input("Silver Price (with GST) ₹/gram", 
                                         value=None if st.session_state.prices["silverWithGST"] == 0 else st.session_state.prices["silverWithGST"],
                                         placeholder="Enter silver price with GST",
                                         min_value=0.0, step=0.01, key="silver_gst_input")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Continue", type="primary", use_container_width=True):
            if all([gold_without_gst and gold_without_gst > 0, gold_with_gst and gold_with_gst > 0, 
                   silver_without_gst and silver_without_gst > 0, silver_with_gst and silver_with_gst > 0]):
                st.session_state.prices = {
                    "goldWithoutGST": gold_without_gst,
                    "goldWithGST": gold_with_gst,
                    "silverWithoutGST": silver_without_gst,
                    "silverWithGST": silver_with_gst
                }
                save_data("daily_prices", st.session_state.prices)
                save_data("last_input_date", datetime.now().strftime("%Y-%m-%d"))
                st.session_state.show_initial_input = False
                st.rerun()
            else:
                st.error("Please enter all prices before continuing.")

def get_current_price():
    """Get current price based on material and GST selection"""
    if st.session_state.material == "gold":
        return st.session_state.prices["goldWithGST"] if st.session_state.include_gst else st.session_state.prices["goldWithoutGST"]
    else:
        return st.session_state.prices["silverWithGST"] if st.session_state.include_gst else st.session_state.prices["silverWithoutGST"]

def calculate_total():
    """Calculate total price using (weight * price) + wages formula"""
    if not st.session_state.weight or st.session_state.weight == "":
        return None
    
    try:
        weight_num = float(st.session_state.weight)
        price_per_gram = get_current_price()
        wage_amount = st.session_state.selected_wage["rate"]
        total = (weight_num * price_per_gram) + wage_amount
        
        return {
            "weight": weight_num,
            "pricePerGram": price_per_gram,
            "wages": wage_amount,
            "total": total,
            "material": st.session_state.material,
            "includeGST": st.session_state.include_gst
        }
    except:
        return None

def add_to_weight(value):
    """Add value to weight with instant update"""
    if st.session_state.weight == "0":
        st.session_state.weight = str(value)
    else:
        st.session_state.weight += str(value)

def calculator_tab():
    """Calculator tab content"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Material Selection
        st.markdown("### Material Selection")
        material_col1, material_col2 = st.columns(2)
        
        with material_col1:
            if st.button("Gold", type="primary" if st.session_state.material == "gold" else "secondary", 
                        use_container_width=True, key="gold_btn"):
                st.session_state.material = "gold"
                st.rerun()
        
        with material_col2:
            if st.button("Silver", type="primary" if st.session_state.material == "silver" else "secondary", 
                        use_container_width=True, key="silver_btn"):
                st.session_state.material = "silver"
                st.rerun()
        
        # Result Display
        result = calculate_total()
        if result:
            st.markdown(f'''
            <div class="result-card">
                <p style="color: #1e3a8a; font-size: 14px; margin-bottom: 5px;">Calculated Price</p>
                <div style="font-size: 36px; font-weight: bold; color: #1e3a8a;">₹{result["total"]:,.0f}</div>
            </div>
            ''', unsafe_allow_html=True)
            st.session_state.result = result
        
        # Weight Input
        st.markdown("### Weight (grams)")
        weight_input = st.text_input("", value=st.session_state.weight, placeholder="0", 
                                   key="weight_display", label_visibility="collapsed")
        
        if weight_input != st.session_state.weight:
            st.session_state.weight = weight_input
            st.rerun()
        
        # GST Toggle - Enhanced
        st.markdown('<div class="gst-section">', unsafe_allow_html=True)
        gst_col1, gst_col2 = st.columns([3, 1])
        with gst_col1:
            st.markdown('<div class="gst-label">Include GST</div>', unsafe_allow_html=True)
        with gst_col2:
            gst_toggle = st.toggle("", value=st.session_state.include_gst, key="gst_toggle")
            if gst_toggle != st.session_state.include_gst:
                st.session_state.include_gst = gst_toggle
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Number Pad - Fixed for mobile
        st.markdown("### Number Pad")
        st.markdown('<div class="number-pad-grid">', unsafe_allow_html=True)
        
        # Use manual grid creation to ensure 3 columns always
        for row in range(3):
            cols = st.columns(3)
            for col_idx in range(3):
                num = row * 3 + col_idx + 1
                with cols[col_idx]:
                    button_key = f"num_{num}_{id(st.session_state)}"
                    if st.button(str(num), key=button_key, use_container_width=True, type="secondary"):
                        add_to_weight(num)
                        st.rerun()
        
        # Bottom row
        cols = st.columns(3)
        with cols[0]:
            if st.button(".", key=f"decimal_{id(st.session_state)}", use_container_width=True, type="secondary"):
                if "." not in st.session_state.weight:
                    st.session_state.weight += "."
                    st.rerun()
        with cols[1]:
            if st.button("0", key=f"zero_{id(st.session_state)}", use_container_width=True, type="secondary"):
                add_to_weight("0")
                st.rerun()
        with cols[2]:
            delete_css = f"""
            <style>
            .element-container:has(#backspace_{id(st.session_state)}) button {{
                background-color: #006a50 !important;
                color: white !important;
            }}
            .element-container:has(#backspace_{id(st.session_state)}) button:hover {{
                background-color: #004d3a !important;
            }}
            </style>
            """
            st.markdown(delete_css, unsafe_allow_html=True)
            if st.button("⌫", key=f"backspace_{id(st.session_state)}", use_container_width=True):
                if len(st.session_state.weight) > 1:
                    st.session_state.weight = st.session_state.weight[:-1]
                else:
                    st.session_state.weight = ""
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Calculate Button
        if st.button("Calculate", type="primary", use_container_width=True, key="calc_btn"):
            if st.session_state.weight and st.session_state.weight != "":
                result = calculate_total()
                if result:
                    st.session_state.result = result
                    st.rerun()
        
        # Calculation Preview
        if result:
            preview_text = f"({result['weight']}g × ₹{result['pricePerGram']}/g) + ₹{result['wages']} = ₹{result['total']:,.0f}"
            st.markdown(f'<div class="calculation-preview">{preview_text}</div>', unsafe_allow_html=True)
        
        # Action Buttons
        if st.session_state.result:
            st.markdown("### Actions")
            action_col1, action_col2 = st.columns(2)
            
            action_css = """
            <style>
            .element-container:has(#clear_btn) button {
                background-color: #006a50 !important;
                color: white !important;
            }
            .element-container:has(#clear_btn) button:hover {
                background-color: #004d3a !important;
            }
            .element-container:has(#save_btn) button {
                background-color: #006a50 !important;
                color: white !important;
            }
            .element-container:has(#save_btn) button:hover {
                background-color: #004d3a !important;
            }
            </style>
            """
            st.markdown(action_css, unsafe_allow_html=True)
            
            with action_col1:
                if st.button("Clear", key="clear_btn", use_container_width=True):
                    st.session_state.weight = ""
                    st.session_state.result = None
                    st.rerun()
            
            with action_col2:
                if st.button("Save", key="save_btn", use_container_width=True):
                    new_entry = {
                        **st.session_state.result,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "id": int(datetime.now().timestamp())
                    }
                    st.session_state.history.insert(0, new_entry)
                    save_data("history", st.session_state.history)
                    
                    st.session_state.weight = ""
                    st.session_state.result = None
                    st.success("Calculation saved to history!")
                    st.rerun()

def wages_tab():
    """Wages/Making Charges tab content - Fixed spacing issues"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Making Charges")
        
        if st.button("Add New Entry", type="primary", use_container_width=True, key="add_wage_btn"):
            new_entry = {
                "id": len(st.session_state.wages_list) + 1,
                "srNo": len(st.session_state.wages_list) + 1,
                "material": f"Item {len(st.session_state.wages_list) + 1}",
                "rate": 1000
            }
            st.session_state.wages_list.append(new_entry)
            save_data("wages_list", st.session_state.wages_list)
            st.rerun()
        
        # Display wages list with fixed spacing
        for i, wage in enumerate(st.session_state.wages_list):
            is_selected = st.session_state.selected_wage["id"] == wage["id"]
            
            # Create container without extra spacing
            container = st.container()
            with container:
                if is_selected:
                    st.markdown('<div class="wages-item selected" style="margin-top: 5px; margin-bottom: 5px;">', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="wages-item" style="margin-top: 5px; margin-bottom: 5px;">', unsafe_allow_html=True)
                
                st.write(f"**{wage['srNo']}. {wage['material']}**")
                
                col1_wage, col2_wage = st.columns([2, 1])
                with col1_wage:
                    new_material = st.text_input("Item Name", value=wage["material"], 
                                               key=f"material_{wage['id']}")
                    if new_material != wage["material"]:
                        st.session_state.wages_list[i]["material"] = new_material
                        if is_selected:
                            st.session_state.selected_wage["material"] = new_material
                        save_data("wages_list", st.session_state.wages_list)
                        st.rerun()
                
                with col2_wage:
                    new_rate = st.number_input("Amount ₹", value=wage["rate"], min_value=1,
                                             key=f"rate_{wage['id']}")
                    if new_rate != wage["rate"]:
                        st.session_state.wages_list[i]["rate"] = new_rate
                        if is_selected:
                            st.session_state.selected_wage["rate"] = new_rate
                        save_data("wages_list", st.session_state.wages_list)
                        st.rerun()
                
                button_col1, button_col2 = st.columns(2)
                with button_col1:
                    if st.button("Select", key=f"select_{wage['id']}", disabled=is_selected, use_container_width=True):
                        st.session_state.selected_wage = wage.copy()
                        st.rerun()
                
                with button_col2:
                    if len(st.session_state.wages_list) > 1:
                        delete_css = f"""
                        <style>
                        .element-container:has(#delete_{wage['id']}) button {{
                            background-color: #006a50 !important;
                            color: white !important;
                        }}
                        .element-container:has(#delete_{wage['id']}) button:hover {{
                            background-color: #004d3a !important;
                        }}
                        </style>
                        """
                        st.markdown(delete_css, unsafe_allow_html=True)
                        if st.button("Delete", key=f"delete_{wage['id']}", use_container_width=True):
                            st.session_state.wages_list = [w for w in st.session_state.wages_list if w["id"] != wage["id"]]
                            for j, w in enumerate(st.session_state.wages_list):
                                w["srNo"] = j + 1
                            
                            if is_selected and st.session_state.wages_list:
                                st.session_state.selected_wage = st.session_state.wages_list[0]
                            
                            save_data("wages_list", st.session_state.wages_list)
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.selected_wage:
            st.info(f"**Selected:** {st.session_state.selected_wage['material']} (Amount: ₹{st.session_state.selected_wage['rate']})")

def prices_tab():
    """Renovated Prices tab - Direct input like landing page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Update Daily Prices")
        
        st.markdown('<div class="price-input-section">', unsafe_allow_html=True)
        st.markdown("#### Gold Prices")
        
        gold_without_gst = st.number_input(
            "Gold Price (without GST) ₹/gram", 
            value=None if st.session_state.prices["goldWithoutGST"] == 0 else st.session_state.prices["goldWithoutGST"],
            placeholder="Enter gold price without GST",
            min_value=0.0, 
            step=0.01, 
            key="edit_gold_no_gst"
        )
        
        gold_with_gst = st.number_input(
            "Gold Price (with GST) ₹/gram", 
            value=None if st.session_state.prices["goldWithGST"] == 0 else st.session_state.prices["goldWithGST"],
            placeholder="Enter gold price with GST",
            min_value=0.0, 
            step=0.01, 
            key="edit_gold_gst"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="price-input-section">', unsafe_allow_html=True)
        st.markdown("#### Silver Prices")
        
        silver_without_gst = st.number_input(
            "Silver Price (without GST) ₹/gram", 
            value=None if st.session_state.prices["silverWithoutGST"] == 0 else st.session_state.prices["silverWithoutGST"],
            placeholder="Enter silver price without GST",
            min_value=0.0, 
            step=0.01, 
            key="edit_silver_no_gst"
        )
        
        silver_with_gst = st.number_input(
            "Silver Price (with GST) ₹/gram", 
            value=None if st.session_state.prices["silverWithGST"] == 0 else st.session_state.prices["silverWithGST"],
            placeholder="Enter silver price with GST",
            min_value=0.0, 
            step=0.01, 
            key="edit_silver_gst"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Update button
        if st.button("Update Prices", type="primary", use_container_width=True, key="update_prices_btn"):
            updated = False
            if gold_without_gst and gold_without_gst != st.session_state.prices["goldWithoutGST"]:
                st.session_state.prices["goldWithoutGST"] = gold_without_gst
                updated = True
            if gold_with_gst and gold_with_gst != st.session_state.prices["goldWithGST"]:
                st.session_state.prices["goldWithGST"] = gold_with_gst
                updated = True
            if silver_without_gst and silver_without_gst != st.session_state.prices["silverWithoutGST"]:
                st.session_state.prices["silverWithoutGST"] = silver_without_gst
                updated = True
            if silver_with_gst and silver_with_gst != st.session_state.prices["silverWithGST"]:
                st.session_state.prices["silverWithGST"] = silver_with_gst
                updated = True
                
            if updated:
                save_data("daily_prices", st.session_state.prices)
                st.success("Prices updated successfully!")
                st.rerun()
        
        st.markdown("---")
        
        # Display current prices
        st.markdown("#### Current Active Prices")
        price_display_col1, price_display_col2 = st.columns(2)
        
        with price_display_col1:
            st.markdown("**Gold Prices**")
            st.write(f"Without GST: ₹{st.session_state.prices['goldWithoutGST']:,.2f}/g")
            st.write(f"With GST: ₹{st.session_state.prices['goldWithGST']:,.2f}/g")
        
        with price_display_col2:
            st.markdown("**Silver Prices**")
            st.write(f"Without GST: ₹{st.session_state.prices['silverWithoutGST']:,.2f}/g")
            st.write(f"With GST: ₹{st.session_state.prices['silverWithGST']:,.2f}/g")
        
        st.markdown("---")
        
        # Reset button
        reset_css = """
        <style>
        .element-container:has(#reset_prices) button {
            background-color: #006a50 !important;
            color: white !important;
        }
        .element-container:has(#reset_prices) button:hover {
            background-color: #004d3a !important;
        }
        </style>
        """
        st.markdown(reset_css, unsafe_allow_html=True)
        if st.button("Reset Daily Prices", key="reset_prices", use_container_width=True):
            st.session_state.show_initial_input = True
            st.rerun()

def history_tab():
    """History tab content"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### History")
        
        if st.session_state.history:
            clear_css = """
            <style>
            .element-container:has(#clear_history) button {
                background-color: #006a50 !important;
                color: white !important;
            }
            .element-container:has(#clear_history) button:hover {
                background-color: #004d3a !important;
            }
            </style>
            """
            st.markdown(clear_css, unsafe_allow_html=True)
            if st.button("Clear All History", key="clear_history", use_container_width=True):
                st.session_state.history = []
                save_data("history", [])
                st.rerun()
            
            st.markdown("---")
            
            for entry in st.session_state.history:
                material_color = "#f59e0b" if entry["material"] == "gold" else "#6b7280"
                gst_text = "with GST" if entry["includeGST"] else "without GST"
                
                st.markdown(f'''
                <div class="history-item">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap;">
                        <span style="background-color: {'#fef3c7' if entry['material'] == 'gold' else '#f3f4f6'}; 
                                   color: {'#92400e' if entry['material'] == 'gold' else '#374151'}; 
                                   padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: 600; margin-bottom: 5px;">
                            {entry["material"].upper()} {entry["weight"]}g
                        </span>
                        <span style="font-size: 20px; font-weight: bold;">₹{entry["total"]:,.0f}</span>
                    </div>
                    <div style="font-size: 12px; color: #6b7280;">
                        {entry["timestamp"]} • {gst_text} • Making: ₹{entry["wages"]}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div style="text-align: center; padding: 50px; color: #9ca3af;">
                <div style="font-size: 48px; margin-bottom: 10px;">📊</div>
                <p>No calculations saved</p>
            </div>
            ''', unsafe_allow_html=True)

def main():
    """Main app function"""
    # Initialize session state
    initialize_session_state()
    
    # Show daily price input if needed
    if st.session_state.show_initial_input:
        daily_price_input()
        return
    
    # Enhanced Header with adjusted font sizes
    st.markdown('''
    <div class="header-title">
        <h1>SSS <span class="small">Jewelry Calculator</span></h1>
        <p>Professional jewelry pricing tool</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Tab navigation
    tab1, tab2, tab3, tab4 = st.tabs(["Calculator", "Wages", "Prices", "History"])
    
    with tab1:
        calculator_tab()
    
    with tab2:
        wages_tab()
    
    with tab3:
        prices_tab()
    
    with tab4:
        history_tab()

if __name__ == "__main__":
    main()