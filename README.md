# TinyCompilerTools
Parser and Scanner for the Tiny programming language, designed to tokenize and analyze code for syntax validation and further compilation tasks.

## TINY Language Parser

This project is a TINY language parser with a graphical user interface (GUI) built using PyQt5. The parser visualizes the parse tree of the TINY language code, allowing users to see the structure of their code in a graphical format.

## Features

- **Code Input**: Users can input TINY language code directly into the text editor or choose a file to load the code.
- **Parse and Visualize**: The parser processes the input code and visualizes the parse tree.
- **Scrollable Visualization**: The parse tree visualization is displayed in a scrollable area to handle large trees.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/tiny-language-parser.git
    cd tiny-language-parser
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    python main.py
    ```

## Usage

1. **Input Code**: Enter your TINY language code in the text editor provided in the GUI.
2. **Parse and Visualize**: Click the "Parse and Visualize" button to parse the code and visualize the parse tree.
3. **Choose File**: Alternatively, you can click the "Choose File" button to load TINY language code from a file.

## Project Structure

- `main.py`: Entry point of the application.
- `gui.py`: Contains the `TreeVisualizer` class which defines the GUI and handles user interactions.
- `scanner.py`: Contains the `Scanner` class which tokenizes the input TINY language code.
- `parser.py`: Contains the `Parser` class which parses the tokens and builds the parse tree.

## Screenshot

![image](https://github.com/user-attachments/assets/3c7a32df-84b5-4dcf-9bd1-f4628572a032)

## Example Code

Here is an example of TINY language code that can be parsed and visualized by this application:

```tiny
read x;
if 0 < x then
    fact := 1;
    repeat
        fact := fact * x;
        x := x - 1
    until x = 0;
    write fact
end
