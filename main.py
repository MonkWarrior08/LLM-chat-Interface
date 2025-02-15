import streamlit as st
from openai import OpenAI

# Sidebar: title and info for OpenAI
st.sidebar.title("Dimi's OpenAI")
st.sidebar.write("By [Monkwarrior08](https://github.com/Monkwarrior08)")



# Add a dropdown for model selection
model_options = ["o1", "o3-mini"]
selected_model = st.sidebar.selectbox("OpenAI model", model_options)

# Sidebar: add a system prompt input field
system_prompt = st.sidebar.text_area(
    "System Prompt",
    "You are a helpful assistant.",
    key="system_prompt",
    height=150
)

# Initialize the OpenAI client with the API key from secrets.toml
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set the default OpenAI model in session state if it hasn't been set already.
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = selected_model

# Update the model in session state if the user changes the selection in the sidebar.
if st.session_state["openai_model"] != selected_model:
    st.session_state["openai_model"] = selected_model

# Ensure that the session state contains a list to store chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render the saved messages in the chat interface.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Listen for user input through the chat input widget.
if prompt := st.chat_input("What is up?"):
    # Append the user's message to the conversation history and display it.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build the conversation for the API call.
    # Prepend the system prompt from the sidebar, if provided.
    messages_for_api = []
    if system_prompt.strip():
        messages_for_api.append({"role": "system", "content": system_prompt})
    messages_for_api.extend(st.session_state.messages)

    with st.chat_message("assistant"):
        result = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages_for_api,
        )
        try:
            # Attempt to extract the assistant's reply.
            answer = result["choices"][0]["message"]["content"]
        except (KeyError, TypeError):
            answer = result.choices[0].message.content
        st.markdown(answer)
    
    # Append the assistant's reply to the conversation history.
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Provide a sidebar button that allows users to clear the chat history.
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
 