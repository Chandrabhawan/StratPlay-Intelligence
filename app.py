import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import joblib

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="StratPlay Intelligence 2.0",
    page_icon="🏏",
    layout="wide"
)

# -----------------------------
# LOAD MODEL
# -----------------------------
score_model = joblib.load("./models/score_prediction.pkl")
winner_model = joblib.load("./models/winner_predictor.pkl")
batsman_clusters = pd.read_csv("./models/batsman_clusters.csv")
team_scores = pd.read_csv("./models/team_scores.csv")

# -----------------------------
# TITLE
# -----------------------------
st.title("🏏 StratPlay Intelligence 2.0")
st.subheader("AI-Powered Cricket Decision Intelligence Platform")

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

module = st.sidebar.radio(
    "Choose Purpose",
    [
        "Score Predictor",
        "Match Winner Predictor",
        "Player Segmentation",
        "Performance Forecast"
    ]
)

# ==========================================================
# MODULE 1: SCORE PREDICTOR
# ==========================================================
if module == "Score Predictor":

    st.header("📈 First Innings Score Predictor")

    st.markdown("Predict the final first innings score using live match conditions.")

    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox(
            "Batting Team",
            [
                "Chennai Super Kings",
                "Mumbai Indians",
                "Royal Challengers Bengaluru",
                "Kolkata Knight Riders",
                "Delhi Capitals",
                "Sunrisers Hyderabad",
                "Rajasthan Royals",
                "Punjab Kings",
                "Gujarat Titans",
                "Lucknow Super Giants"
            ]
        )

        bowling_team = st.selectbox(
            "Bowling Team",
            [
                "Chennai Super Kings",
                "Mumbai Indians",
                "Royal Challengers Bengaluru",
                "Kolkata Knight Riders",
                "Delhi Capitals",
                "Sunrisers Hyderabad",
                "Rajasthan Royals",
                "Punjab Kings",
                "Gujarat Titans",
                "Lucknow Super Giants"
            ]
        )

        venue = st.selectbox(
            "Venue",
            [
                "M Chinnaswamy Stadium", 
            "Rajiv Gandhi International Stadium, Uppal", 
            "Maharashtra Cricket Association Stadium", 
            "Saurashtra Cricket Association Stadium", 
            "Holkar Cricket Stadium", 
            "M.Chinnaswamy Stadium", "Wankhede Stadium", 
            "Eden Gardens", 
            "Feroz Shah Kotla", 
            "Punjab Cricket Association IS Bindra Stadium, Mohali", 
            "Green Park", "Punjab Cricket Association IS Bindra Stadium", 
            "Rajiv Gandhi International Stadium", "MA Chidambaram Stadium", 
            "Sawai Mansingh Stadium", 
            "Arun Jaitley Stadium", 
            "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium", 
            "Sheikh Zayed Stadium", 
            "Dubai International Cricket Stadium", 
            "Sharjah Cricket Stadium", 
            "MA Chidambaram Stadium, Chepauk, Chennai", 
            "Wankhede Stadium, Mumbai", 
            "Narendra Modi Stadium, Ahmedabad", 
            "Arun Jaitley Stadium, Delhi", 
            "Zayed Cricket Stadium, Abu Dhabi", 
            "Brabourne Stadium, Mumbai", 
            "Dr DY Patil Sports Academy, Mumbai", 
            "Maharashtra Cricket Association Stadium, Pune", 
            "Eden Gardens, Kolkata", 
            "Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh", 
            "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow", 
            "Rajiv Gandhi International Stadium, Uppal, Hyderabad", 
            "M Chinnaswamy Stadium, Bengaluru", 
            "Barsapara Cricket Stadium, Guwahati", 
            "Sawai Mansingh Stadium, Jaipur", 
            "Himachal Pradesh Cricket Association Stadium, Dharamsala", 
            "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur", 
            "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam", 
            "Punjab Cricket Association Stadium, Mohali", 
            "MA Chidambaram Stadium, Chepauk", 
            "Dr DY Patil Sports Academy", 
            "Newlands", 
            "St George's Park", 
            "Kingsmead", 
            "SuperSport Park", 
            "Buffalo Park", 
            "New Wanderers Stadium", 
            "De Beers Diamond Oval", 
            "OUTsurance Oval", 
            "Brabourne Stadium", 
            "Sardar Patel Stadium, Motera", 
            "Barabati Stadium", 
            "Vidarbha Cricket Association Stadium, Jamtha", 
            "Himachal Pradesh Cricket Association Stadium", 
            "Nehru Stadium", 
            "Subrata Roy Sahara Stadium", 
            "Shaheed Veer Narayan Singh International Stadium", 
            "JSCA International Stadium Complex",
            "Maharaja Yadavindra Singh International Cricket Stadium, New Chandigarh"
            ]
        )

    with col2:
        overs_completed = st.slider(
            "Overs Completed",
            min_value=3.0,
            max_value=20.0,
            value=17.0,
            step=0.1
        )

        current_score = st.number_input(
            "Current Score",
            min_value=0,
            max_value=300,
            value=120
        )

        wickets_fallen = st.slider(
            "Wickets Fallen",
            min_value=0,
            max_value=10,
            value=3
        )

    # Run Rate Calculation
    run_rate = current_score / overs_completed

    st.metric("Current Run Rate", f"{run_rate:.2f}")

    # Prediction
    if st.button("Predict Final Score"):

        input_df = pd.DataFrame({
            "team_batting": [batting_team],
            "team_bowling": [bowling_team],
            "venue": [venue],
            "overs_completed": [overs_completed],
            "current_score": [current_score],
            "wickets_fallen": [wickets_fallen],
            "run_rate": [run_rate]
        })

        prediction = score_model.predict(input_df)

        predicted_score = int(round(prediction[0]))

        st.success(f"🏏 Predicted Final Score: {predicted_score}")

# ==========================================================
# MODULE 2: MATCH WINNER PREDICTOR
# ==========================================================

elif module == "Match Winner Predictor":

    st.header("🏆 Match Winner Predictor")

    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox(
            "Batting Team",
            ["Chennai Super Kings",
                "Mumbai Indians",
                "Royal Challengers Bengaluru",
                "Kolkata Knight Riders",
                "Delhi Capitals",
                "Sunrisers Hyderabad",
                "Rajasthan Royals",
                "Punjab Kings",
                "Gujarat Titans",
                "Lucknow Super Giants"],
            key="bat_team"
        )

        bowling_team = st.selectbox(
            "Bowling Team",
            ["Chennai Super Kings",
                "Mumbai Indians",
                "Royal Challengers Bengaluru",
                "Kolkata Knight Riders",
                "Delhi Capitals",
                "Sunrisers Hyderabad",
                "Rajasthan Royals",
                "Punjab Kings",
                "Gujarat Titans",
                "Lucknow Super Giants"],
            key="bowl_team"
        )

        venue = st.selectbox(
            "Venue",
            [
            "M Chinnaswamy Stadium", 
            "Rajiv Gandhi International Stadium, Uppal", 
            "Maharashtra Cricket Association Stadium", 
            "Saurashtra Cricket Association Stadium", 
            "Holkar Cricket Stadium", 
            "M.Chinnaswamy Stadium", "Wankhede Stadium", 
            "Eden Gardens", 
            "Feroz Shah Kotla", 
            "Punjab Cricket Association IS Bindra Stadium, Mohali", 
            "Green Park", "Punjab Cricket Association IS Bindra Stadium", 
            "Rajiv Gandhi International Stadium", "MA Chidambaram Stadium", 
            "Sawai Mansingh Stadium", 
            "Arun Jaitley Stadium", 
            "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium", 
            "Sheikh Zayed Stadium", 
            "Dubai International Cricket Stadium", 
            "Sharjah Cricket Stadium", 
            "MA Chidambaram Stadium, Chepauk, Chennai", 
            "Wankhede Stadium, Mumbai", 
            "Narendra Modi Stadium, Ahmedabad", 
            "Arun Jaitley Stadium, Delhi", 
            "Zayed Cricket Stadium, Abu Dhabi", 
            "Brabourne Stadium, Mumbai", 
            "Dr DY Patil Sports Academy, Mumbai", 
            "Maharashtra Cricket Association Stadium, Pune", 
            "Eden Gardens, Kolkata", 
            "Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh", 
            "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow", 
            "Rajiv Gandhi International Stadium, Uppal, Hyderabad", 
            "M Chinnaswamy Stadium, Bengaluru", 
            "Barsapara Cricket Stadium, Guwahati", 
            "Sawai Mansingh Stadium, Jaipur", 
            "Himachal Pradesh Cricket Association Stadium, Dharamsala", 
            "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur", 
            "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam", 
            "Punjab Cricket Association Stadium, Mohali", 
            "MA Chidambaram Stadium, Chepauk", 
            "Dr DY Patil Sports Academy", 
            "Newlands", 
            "St George's Park", 
            "Kingsmead", 
            "SuperSport Park", 
            "Buffalo Park", 
            "New Wanderers Stadium", 
            "De Beers Diamond Oval", 
            "OUTsurance Oval", 
            "Brabourne Stadium", 
            "Sardar Patel Stadium, Motera", 
            "Barabati Stadium", 
            "Vidarbha Cricket Association Stadium, Jamtha", 
            "Himachal Pradesh Cricket Association Stadium", 
            "Nehru Stadium", 
            "Subrata Roy Sahara Stadium", 
            "Shaheed Veer Narayan Singh International Stadium", 
            "JSCA International Stadium Complex",
            "Maharaja Yadavindra Singh International Cricket Stadium, New Chandigarh"
            ],
            key="venue"
        )

        

    with col2:
        target = st.number_input("Target", min_value=10, max_value=350, value=180)
        current_score = st.number_input("Current Score", min_value=0, max_value=350, value=120)
        overs_completed = st.slider("Overs Completed", 1.0, 20.0, 15.0, 0.1)
        wickets = st.slider("Wickets Left", 0, 10, 6)

    balls_left = 120 - int(overs_completed * 6)
    runs_left = target - current_score
    crr = current_score / overs_completed
    required_run_rate = (runs_left * 6) / balls_left if balls_left > 0 else 0

    st.metric("Required Run Rate", f"{required_run_rate:.2f}")

    if st.button("Predict Winner"):

    
        input_df = pd.DataFrame({
        'team_batting': [batting_team],
        'team_bowling': [bowling_team],
        'venue' : [venue],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets_left': [wickets],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [required_run_rate]
})

        probs = winner_model.predict_proba(input_df)[0]

        st.success(f"{batting_team}: {round(probs[1]*100)}%")
        st.error(f"{bowling_team}: {round(probs[0]*100)}%")

# ==========================================================
# MODULE 3: PLAYER SEGMENTATION
# ==========================================================


elif module == "Player Segmentation":

    st.header("🧠 Player Segmentation")

    st.markdown(
        """
        Discover player archetypes using:
        - K-Means Clustering
        - Hierarchical Clustering
        """
    )

    clustering_method = st.selectbox(
        "Choose Clustering Method",
        ["K-Means", "Hierarchical"]
    )

    player_name = st.selectbox(
        "Select Player",
        sorted(batsman_clusters['batter'].unique())
    )

    player_data = batsman_clusters[
        batsman_clusters['batter'] == player_name
    ]

    st.subheader(f"📊 {player_name}")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Runs",
        int(player_data['batsman_total_runs'].values[0])
    )

    col2.metric(
        "Strike Rate",
        round(player_data['strike_rate'].values[0], 2)
    )

    col3.metric(
        "Boundary %",
        round(player_data['boundary_percentage'].values[0], 2)
    )

    if clustering_method == "K-Means":

        cluster = player_data['batsman_type'].values[0]

        st.success(f"K-Means Cluster: {cluster}")

    else:

        hierarchical_cluster = player_data['hierarchical_cluster'].values[0]

        st.info(
            f"Hierarchical Cluster Group: {hierarchical_cluster}"
        )

    st.subheader("📈 Cluster Visualization")

    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(
        batsman_clusters['strike_rate'],
        batsman_clusters['batsman_total_runs'],
        c=batsman_clusters['kmeans_cluster']
    )

    ax.set_xlabel("Strike Rate")
    ax.set_ylabel("Total Runs")
    ax.set_title("Player Clusters")

    st.pyplot(fig)



# ==========================================================
# MODULE 4: PERFORMANCE FORECAST
# ==========================================================


elif module == "Performance Forecast":

    st.header("📉 Team Performance Forecasting")

    st.markdown(
        """
        Forecast future team performance using ARIMA Time Series Modeling.
        """
    )

    team_name = st.selectbox(
        "Select Team",
        sorted(team_scores['team_batting'].unique())
    )

    forecast_steps = st.slider(
        "Forecast Next Matches",
        1,
        10,
        5
    )

    team_data = team_scores[
        team_scores['team_batting'] == team_name
    ]

    team_data = team_data.sort_values('match_date')

    series = team_data['total_runs']

    model = ARIMA(series, order=(3,1,1))

    model_fit = model.fit()

    forecast = model_fit.forecast(steps=forecast_steps)

    st.subheader("📈 Forecasted Scores")

    forecast_df = pd.DataFrame({
        "Future Match": range(1, forecast_steps + 1),
        "Predicted Score": forecast.values
    })

    st.dataframe(forecast_df)

    fig, ax = plt.subplots(figsize=(12,6))

    ax.plot(
        series.values,
        label="Historical Scores"
    )

    forecast_index = range(
        len(series),
        len(series) + len(forecast)
    )

    ax.plot(
        forecast_index,
        forecast.values,
        linestyle='dashed',
        label='Forecast'
    )

    ax.set_title(f"{team_name} Performance Forecast")

    ax.set_xlabel("Matches")
    ax.set_ylabel("Runs")

    ax.legend()

    st.pyplot(fig)