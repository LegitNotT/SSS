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
        background: rgba(240, 253, 250, 0.3);
        border: 1px solid rgba(20, 184, 166, 0.3);
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
        margin: 5px 0;
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
    
    div[data-testid="stNumberInput"] > div > div > input {
        font-size: 24px;
        text-align: center;
        font-family: monospace;
    }
    
    /* Mobile-friendly number pad using CSS Grid */
    .number-pad-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 20px 0;
        max-width: 300px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .number-pad-btn {
        aspect-ratio: 1;
        min-height: 60px;
        border: none;
        border-radius: 12px;
        background-color: #f3f4f6;
        font-size: 20px;
        font-weight: 800;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .number-pad-btn:hover {
        background-color: #e5e7eb;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .number-pad-btn.delete {
        background-color: #006a50;
        color: white;
    }
    
    .number-pad-btn.delete:hover {
        background-color: #004d3a;
    }
    
    .peacock-green {
        background-color: #006a50 !important;
        color: white !important;
    }
    
    .peacock-green:hover {
        background-color: #004d3a !important;
    }
    
    /* Custom button styling */
    .stButton > button {
        font-weight: 600;
    }
    
    /* Responsive design for mobile */
    @media (max-width: 768px) {
        .main > div {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .number-pad-container {
            max-width: 250px;
            gap: 8px;
        }
        
        .number-pad-btn {
            min-height: 50px;
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
            font-size: 24px;
        }
    }
    
    /* Force Streamlit columns to work better on mobile */
    @media (max-width: 640px) {
        .element-container .row-widget.stSelectbox,
        .element-container .row-widget.stNumberInput {
            width: 100% !important;
        }
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
        st.markdown("### Gold Prices")
        gold_without_gst = st.number_input("Gold Price (without GST) ₹/gram", 
                                          value=st.session_state.prices["goldWithoutGST"],
                                          min_value=0.0, step=1.0, key="gold_no_gst_input")
        
        gold_with_gst = st.number_input("Gold Price (with GST) ₹/gram", 
                                       value=st.session_state.prices["goldWithGST"],
                                       min_value=0.0, step=1.0, key="gold_gst_input")
        
        st.markdown("### Silver Prices")
        silver_without_gst = st.number_input("Silver Price (without GST) ₹/gram", 
                                            value=st.session_state.prices["silverWithoutGST"],
                                            min_value=0.0, step=1.0, key="silver_no_gst_input")
        
        silver_with_gst = st.number_input("Silver Price (with GST) ₹/gram", 
                                         value=st.session_state.prices["silverWithGST"],
                                         min_value=0.0, step=1.0, key="silver_gst_input")
        
        if st.button("Continue", type="primary", use_container_width=True):
            if all([gold_without_gst > 0, gold_with_gst > 0, silver_without_gst > 0, silver_with_gst > 0]):
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

def create_mobile_number_pad():
    """Create a mobile-friendly number pad using HTML/CSS grid"""
    
    # Create the number pad HTML
    number_pad_html = """
    <div class="number-pad-container">
    """
    
    # Numbers 1-9
    for i in range(1, 10):
        number_pad_html += f'<div class="number-pad-btn" onclick="addToWeight(\'{i}\')">{i}</div>'
    
    # Bottom row: decimal, 0, backspace
    number_pad_html += '''
        <div class="number-pad-btn" onclick="addDecimal()">.</div>
        <div class="number-pad-btn" onclick="addToWeight('0')">0</div>
        <div class="number-pad-btn delete" onclick="backspace()">⌫</div>
    </div>
    
    <script>
    function addToWeight(num) {
        const event = new CustomEvent('streamlit:setComponentValue', {
            detail: {
                key: 'number_pad_action',
                value: 'add_' + num
            }
        });
        window.dispatchEvent(event);
        // Also trigger a rerun by clicking a hidden button
        setTimeout(() => {
            const buttons = parent.document.querySelectorAll('button');
            const hiddenButton = Array.from(buttons).find(btn => btn.textContent.includes('_trigger_rerun'));
            if (hiddenButton) hiddenButton.click();
        }, 50);
    }
    
    function addDecimal() {
        const event = new CustomEvent('streamlit:setComponentValue', {
            detail: {
                key: 'number_pad_action',
                value: 'add_decimal'
            }
        });
        window.dispatchEvent(event);
        setTimeout(() => {
            const buttons = parent.document.querySelectorAll('button');
            const hiddenButton = Array.from(buttons).find(btn => btn.textContent.includes('_trigger_rerun'));
            if (hiddenButton) hiddenButton.click();
        }, 50);
    }
    
    function backspace() {
        const event = new CustomEvent('streamlit:setComponentValue', {
            detail: {
                key: 'number_pad_action',
                value: 'backspace'
            }
        });
        window.dispatchEvent(event);
        setTimeout(() => {
            const buttons = parent.document.querySelectorAll('button');
            const hiddenButton = Array.from(buttons).find(btn => btn.textContent.includes('_trigger_rerun'));
            if (hiddenButton) hiddenButton.click();
        }, 50);
    }
    </script>
    '''
    
    st.markdown(number_pad_html, unsafe_allow_html=True)

def calculator_tab():
    """Calculator tab content"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Material Selection
        st.markdown("### Material Selection")
        material_col1, material_col2 = st.columns(2)
        
        with material_col1:
            if st.button("Gold", type="primary" if st.session_state.material == "gold" else "secondary", use_container_width=True):
                st.session_state.material = "gold"
                st.rerun()
        
        with material_col2:
            if st.button("Silver", type="primary" if st.session_state.material == "silver" else "secondary", use_container_width=True):
                st.session_state.material = "silver"
                st.rerun()
        
        # Result Display (moved to top)
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
        
        # GST Toggle
        gst_col1, gst_col2 = st.columns([3, 1])
        with gst_col1:
            st.write("**Include GST**")
        with gst_col2:
            gst_toggle = st.toggle("", value=st.session_state.include_gst, key="gst_toggle")
            if gst_toggle != st.session_state.include_gst:
                st.session_state.include_gst = gst_toggle
                st.rerun()
        
        # Number Pad - Using traditional Streamlit buttons for better reliability
        st.markdown("### Number Pad")
        
        # Create number pad with proper mobile layout
        st.markdown('<div style="max-width: 300px; margin: 0 auto;">', unsafe_allow_html=True)
        
        # Numbers 1-9 in 3x3 grid
        for row in range(3):
            cols = st.columns(3)
            for col_idx in range(3):
                num = row * 3 + col_idx + 1
                with cols[col_idx]:
                    if st.button(str(num), key=f"num_{num}", use_container_width=True, type="secondary"):
                        if st.session_state.weight == "0":
                            st.session_state.weight = str(num)
                        else:
                            st.session_state.weight += str(num)
                        st.rerun()
        
        # Bottom row: decimal, 0, backspace
        cols = st.columns(3)
        with cols[0]:
            if st.button(".", key="decimal", use_container_width=True, type="secondary"):
                if "." not in st.session_state.weight:
                    st.session_state.weight += "."
                    st.rerun()
        with cols[1]:
            if st.button("0", key="zero", use_container_width=True, type="secondary"):
                if st.session_state.weight != "0":
                    st.session_state.weight += "0"
                else:
                    st.session_state.weight = "0"
                st.rerun()
        with cols[2]:
            # Use peacock green for delete button
            delete_css = """
            <style>
            .element-container:has(#backspace) button {
                background-color: #006a50 !important;
                color: white !important;
            }
            .element-container:has(#backspace) button:hover {
                background-color: #004d3a !important;
            }
            </style>
            """
            st.markdown(delete_css, unsafe_allow_html=True)
            if st.button("⌫", key="backspace", use_container_width=True):
                if len(st.session_state.weight) > 1:
                    st.session_state.weight = st.session_state.weight[:-1]
                else:
                    st.session_state.weight = ""
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Calculate Button
        if st.button("Calculate", type="primary", use_container_width=True):
            if st.session_state.weight and st.session_state.weight != "":
                result = calculate_total()
                if result:
                    st.session_state.result = result
                    st.rerun()
        
        # Calculation Preview
        if result:
            preview_text = f"({result['weight']}g × ₹{result['pricePerGram']}/g) + ₹{result['wages']} = ₹{result['total']:,.0f}"
            st.markdown(f'<div class="calculation-preview">{preview_text}</div>', unsafe_allow_html=True)
        
        # Action Buttons (only show when result exists)
        if st.session_state.result:
            st.markdown("### Actions")
            action_col1, action_col2 = st.columns(2)
            
            # Custom CSS for action buttons
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
                    # Save to history
                    new_entry = {
                        **st.session_state.result,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "id": int(datetime.now().timestamp())
                    }
                    st.session_state.history.insert(0, new_entry)
                    save_data("history", st.session_state.history)
                    
                    # Clear inputs
                    st.session_state.weight = ""
                    st.session_state.result = None
                    st.success("Calculation saved to history!")
                    st.rerun()

def wages_tab():
    """Wages/Making Charges tab content"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Making Charges")
        
        # Add new wage entry button
        if st.button("Add New Entry", type="primary", use_container_width=True):
            new_entry = {
                "id": len(st.session_state.wages_list) + 1,
                "srNo": len(st.session_state.wages_list) + 1,
                "material": f"Item {len(st.session_state.wages_list) + 1}",
                "rate": 1000
            }
            st.session_state.wages_list.append(new_entry)
            save_data("wages_list", st.session_state.wages_list)
            st.rerun()
        
        st.markdown("---")
        
        # Display wages list
        for i, wage in enumerate(st.session_state.wages_list):
            is_selected = st.session_state.selected_wage["id"] == wage["id"]
            
            with st.container():
                if is_selected:
                    st.markdown('<div class="wages-item selected">', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="wages-item">', unsafe_allow_html=True)
                
                # Use single column layout on mobile
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
                
                # Action buttons
                button_col1, button_col2 = st.columns(2)
                with button_col1:
                    if st.button("Select", key=f"select_{wage['id']}", disabled=is_selected, use_container_width=True):
                        st.session_state.selected_wage = wage.copy()
                        st.rerun()
                
                with button_col2:
                    if len(st.session_state.wages_list) > 1:
                        # Custom CSS for delete button
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
                            # Reorder serial numbers
                            for j, w in enumerate(st.session_state.wages_list):
                                w["srNo"] = j + 1
                            
                            # Update selected wage if deleted
                            if is_selected and st.session_state.wages_list:
                                st.session_state.selected_wage = st.session_state.wages_list[0]
                            
                            save_data("wages_list", st.session_state.wages_list)
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
        
        # Selected wage info
        if st.session_state.selected_wage:
            st.info(f"**Selected:** {st.session_state.selected_wage['material']} (Amount: ₹{st.session_state.selected_wage['rate']})")

def prices_tab():
    """Prices tab content"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Current Prices")
        
        # Price input selector
        price_options = {
            "Gold (without GST)": "goldWithoutGST",
            "Gold (with GST)": "goldWithGST", 
            "Silver (without GST)": "silverWithoutGST",
            "Silver (with GST)": "silverWithGST"
        }
        
        selected_price = st.selectbox("Select price to edit:", options=list(price_options.keys()))
        price_key = price_options[selected_price]
        
        st.markdown(f"#### Editing: {selected_price}")
        
        # Current value display
        current_value = st.session_state.prices[price_key]
        st.markdown(f"**Current Value: ₹{current_value}/gram**")
        
        # Number input field
        new_value = st.number_input("Enter new price:", value=current_value, min_value=0.0, step=1.0, key=f"price_input_{price_key}")
        
        # Number pad for price input - mobile friendly
        st.markdown("### Number Pad")
        st.markdown('<div style="max-width: 300px; margin: 0 auto;">', unsafe_allow_html=True)
        
        for row in range(3):
            cols = st.columns(3)
            for col_idx in range(3):
                num = row * 3 + col_idx + 1
                with cols[col_idx]:
                    if st.button(str(num), key=f"price_num_{num}_{price_key}", use_container_width=True, type="secondary"):
                        if new_value == 0:
                            new_value = float(str(num))
                        else:
                            new_value = float(str(int(new_value)) + str(num))
                        st.session_state.prices[price_key] = new_value
                        save_data("daily_prices", st.session_state.prices)
                        st.rerun()
        
        # Bottom row: decimal, 0, backspace
        cols = st.columns(3)
        with cols[0]:
            if st.button(".", key=f"price_decimal_{price_key}", use_container_width=True, type="secondary"):
                if "." not in str(new_value):
                    new_value = float(str(int(new_value)) + ".")
                    st.session_state.prices[price_key] = new_value
                    save_data("daily_prices", st.session_state.prices)
                    st.rerun()
        with cols[1]:
            if st.button("0", key=f"price_zero_{price_key}", use_container_width=True, type="secondary"):
                if new_value != 0:
                    new_value = float(str(int(new_value)) + "0")
                else:
                    new_value = 0.0
                st.session_state.prices[price_key] = new_value
                save_data("daily_prices", st.session_state.prices)
                st.rerun()
        with cols[2]:
            # Use peacock green for delete button
            delete_css = f"""
            <style>
            .element-container:has(#price_backspace_{price_key}) button {{
                background-color: #006a50 !important;
                color: white !important;
            }}
            .element-container:has(#price_backspace_{price_key}) button:hover {{
                background-color: #004d3a !important;
            }}
            </style>
            """
            st.markdown(delete_css, unsafe_allow_html=True)
            if st.button("⌫", key=f"price_backspace_{price_key}", use_container_width=True):
                current_str = str(int(new_value))
                if len(current_str) > 1:
                    new_value = float(current_str[:-1]) if current_str[:-1] != '' else 0.0
                else:
                    new_value = 0.0
                st.session_state.prices[price_key] = new_value
                save_data("daily_prices", st.session_state.prices)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Update price if changed through number input
        if new_value != st.session_state.prices[price_key]:
            st.session_state.prices[price_key] = new_value
            save_data("daily_prices", st.session_state.prices)
        
        st.markdown("---")
        
        # Display all current prices
        st.markdown("#### All Current Prices")
        for display_name, key in price_options.items():
            value = st.session_state.prices[key]
            color = "#f59e0b" if "Gold" in display_name else "#6b7280"
            st.markdown(f"**{display_name}:** ₹{value:,.0f}/gram")
        
        st.markdown("---")
        
        # Reset button with peacock green styling
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
            # Clear all button with peacock green styling
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
    
    # Header - moved to header area and aligned left
    st.markdown('''
    <div class="header-title">
        <h1>SSS Jewelry Calculator</h1>
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