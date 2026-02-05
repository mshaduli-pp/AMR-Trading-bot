import streamlit as st
import random
import time

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Automated Trading Terminal", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #306998; }
    </style>
    """, unsafe_allow_html=True)


# --- 2. LOGIC FUNCTIONS (Python) ---
def get_market_price(last_price):
    """Simulates market volatility."""
    change_pct = random.uniform(-0.03, 0.03)  # Max 3% change
    return last_price * (1 + change_pct)


# --- 3. SIDEBAR INTERFACE (User Inputs) ---
st.sidebar.title("Stay calm working under progress")
init_balance = st.sidebar.number_input("Starting Bank Capital ($)", min_value=100, value=1000)
trade_size = st.sidebar.slider("Trade Size (Units per move)", 1, 10, 1)
ma_window = st.sidebar.selectbox("Moving Average Window", [3, 5, 10, 20], index=1)

# Initialize Session Data (The "Database")
if 'data' not in st.session_state:
    st.session_state.data = []  # Price history
    st.session_state.balance = float(init_balance)
    st.session_state.inventory = 0
    # Log stores lists of [Time, Action, Price] for the table
    st.session_state.logs = [["Time", "Action", "Price"]]

# --- 4. DASHBOARD LAYOUT ---
st.title("Algorithmic Trading Terminal")
st.write("Analyzing real-time price trends using mean Reversion logic...")

# Top Row Metrics
m1, m2, m3, m4 = st.columns(4)
bank_stat = m1.empty()
price_stat = m2.empty()
inv_stat = m3.empty()
profit_stat = m4.empty()

# Main Chart (Streamlit handles line charts from pure Python lists)
chart_container = st.empty()

# Transaction Log Table (Using st.table for pure Python data)
st.subheader("Live Transaction System")
log_table = st.empty()

# --- 5. THE TRADING ENGINE ---
if st.sidebar.button("Launch System"):
    current_price = 100.0

    for i in range(100):  # Runs for 100 data ticks
        # Step A: Data Ingestion
        current_price = get_market_price(current_price)
        st.session_state.data.append(current_price)

        # Step B: Algorithmic Logic
        if len(st.session_state.data) >= ma_window:
            # Calculate Moving Average (Python list slicing and sum)
            moving_avg = sum(st.session_state.data[-ma_window:]) / ma_window

            # Trading Decisions
            action = None

            # Buying Logic: Price is low compared to history
            if current_price < (moving_avg * 0.98) and st.session_state.balance >= (current_price * trade_size):
                cost = current_price * trade_size
                st.session_state.balance -= cost
                st.session_state.inventory += trade_size
                action = "BUY"

            # Selling Logic: Price is high compared to history
            elif current_price > (moving_avg * 1.02) and st.session_state.inventory >= trade_size:
                revenue = current_price * trade_size
                st.session_state.balance += revenue
                st.session_state.inventory -= trade_size
                action = "SELL"

            # Log the trade if an action was taken
            if action:
                # Append log as a list [Time, Action, Price]
                st.session_state.logs.insert(1, [i, action, round(current_price, 2)])

        # Step C: Update Interface Metrics
        bank_stat.metric("Bank Balance", f"${st.session_state.balance:.2f}")
        price_stat.metric("Asset Price", f"${current_price:.2f}", f"{((current_price - 100) / 100) * 100:.1f}%")
        inv_stat.metric("Inventory", f"{st.session_state.inventory} units")

        total_val = st.session_state.balance + (st.session_state.inventory * current_price)
        profit_stat.metric("Net Worth", f"${total_val:.2f}", f"${total_val - init_balance:.2f}")

        # Step D: Update Visuals
        chart_container.line_chart(st.session_state.data)

        # Display the logs using the pure Streamlit table function
        if len(st.session_state.logs) > 1:
            log_table.table(st.session_state.logs[:6])  # Show header row + 5 trades

        time.sleep(0.4)  # Control the "Tick" speed

st.sidebar.info("Click 'Launch' to begin over calculation of the trading suppliers")

if __name__ == "__main__":
    pass  
