import streamlit as st

st.set_page_config(page_title="Surebet & Risk Calculator", layout="centered")
st.title("🎯 Surebet / Profit-Based Bet Calculator")

st.markdown("""
This tool calculates how to place bets on a **two-outcome match** (like cricket or football)  
to either get a **guaranteed profit** (arbitrage), or reach a **target profit** based on your prediction.
""")

# --- Input Section ---
st.markdown("## 💰 Your Input")

base_money = st.number_input("Initial Capital (₹):", min_value=10.0, step=10.0, format="%.2f")
profit_percent = st.number_input("Desired Profit %:", min_value=1.0, max_value=200.0, step=1.0)

st.markdown("## 🏏 Match Info & Odds")

team1 = st.text_input("Team 1 Name", value="India")
team2 = st.text_input("Team 2 Name", value="Australia")

odds1 = st.number_input(f"Odds for {team1}:", min_value=1.01, step=0.01, format="%.2f")
odds2 = st.number_input(f"Odds for {team2}:", min_value=1.01, step=0.01, format="%.2f")

# --- Predictive Input ---
user_pick = st.radio("🤔 Which team do you think will win?", [team1, team2], key="likely_winner")

# --- Arbitrage Logic ---
def calculate_arbitrage(odds1, odds2, base_money, profit_percent):
    target_total = base_money * (1 + profit_percent / 100)

    inv1 = 1 / odds1
    inv2 = 1 / odds2
    total_inv = inv1 + inv2

    if total_inv >= 1:
        return None  # No arbitrage possible

    bet1 = target_total * inv1 / total_inv
    bet2 = target_total * inv2 / total_inv
    invested = bet1 + bet2
    profit = target_total - invested
    profit_percent_actual = (profit / invested) * 100

    return {
        "bet1": round(bet1, 2),
        "bet2": round(bet2, 2),
        "total_invested": round(invested, 2),
        "guaranteed_return": round(target_total, 2),
        "profit": round(profit, 2),
        "profit_percent": round(profit_percent_actual, 2)
    }

# --- Risk Bet Logic ---
def calculate_risk_bet(odds, base_money, desired_profit_percent):
    target_return = base_money * (1 + desired_profit_percent / 100)
    required_bet = target_return / odds
    profit = target_return - required_bet
    return round(required_bet, 2), round(profit, 2)

# --- Arbitrage Info ---
with st.expander("ℹ️ What is needed for arbitrage (surebet)?"):
    st.markdown("""
    A **surebet (arbitrage)** exists if:
    ```
    (1 / Odds for Team 1) + (1 / Odds for Team 2) < 1
    ```
    This means the combined probabilities are less than 100%,
    allowing you to cover both outcomes and still profit.

    🔸 Usually happens across **different bookies** or promotions.
    """)

# --- Calculation Button ---
if st.button("🧮 Calculate"):
    if not (team1 and team2):
        st.warning("Please enter both team names.")
    else:
        result = calculate_arbitrage(odds1, odds2, base_money, profit_percent)

        if result:
            st.success("✅ Arbitrage Found! Guaranteed Profit Possible.")
            st.markdown(f"💸 Bet ₹{result['bet1']} on **{team1}** at {odds1}")
            st.markdown(f"💸 Bet ₹{result['bet2']} on **{team2}** at {odds2}")
            st.markdown("---")
            st.markdown(f"**Total Invested:** ₹{result['total_invested']}")
            st.markdown(f"**Guaranteed Return:** ₹{result['guaranteed_return']}")
            st.markdown(f"**Profit:** ₹{result['profit']} ({result['profit_percent']}%)")
        else:
            st.warning("⚠️ No arbitrage with these odds.")
            odds = odds1 if user_pick == team1 else odds2
            required_bet, expected_profit = calculate_risk_bet(odds, base_money, profit_percent)
            payout = round(required_bet * odds, 2)

            st.info("You can still place a calculated bet based on your prediction:")
            st.markdown(f"💸 Bet ₹{required_bet} on **{user_pick}** at odds {odds}")
            st.markdown(f"💵 Potential Return: ₹{payout}")
            st.markdown(f"📈 Expected Profit (if correct): ₹{expected_profit}")
            st.markdown("⚠️ _Note: This is **not risk-free** — you only profit if your prediction is correct._")
