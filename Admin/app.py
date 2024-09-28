import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BASE_URL = "http://localhost:5000"

def fetch_users():
    response = requests.get(f"{BASE_URL}/users")
    if response.status_code == 200:
        return response.json()
    return []

def fetch_user_stats(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}/stats")
    if response.status_code == 200:
        return response.json()
    return None

def main():
    st.title("Admin Dashboard")

    # Fetch and display the user list
    users = fetch_users()
    user_emails = [user['email'] for user in users]

    selected_user = st.selectbox("Select a user to view stats", options=user_emails)

    # Once a user is selected, fetch and display their stats
    if selected_user:
        user_id = next(user['id'] for user in users if user['email'] == selected_user)
        user_stats = fetch_user_stats(user_id)

        if user_stats:
            st.write(f"User Stats for {selected_user}")

            # Display general stats
            st.metric("Total API Calls", user_stats['total_api_calls'])
            st.metric("Total Prompt Tokens", user_stats['total_prompt_tokens'])
            st.metric("Total Completion Tokens", user_stats['total_completion_tokens'])

            # Show breadcrumb structure
            st.markdown("**User Stats** > **API Usage**")

            # Convert API usage data to a DataFrame
            api_usage_df = pd.DataFrame(user_stats['api_usage'])
            if not api_usage_df.empty:
                api_usage_df['created_at'] = pd.to_datetime(api_usage_df['created_at'])

                # 2x2 grid layout for graphs
                col1, col2 = st.columns(2)

                # Line chart - Total tokens used over time
                with col1:
                    fig_line = px.line(api_usage_df, x='created_at', y=api_usage_df['api_response'].apply(lambda x: x['usage']['total_tokens']),
                                       title='Total Tokens Used Over Time')
                    st.plotly_chart(fig_line, use_container_width=True)

                # Bar chart - API calls over time
                with col2:
                    fig_bar = px.bar(api_usage_df, x='created_at', y=api_usage_df['api_response'].apply(lambda x: x['usage']['total_tokens']),
                                     title='API Calls Over Time')
                    st.plotly_chart(fig_bar, use_container_width=True)

                # Pie chart - Distribution of Prompt vs. Completion tokens
                with col1:
                    total_prompt_tokens = sum(api_usage_df['api_response'].apply(lambda x: x['usage']['prompt_tokens']))
                    total_completion_tokens = sum(api_usage_df['api_response'].apply(lambda x: x['usage']['completion_tokens']))
                    fig_pie = px.pie(values=[total_prompt_tokens, total_completion_tokens], 
                                     names=['Prompt Tokens', 'Completion Tokens'],
                                     title='Distribution of Prompt vs. Completion Tokens')
                    st.plotly_chart(fig_pie, use_container_width=True)

                # Area chart - Cumulative token usage over time
                with col2:
                    api_usage_df['cumulative_tokens'] = api_usage_df['api_response'].apply(lambda x: x['usage']['total_tokens']).cumsum()
                    fig_area = px.area(api_usage_df, x='created_at', y='cumulative_tokens', 
                                       title='Cumulative Token Usage Over Time')
                    st.plotly_chart(fig_area, use_container_width=True)

            else:
                st.write("No API usage data available.")

if __name__ == "__main__":
    main()
