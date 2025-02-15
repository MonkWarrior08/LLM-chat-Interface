import streamlit as st
import google.generativeai as genai  # Updated import

# Sidebar: title and info for Gemini
st.sidebar.title("Dimi's Gemini")
st.sidebar.write("By [Monkwarrior08](https://github.com/MonkWarrior08)")

# Sidebar: select the Gemini model (example model names; modify as needed)
model_options = ["gemini-2.0-flash"]  # Updated model name
selected_model = st.sidebar.selectbox("Gemini model", model_options)

# Sidebar: add a system prompt input field
# You can type instructions here that will always be prepended to your user query.
system_prompt = st.sidebar.text_area(
    "System Prompt",
    "You are a helpful assistant.",
    key="system_prompt",
    height=150
)

# Initialize Gemini AI with API key from secrets.toml
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to generate a response from Gemini AI,
# now including the system prompt (if provided) in the conversation context.
def get_gemini_response(user_message):
    # Retrieve the system prompt from session state (or sidebar) if provided
    system_prompt = st.session_state.get("system_prompt", "")
    # Build the combined message: include the system prompt followed by the user message.
    if system_prompt.strip():
        combined_message = f"{system_prompt}\n\nUser: {user_message}"
    else:
        combined_message = user_message

    # Create an instance of the GenerativeModel using the selected model
    model = genai.GenerativeModel(selected_model)
    # Generate a text response based on the combined message
    response = model.generate_content(combined_message)
    return response.text

# Display Conversation History
st.header("Gemini AI Chat")
for i, message in enumerate(st.session_state.conversation):
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# Chat input for user messages
user_input = st.chat_input("Type your message here...")

if user_input:
    # Append user message to conversation history
    st.session_state.conversation.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Get AI response
    response = get_gemini_response(user_input)
    st.session_state.conversation.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

# Provide a sidebar button that allows users to clear the chat history.
if st.sidebar.button("Clear Chat"):
    st.session_state.conversation = []