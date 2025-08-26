import streamlit as st
import requests
import pandas as pd

st.title("HR Resource Query Chatbot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Only display employee table if data exists and is valid
        if message["role"] == "assistant" and "employees" in message and message["employees"]:
            try:
                df = pd.DataFrame(message["employees"])
                required_columns = ["name", "skills", "experience_years", "projects", "availability"]
                if all(col in df.columns for col in required_columns):
                    st.table(df[required_columns])
                else:
                    st.warning("Employee data is incomplete and cannot be displayed as a table.")
            except Exception as e:
                st.error(f"Error displaying employee data: {str(e)}")

# Chat input
if query := st.chat_input("Enter your query (e.g., 'Find Python developers with 3+ years experience')"):
    # Display user query
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Call FastAPI backend
    try:
        response = requests.post("https://broadly-more-pug.ngrok-free.app/chat", json={"query": query})
        response.raise_for_status()
        result = response.json()
        response_text = result["response"]
        employees = result.get("employees", [])
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response_text)  # Already renders markdown format, which now matches assignment style
            if employees:
                df = pd.DataFrame(employees)
                required_columns = ["name", "skills", "experience_years", "projects", "availability"]
                if all(col in df.columns for col in required_columns):
                    st.table(df[required_columns])
                else:
                    st.warning("Employee data is incomplete and cannot be displayed as a table.")
                    # except Exception as e:
                    # st.error(f"Error displaying employee data: {str(e)}")
        
        # Store response and employees in session state
        st.session_state.messages.append({"role": "assistant", "content": response_text, "employees": employees})
    
    except requests.RequestException as e:
        error_msg = f"Oops! Something went wrong: {str(e)}. Please check your connection or try again."
        with st.chat_message("assistant"):
            st.error(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg, "employees": []})
