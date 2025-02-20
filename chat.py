import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QComboBox
)
from PyQt6.QtCore import pyqtSignal, QThread, Qt
from PyQt6.QtGui import QKeyEvent

# Import get_response functions from both modules
from gemini import get_response as gemini_get_response
from o3 import get_response as o3_get_response
from o1 import get_response as o1_get_response

# New custom text edit for multi-line input with a returnPressed signal.
class InputTextEdit(QTextEdit):
    returnPressed = pyqtSignal()

    def keyPressEvent(self, event: QKeyEvent):
        # Check if Enter/Return is pressed without Shift (to send the message)
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
            event.accept()
            self.returnPressed.emit()
        else:
            super().keyPressEvent(event)

class ResponseWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, prompt, get_response_func, system_prompt, parent=None):
        super().__init__(parent)
        self.prompt = prompt
        self.get_response_func = get_response_func
        self.system_prompt = system_prompt

    def run(self):
        # Call the selected model's API (Gemini, O3 Mini, or O1)
        response = self.get_response_func(self.prompt, self.system_prompt)
        self.finished.emit(response)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Default model is Gemini
        self.current_model_name = "Gemini"
        self.get_response_func = gemini_get_response

        # Initialize conversation history (as a list of tuples: (sender, message))
        self.conversation_history = []

        self.setWindowTitle(f"{self.current_model_name}")
        self.resize(800, 600)

        # Set up the main container widget with a horizontal layout:
        # left sidebar for model selection and right chat area.
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left sidebar widget for model selection.
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        
        model_label = QLabel("Select Model")
        sidebar_layout.addWidget(model_label)
        
        # Button to select Gemini
        self.gemini_button = QPushButton("Gemini")
        self.gemini_button.clicked.connect(self.select_gemini)
        sidebar_layout.addWidget(self.gemini_button)
        
        # Button to select O3 Mini
        self.o3mini_button = QPushButton("O3 Mini")
        self.o3mini_button.clicked.connect(self.select_o3mini)
        sidebar_layout.addWidget(self.o3mini_button)
        
        # Button to select O1
        self.o1_button = QPushButton("O1")
        self.o1_button.clicked.connect(self.select_o1)
        sidebar_layout.addWidget(self.o1_button)
        
        # Add spacing before adding system prompt selection.
        sidebar_layout.addSpacing(20)
        
        # System prompt selection: add a label and combo box.
        system_prompt_label = QLabel("Select System Prompt")
        sidebar_layout.addWidget(system_prompt_label)
        
        self.system_prompt_combo = QComboBox()
        # Add system prompt options.
        self.system_prompt_combo.addItem("None", "")
        self.system_prompt_combo.addItem("Pirate", "You talk like a pirate.")
        self.system_prompt_combo.addItem("french", "you are a french speaker.")
        self.system_prompt_combo.addItem("Sarcastic", "You are sarcastic.")
        sidebar_layout.addWidget(self.system_prompt_combo)
        
        sidebar_layout.addStretch()  # Push the buttons to the top

        # Right side: Chat display and input area.
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        
        self.chat_display = QTextEdit()
        # Set the font size to 16px using a stylesheet.
        self.chat_display.setStyleSheet("font-size: 16px; font-family: 'Arial', sans-serif;")
        self.chat_display.setReadOnly(True)

        chat_layout.addWidget(self.chat_display)
        
        # Replace QLineEdit with a multi-line InputTextEdit.
        self.input_line = InputTextEdit()
        # Set fixed height to approximately three lines (adjust as needed)
        self.input_line.setFixedHeight(80)
        self.input_line.returnPressed.connect(self.on_send)
        chat_layout.addWidget(self.input_line)
        
        # Add both sidebar and chat widget into the main layout.
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(chat_widget)

    def select_gemini(self):
        """Gemini model """
        self.current_model_name = 'Gemini'
        self.get_response_func = gemini_get_response
        self.start_new_conversation()

    def select_o3mini(self):
        """O3 Mini model """
        self.current_model_name = 'O3 Mini'
        self.get_response_func = o3_get_response
        self.start_new_conversation()

    def select_o1(self):
        """O1 model """
        self.current_model_name = 'O1'
        self.get_response_func = o1_get_response
        self.start_new_conversation()

    def start_new_conversation(self):
        """Clear the conversation and update the interface for the new model."""
        self.chat_display.clear()
        self.input_line.clear()
        self.input_line.setEnabled(True)
        self.setWindowTitle(f"{self.current_model_name} Chat Interface")
        # Clear stored conversation history when starting fresh.
        self.conversation_history = []
       
    def on_send(self):
        # Use toPlainText() instead of text() for QTextEdit.
        user_text = self.input_line.toPlainText().strip()
        if not user_text:
            return

        # Append the user's message (update display and conversation history).
        self.append_message("User", user_text)
        self.input_line.clear()
        self.input_line.setDisabled(True)

        # Build a full prompt that includes the conversation history.
        if self.current_model_name == "Gemini":
            full_prompt = "\n".join(f"{sender}: {message}" for sender, message in self.conversation_history)
            full_prompt += "\nGemini:"  # cue the model to respond
        elif self.current_model_name == "O3 Mini":
            full_prompt = "\n".join(f"{sender}: {message}" for sender, message in self.conversation_history)
            full_prompt += "\nO3 Mini:"  # cue the model to respond
        elif self.current_model_name == "O1":
            full_prompt = "\n".join(f"{sender}: {message}" for sender, message in self.conversation_history)
            full_prompt += "\nO1:"  # cue the model to respond

        # Retrieve the currently selected system prompt from the combo box.
        system_prompt = self.system_prompt_combo.currentData() or ""

        # Start a worker thread with the selected model function and system prompt.
        self.worker = ResponseWorker(full_prompt, self.get_response_func, system_prompt)
        self.worker.finished.connect(self.handle_response)
        self.worker.start()

    def handle_response(self, response):
        self.append_message(self.current_model_name, response)
        self.input_line.setDisabled(False)
        self.input_line.setFocus()

    def append_message(self, sender, message):
        """
        Append a new message by saving it in conversation_history and
        refreshing the chat display with markdown rendering.
        """
        # If the conversation isn't empty and the sender changes,
        # add an empty line to visually separate the messages.
       
              # Insert a blank line
        self.chat_display.append(f"<b>{sender}:</b> {message}")
        # Store the message in the conversation history.
        self.conversation_history.append((sender, message))
        # Refresh the chat display using markdown rendering.
        self.update_chat_display()

    def update_chat_display(self):
        """
        Rebuild the entire chat conversation as a markdown string and
        set it on the chat_display widget with a blank line between each message.
        """
        # Build the markdown text with two newlines between messages.
        markdown_text = "\n\n<br></br>".join(
            f"**{sender}:** {message}" for sender, message in self.conversation_history
        )
        self.chat_display.setMarkdown(markdown_text)
        # Re-apply the stylesheet after setting the markdown.
       

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec()) 