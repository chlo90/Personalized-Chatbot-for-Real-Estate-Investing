import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from realestategpt import RealEstateGPT

# Initialize conversation history in session state if not already present
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

main_title = 'Find your perfect house in Austin with AI!'
# Set the title of the app
st.title(main_title)

austin_data = pd.read_csv('austin_redfin_scraping_072624.csv').dropna().reset_index().drop(columns=['Unnamed: 0'])

# Create the map
# map = folium.Map(location=[ZOOM_LAT, ZOOM_LONG], zoom_start=ZOOM_START)
# for _, row in austin_data.iterrows():
#     folium.Marker(
#         location=[row['latitude'], row['longitude']],
#         popup=f"Property: {row['zip_code']}"
#     ).add_to(map)
#
# # Display the map
# st_data = st_folium(map, width=725, height=500)

# Initialize or reset the conversation history in session state if not already present
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

# Initialize the RealEstateGPT instance outside the process_query function to persist its state
if 'realestategpt' not in st.session_state:
    st.session_state['realestategpt'] = RealEstateGPT(one_shot=False)  # Assuming you want a conversational mode


# Function to process the query and update conversation
def process_query(query):
    if query:  # Check if the query is not empty
        # Use the persistent RealEstateGPT instance
        response = st.session_state['realestategpt'].ask_real_estate_question(query)
        # Update the conversation history with structured data
        st.session_state['conversation_history'].append({'Client': query, 'AI': response})


# Function to display conversation history
def display_conversation():
    for exchange in st.session_state['conversation_history']:
        st.text_area("You", value=exchange['Client'], height=100, disabled=True)
        st.text_area("AI", value=exchange['AI'], height=100, disabled=True)


# Display the conversation history
display_conversation()

# Collect new question input
user_question = st.text_input("Talk to me about your dream house:", key="user_question")

# Button to submit the question
if st.button('Send'):
    process_query(user_question)
    # Clear the input text by re-rendering the UI
#    st.session_state['user_question'] = ''  # Optional: clear the input box (might need adjustment or removal)
    # Rerun the script to refresh the UI, indirectly clearing the input field if not cleared by the optional line above
    st.rerun()