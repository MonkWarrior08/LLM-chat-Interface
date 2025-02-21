# LLM-chat-Interface

A simple PyQt6-based chat interface that lets you interact with multiple language models (Gemini, O3 Mini, and O1) in a single application. The interface supports a multi-line text input with an intuitive Enter/Return key functionality and displays responses using markdown formatting.

## Features

- **Multi-model Support:**  
  Easily choose between Gemini, O3 Mini, and O1 models from the sidebar.

- **Custom Chat Interface:**  
  A clean and simple GUI built with PyQt6 for real-time conversations.

- **System Prompt Configuration:**  
  Select a system prompt (e.g., *Code*, *Explain*, or *Scientific*) to provide context to the model responses.

- **Multi-line Input:**  
  Use the dedicated multi-line input box. Press **Enter/Return** (without Shift) to send your message, or **Shift+Enter** to add a new line.

## Code Structure

- **chat.py:**  
  Contains the main GUI application, model selection logic, conversation history management, and response handling. It uses a custom `InputTextEdit` widget to capture multi-line input and sends messages to the selected model.

- **gemini.py:**  
  Implements the API integration for the Gemini model using Google Gen AI. It builds a prompt by combining a system prompt with the user input before sending the request.

- **o3.py:**  
  Integrates with the OpenAI API to use the O3 Mini model. It sends chat-style messages including a system prompt (if provided) and user prompt.

- **o1.py:**  
  Provides access to the O1 model via the OpenAI API with additional options like heightened reasoning effort.

## Requirements

- Python 3.8 or higher
- [PyQt6](https://pypi.org/project/PyQt6/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [openai](https://pypi.org/project/openai/)
- [google-genai](https://pypi.org/project/google-genai/) (for Gemini integration)

## Setup

1. **Clone the Repository:**

  ```bash
  git clone https://github.com/yourusername/LLM-chat-Interface.git
  cd LLM-chat-Interface
  ```

2. **Create a Virtual Environment (Optional but Recommended):**

  ```bash
  python -m venv venv
  source venv/bin/activate   # On Windows: venv\Scripts\activate
  ```

3. **Install Dependencies:**

  Using `requirements.txt`, install via:

  ```bash
  pip install -r requirements.txt
  ```

  Otherwise, install the packages manually:

  ```bash
  pip install PyQt6 python-dotenv openai google-genai
  ```

4. **Configure Environment Variables:**

  Create a `.env` file in the project root with your credentials:

  ```bash
  # .env file
  OPENAI_API_KEY=your_openai_api_key_here
  GEMINI_API_KEY=your_gemini_api_key_here
  ```

  - The **OPENAI_API_KEY** is used for both O3 Mini and O1 models.
  - The **GEMINI_API_KEY** is required for the Gemini integration.

## Running the Application

Launch the chat interface by running:

  ```bash
  python chat.py
  ```

A window will open that displays:
- A left sidebar for selecting the AI model and system prompt.
- A chat area on the right where messages are displayed in real time.
- A multi-line text box at the bottom for input.

Type your message into the input area and press **Enter/Return** (without holding Shift) to send your message. The response from the selected model will appear in the chat display area.

## Usage Notes

- **Model Switching:**  
  Click on the "Gemini", "O3 Mini", or "O1" buttons in the sidebar to switch between models. Switching models clears the current conversation.

- **System Prompts:**  
  Use the drop-down menu in the sidebar to choose a system prompt. This provides context for the model (such as instructing it to explain code or provide scientific detail).

- **Conversation History:**  
  The application maintains a conversation history which is used to build the prompt for model responses. Starting a new conversation clears this history.

## Troubleshooting

- **API Key Issues:**  
  Ensure that your API keys are correctly set in the `.env` file and that there are no extra spaces or formatting issues.

- **Dependencies:**  
  Verify that all dependencies are installed. Use `pip list` to check the installed packages if you encounter module import errors.

- **PyQt6:**  
  If the GUI does not launch or you run into display issues, confirm that your system supports PyQt6 and that you are using a compatible version of Python.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements, bug fixes, or new features.

---
Happy chatting with your custom LLM interface!