# Basic Imports
from dotenv import load_dotenv
import os

# Third Party Imports
import streamlit as st

# Internal Imports
from agent.main_logic import (
    ai_api_call,
    ai_api_response_formatting,
    running_tool_calls_processing,
    check_function_simulation
)
from agent.tools import restaurant_tools
from agent.prompts import (
    restaurant_test_conversation_system_prompt,
    restaurant_test_conversation_system_prompt_w_fewshot
)

# Setting up Logging
import logging

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('foodiespot')

# Global Constants and Variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Parent directory
DATA_DIR = os.path.join(BASE_DIR, "data")

logger.info(f"BASE_DIR set to: {BASE_DIR}")
logger.info(f"DATA_DIR set to: {DATA_DIR}")

# Load environment variables from .env file
load_dotenv()  
together_ai_api_key = os.getenv("TOGETHER_API_KEY")
if together_ai_api_key:
    logger.info("API key loaded successfully")
else:
    logger.error("API key not found in environment variables")

logger.info("FoodieSpot Reservation Assistant started")

# App configuration
st.title("FoodieSpot Reservation Assistant")
st.subheader("Book tables at our restaurants across Bangalore")

# Initialize chat settings
system_prompt = restaurant_test_conversation_system_prompt_w_fewshot
first_message = "Hello! I'm here to help with your reservation at FoodieSpot in Bangalore. You can ask me for recommendations of restaurants or book a table at your preferred location."

# Session state initialization
if "messages" not in st.session_state:
    restaurant_test_conversation = []
    restaurant_test_conversation.append({"role": "system", "content": system_prompt})
    restaurant_test_conversation.append({"role": "assistant", "content": first_message})
    st.session_state.messages = restaurant_test_conversation

# Conversation reset function
def reset_conversation():
        logger.info("Conversation reset by user")
        restaurant_test_conversation = []
        restaurant_test_conversation.append({"role": "system", "content": system_prompt})
        restaurant_test_conversation.append({"role": "assistant", "content": first_message})
        st.session_state.messages = restaurant_test_conversation

# Sidebar reset button
with st.sidebar:
    st.button("Restart Conversation", on_click=reset_conversation)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] not in ["system", "tool"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input and processing
if prompt := st.chat_input("Ask about reservations or available restaurants..."):
    logger.info(f"User input received: {prompt}...")

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                logger.info(f"Making AI call with conversation history length: {len(st.session_state.messages)} messages")
                # Initial API call
                api_response = ai_api_call(
                            api_key=together_ai_api_key, 
                            conversation_history=st.session_state.messages, 
                            tools=restaurant_tools, 
                            tool_calling_enabled=True)
                
            except Exception as e:
                logger.error(f"API call failed: {str(e)}", exc_info=True)
                st.error(f"An error occurred with the API call with User Message. Please restart the conversation.")
                st.stop()
        
        # Process API response
        formatted_response = ai_api_response_formatting(api_response)
        logger.info(f"API response received: {type(formatted_response)}")
        
        # Handle direct responses
        if not isinstance(formatted_response, list):
            response_content = formatted_response.get("content", "")

            #Checking for function simulation
            function_simulation_resp = check_function_simulation(response_content)
            if function_simulation_resp:
                logger.warning(f"Function simulation detected in response: {response_content[:100]}...")
                st.error (f"An error occurred with the API call with User Message. Please restart the conversation.")
                st.stop()
                
            else:
                st.markdown(response_content)
                st.session_state.messages.append(formatted_response)
            
        # Handle tool calls
        if isinstance(formatted_response, list):
            logger.info(f"Processing {len(formatted_response)} tool calls")
            # Show "thinking" message
            message_placeholder = st.empty()
            message_placeholder.markdown("Processing your request...")

            # Process tool calls
            tool_messages = running_tool_calls_processing(formatted_response)
            st.session_state.messages.extend(tool_messages)

            # Logging tool call processing completion
            logger.info(f"Tool execution completed with {len(tool_messages)} results")
        
            # Follow-up API call
            try:
                updated_response = ai_api_call(api_key=together_ai_api_key, 
                                           conversation_history=st.session_state.messages, 
                                           tools=restaurant_tools, 
                                           tool_calling_enabled=False)
            except Exception as e:
                logger.error(f"API call failed: {str(e)}", exc_info=True)
                st.error(f"An error occurred with the API call after Tool Use. Please restart the conversation.")
                st.stop()

            # Display final response
            formatted_updated_response = ai_api_response_formatting(updated_response)
            message_placeholder.markdown(formatted_updated_response.get("content", ""))
            st.session_state.messages.append(formatted_updated_response)