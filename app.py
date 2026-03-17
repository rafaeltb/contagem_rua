import streamlit as st

# Main Title
st.title('Vineyard Productivity Management')

# Layout settings for mobile optimization
st.set_page_config(layout='wide')

# Sidebar for navigation
st.sidebar.title('Navigation')

# Sections
st.sidebar.header('Productivity Metrics')

# Input fields for vineyard data
area = st.sidebar.number_input('Enter Vineyard Area (acres)', min_value=0.0)

yield_per_acre = st.sidebar.number_input('Enter Yield per Acre (tons)', min_value=0.0)

# Calculate total yield
if st.sidebar.button('Calculate Total Yield'):
    total_yield = area * yield_per_acre
    st.write(f'Total Expected Yield: {total_yield} tons')

# Footer
st.sidebar.write("Created by rafaeltb")