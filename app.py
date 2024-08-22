import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import re
from realestategpt import RealEstateGPT

# Initialize conversation history in session state if not already present
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

main_title = 'Find your perfect house in Austin with AI!'
# Set the title of the app
st.title(main_title)

austin_data = pd.read_csv('data/redfin_sales_080924.csv').dropna().reset_index().drop(columns=['Unnamed: 0'])

# Create the map - focus on Austin MSA map
ZOOM_LAT, ZOOM_LONG, ZOOM_START = 30.266666, -97.733330, 10
map = folium.Map(location=[ZOOM_LAT, ZOOM_LONG], zoom_start=ZOOM_START)
for _, row in austin_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"<a href='{row['Picture']}' target='_blank'>Property: {row['Address']}</a>",
    ).add_to(map)

# Display the map
st_data = st_folium(map, width=725, height=500)

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
        # Escape special characters in the response for safe regex usage
        # sanitized_response = re.escape(response)
        
        # Filter the dataset based on the sanitized response
        # suggested_properties = austin_data[austin_data['Address'].str.contains(sanitized_response, case=False, na=False)]

        # Update the conversation history with structured data
        st.session_state['conversation_history'].append({
            'Client': query, 
             'AI': "Suggested properties based on your query:",
            'suggestions': response
        })



# Function to display conversation history
def display_conversation():
    for exchange in st.session_state['conversation_history']:
        st.text_area("You", value=exchange['Client'], height=100, disabled=True)
        st.markdown(exchange['AI'], unsafe_allow_html=True)  # Allows rendering of markdown (images)
        # st.text_area("AI", value=exchange['AI'], height=100, disabled=True)
       # Display buttons for each property suggestion
       # Ensure 'suggestions' is a DataFrame
        # Check type of 'suggestions'
        suggestions = exchange.get('suggestions')
        
        # Debugging: Check type of 'suggestions'
        st.write("Type of 'suggestions':", type(suggestions))
        
        if isinstance(suggestions, pd.DataFrame) and not suggestions.empty:
            selected_property = st.radio(
                "Select a property:",
                options=[f"{idx+1}. {row['address']}" for idx, row in exchange['suggestions'].iterrows()]
            )

            # Get the index of the selected property
            selected_idx = int(selected_property.split('.')[0]) - 1
            if selected_idx >= 0:
                selected_row = exchange['suggestions'].iloc[selected_idx]
                # Show the image for the selected property
                st.image(selected_row['Picture'], caption=f"Image of property at {selected_row['address']}")
        else:
            st.write("No properties found based on your query.")


# Function to clear the input box
def clear_text():
    st.session_state['user_question'] = ''  # Clears the input box

# Display the conversation history
display_conversation()

# Collect new question input
user_question = st.text_input("Talk to me about your dream house:", key="user_question")

# Button to submit the question
if st.button('Send'):
    process_query(user_question)
    # Clear the input text by re-rendering the UI
    # clear_text()  # Optional: clear the input box (might need adjustment or removal)
    # Rerun the script to refresh the UI, indirectly clearing the input field if not cleared by the optional line above
    st.rerun()

