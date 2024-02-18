from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qsci import * 
from PyQt5.QtGui import * 
import webbrowser
import subprocess


import sys
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.body_clr = "#ADD8E6"
        self.init_ui()
        self.current_file_path = None
        self.current_file = None


    def init_ui(self):
        self.setWindowTitle("GOOF-IDE")
        self.resize(1300, 900)

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.body_clr};
            }}
            """ + open("./src/css/style.qss", "r").read())

        self.window_font = QFont("Microsoft Sans Serif") #font needs to be installed on computer
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)

        self.set_up_menu()
        self.set_up_body()
        self.statusBar().showMessage("WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP WAKE UP ")

        self.open_folder('C:/Users/fredd/OneDrive/Desktop/Hackathon')

        self.show()

    def get_editor(self) -> QsciScintilla:
        pass

    def run_file(self):
        if self.current_file_path:
            # Run the current file as a Python script
            try:
                # Execute the script
                output = subprocess.run(['python', self.current_file_path], text=True, capture_output=True, check=True)
                # Display the script's output and/or errors
                self.statusBar().showMessage("Script executed successfully.", 5000)
                QMessageBox.information(self, "Output", output.stdout)
            except subprocess.CalledProcessError as e:
                # If there's an error running the script, show it in a message box
                QMessageBox.warning(self, "Error", e.stderr)
        else:
            QMessageBox.warning(self, "No file", "There is no file currently open to run.")

    def set_up_menu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")

        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)

        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        open_folder = QAction('Open Folder', self)
        open_folder.setShortcut('Ctrl+Shift+O')
        open_folder.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder)

        close_file = file_menu.addAction("Close File")
        close_file.setShortcut("Ctrl+C")
        close_file.triggered.connect(self.close_file)

        # death menu
        edit_menu = menu_bar.addMenu("Dont Click Me")

        dont_click_me = edit_menu.addAction("I said dont click me")
        dont_click_me.triggered.connect(self.open_death)


        # run code
        run_menu = menu_bar.addMenu("Run")
        run_action = run_menu.addAction("Run File")
        run_action.setShortcut("Ctrl+R")
        run_action.triggered.connect(self.run_file)
        
    def open_folder(self, path=None):
        if path is None:
            dir_path = QFileDialog.getExistingDirectory(self, 'Open Folder', '/')
        else:
            dir_path = path  # Use the provided path argument
        if dir_path:
            self.directory_view.setRootIndex(self.file_system_model.setRootPath(dir_path))

        # add more
    def close_file(self):
        # Check if there are unsaved changes
        if self.text_edit.document().isModified():
            reply = QMessageBox.question(self, 'Close File', "You have unsaved changes. Do you want to save them before closing?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)

            if reply == QMessageBox.Save:
                self.save_file()  # Save the file
            elif reply == QMessageBox.Cancel:
                return  # Do not close the file if the user cancels
            
        # Proceed to close the file
        self.text_edit.clear()
        self.current_file_path = None
        self.file_name_label.setText("No file opened")
        self.statusBar().showMessage("File closed", 2000)

    def save_file(self):
        if self.current_file_path:
            # Save the current content to the file
            with open(self.current_file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.text())
            self.statusBar().showMessage(f"Saved {self.current_file_path}", 2000)
        else:
            # No file is open, use Save As functionality
            self.save_as()
    
    def open_file(self):
        # Open a file dialog to select a .txt file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        
        # Check if a file was selected
        if file_name:
            self.current_file_path = file_name
            # Read the content of the file
            with open(file_name, 'r', encoding='utf-8') as file:
                file_content = file.read()
            
            # Display the content in the editor
            self.display_file_content(file_content, file_name)
    
    def open_death(self):
        webbrowser.open('https://www.youtube.com/watch?v=xvFZjo5PgG0', new=2)   
    
    def display_file_content(self, content):
        self.text_edit.setText(content)    

    def display_file_content(self, content, file_name):
        self.text_edit.setText(content)
        self.file_name_label.setText(Path(file_name).name)  # Display just the file name

    def set_up_body(self):
        # Main horizontal layout
        main_layout = QHBoxLayout()

        # File explorer
        self.file_system_model = QFileSystemModel(self)
        self.file_system_model.setReadOnly(False)

        self.file_system_model.setRootPath("C:/Users/fredd/OneDrive/Desktop/Hackathon")

        self.directory_view = QTreeView()

        self.directory_view.setModel(self.file_system_model)
        self.directory_view.hideColumn(1)  # hide size
        self.directory_view.hideColumn(2)  # hide type
        self.directory_view.hideColumn(3)  # hide date modified
        self.directory_view.setVisible(True)
        self.directory_view.clicked.connect(self.open_file_from_tree)

        # Pink body area
        self.body_frame = QFrame()
        self.body_frame.setFrameShape(QFrame.NoFrame)
        self.body_frame.setFrameShadow(QFrame.Plain)
        self.body_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        body_layout = QVBoxLayout()
        self.body_frame.setLayout(body_layout)

        # Label for displaying the file name
        self.file_name_label = QLabel("No file opened")
        self.file_name_label.setFont(QFont("Arial", 14))
        self.file_name_label.setAlignment(Qt.AlignCenter)
        # Set the background color of the label to grey
        # and add some padding for aesthetic purposes
        self.file_name_label.setStyleSheet("""
            background-color: white;
            padding: 5px;
            border-radius: 5px;
        """)
        self.file_name_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        body_layout.addWidget(self.file_name_label)

        # QsciScintilla editor
        self.text_edit = QsciScintilla()
        self.text_edit.setFont(QFont("Consolas", 10))
        
        # Set the Python lexer
        lexer = QsciLexerPython()
        lexer.setDefaultFont(QFont("Consolas", 10))
        self.text_edit.setLexer(lexer)
        
        # Enable line numbers with the margin
        self.text_edit.setMarginsFont(self.text_edit.font())
        self.text_edit.setMarginWidth(0, QFontMetrics(self.text_edit.font()).width("0000") + 6)
        self.text_edit.setMarginLineNumbers(0, True)
        
        # Set background color for the editor (light blue)
        # lexer.setPaper(QColor("#ADD8E6"))

        body_layout.addWidget(self.text_edit)  # added to the body_frame widget children

        # Splitter to allow resizing
        self.hsplit = QSplitter(Qt.Horizontal)
        self.hsplit.addWidget(self.directory_view)
        self.hsplit.addWidget(self.body_frame)

        # Set the initial sizes of the splitter to make the directory view and text editor share the space equally
        total_width = self.width()
        self.hsplit.setSizes([total_width//4, 3*total_width//4])

        main_layout.addWidget(self.hsplit)
        
        # Set the main layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def open_file_from_tree(self, file_index):
        file_path = self.file_system_model.filePath(file_index)
        
        # Check if the selected item is a file
        if QFileInfo(file_path).isFile():
            self.current_file_path = file_path
            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                self.file_name_label.setText(QFileInfo(file_path).fileName())  # Display just the file name
            # Display the content in the editor
            self.text_edit.setText(file_content)

# stylesheet = """
#     MainWindow {
#         background-image: url("C:/Users/fredd/OneDrive/Desktop/Hackathon/assets/images/Anime.jpg"); 
#         background-repeat: no-repeat; 
#         background-position: center;
#     }
# """

if __name__ == '__main__':
    app = QApplication([])
    # app.setStyleSheet(stylesheet) 
    window = MainWindow()
    sys.exit(app.exec())