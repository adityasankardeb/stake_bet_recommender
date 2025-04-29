import streamlit as st

st.set_page_config(page_title="Surebet / Risk Bet Calculator", layout="centered")
st.title("📊 Surebet / Risk Bet Calculator")

st.markdown("""
This tool helps you determine whether an arbitrage opportunity exists and  
calculates **how to place your bets** across two teams to achieve a **desired profit**,  
even when arbitrage is not possible.
""")

# Inputs
st.header("📝 Enter Match Odds")
team1 = st.text_input("Team 1 Name", value="Team A")
team2 = st.text_input("Team 2 Name", value="Team B")

odds1 = st.number_input(f"Odds for {team1}", min_value=1.01, step=0.01, format="%.2f")
odds2 = st.number_input(f"Odds for {team2}", min_value=1.01, step=0.01, format="%.2f")

st.header("💵 Desired Outcome")
base_money = st.number_input("Total amount you're willing to bet (₹)", min_value=10.0, step=10.0, format="%.2f")
desired_profit_percent = st.number_input("Target Profit Percentage (%)", min_value=1.0, max_value=200.0, value=10.0)

# Check for arbitrage
def check_arbitrage(o1, o2):
    return (1/o1 + 1/o2) < 1

# Smart hedge strategy
def calculate_hedged_bet(predicted_team, o1, o2, capital, target_pct):
    # Assign odds based on user prediction
    if predicted_team == team1:
        pred_odds = o1
        other_odds = o2
    else:
        pred_odds = o2
        other_odds = o1

    target_profit = capital * (target_pct / 100)
    target_return = capital + target_profit

    for b_pred in range(0, int(capital)+1):
        b_other = capital - b_pred
        if b_pred * pred_odds >= target_return:
            return {
                "bet_pred": round(b_pred, 2),
                "bet_other": round(b_other, 2),
                "expected_return": round(b_pred * pred_odds, 2),
                "expected_loss": round(b_other * other_odds, 2),
                "net_profit": round(b_pred * pred_odds - capital, 2)
            }
    # fallback if ideal target not found
    b_pred = int(capital * 0.7)
    b_other = capital - b_pred
    return {
        "bet_pred": round(b_pred, 2),
        "bet_other": round(b_other, 2),
        "expected_return": round(b_pred * pred_odds, 2),
        "expected_loss": round(b_other * other_odds, 2),
        "net_profit": round(b_pred * pred_odds - capital, 2)
    }

# Logic Trigger
if st.button("📈 Calculate Best Bet"):

    if not team1 or not team2:
        st.error("Please enter valid team names.")
    else:
        is_arbitrage = check_arbitrage(odds1, odds2)

        if is_arbitrage:
            st.success("✅ Arbitrage is possible!")
            inv1 = base_money / (1 + (odds1 / odds2))
            inv2 = base_money - inv1
            profit = round(min(inv1 * odds1, inv2 * odds2) - base_money, 2)

            st.markdown(f"💰 Bet ₹{round(inv1, 2)} on **{team1}**")
            st.markdown(f"💰 Bet ₹{round(inv2, 2)} on **{team2}**")
            st.markdown(f"📊 Guaranteed profit: ₹{profit}")
        else:
            st.warning("⚠️ These odds do NOT allow a guaranteed profit (no arbitrage opportunity).")

            predicted_team = st.radio("Who do you believe will win?", [team1, team2], index=0)
            result = calculate_hedged_bet(predicted_team, odds1, odds2, base_money, desired_profit_percent)

            st.markdown(f"🧠 Based on your input and belief:")
            st.markdown(f"👉 Bet ₹{result['bet_pred']} on **{predicted_team}**")
            other_team = team1 if predicted_team == team2 else team2
            st.markdown(f"👉 Bet ₹{result['bet_other']} on **{other_team}**")

            st.markdown("---")
            st.markdown(f"✅ If you're right: Return = ₹{result['expected_return']} | Profit = ₹{result['net_profit']}")
            st.markdown(f"❌ If you're wrong: You get ₹{result['expected_loss']} back (lower than capital)")
