import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit
)
import html
import os
import multiprocessing

message_queue = multiprocessing.Queue()


class TextToHtmlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text to HTML Converter")
        self.init_ui()

    def init_ui(self):

        self.layout = QVBoxLayout()

        path_layout = QHBoxLayout()
        self.path_input = QLineEdit(self)
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_file)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_button)
        self.layout.addLayout(path_layout)


        self.result_display = QTextEdit(self)
        self.result_display.setPlaceholderText("HTML result")
        self.layout.addWidget(self.result_display)


        self.convert_button = QPushButton("Convert to HTML", self)
        self.convert_button.clicked.connect(self.convert_to_html)

        self.send_button = QPushButton("Send to C program", self)
        self.send_button.clicked.connect(self.send_to_c)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.send_button)
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt)")
        if file_path:
            self.path_input.setText(file_path)

    def convert_to_html(self):
        file_path = self.path_input.text()
        if not os.path.isfile(file_path):
            self.result_display.setText("Invalid file path.")
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if not lines:
            self.result_display.setText("Empty file.")
            return

        title = html.escape(lines[0].strip())
        paragraphs = [f"<p>{html.escape(line.strip())}</p>" for line in lines[1:] if line.strip()]
        html_content = f"<html><head><title>{title}</title></head><body><h1>{title}</h1>{''.join(paragraphs)}</body></html>"

        self.result_display.setPlainText(html_content)

    def send_to_c(self):
        html_result = self.result_display.toPlainText()
        if html_result:
            with open("message.txt", "w", encoding='utf-8') as f:
                f.write(html_result)
            self.result_display.append("\n[INFO] HTML content written to 'message.txt' for C app.")
        else:
            self.result_display.append("\n[ERROR] No HTML to send.")

def run_app():
    app = QApplication(sys.argv)
    window = TextToHtmlApp()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
