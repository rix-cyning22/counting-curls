# Virtual Painter

Virtual Painter is an interactive application that allows users to draw, erase, and save their creations on a virtual canvas using hand gestures. The project leverages computer vision techniques for hand detection and tracking, enabling a seamless and intuitive experience.

## Features

- **Drawing Tool**: Draw on the canvas using a virtual brush.
- **Eraser Tool**: Erase parts of your drawing with a virtual eraser.
- **Save Tool**: Save your canvas as a PNG file with a simple gesture.
- **Hand Gesture Recognition**: Utilizes hand tracking for precise control.
- **Modular Design**: Each tool is a modular component, making it easy to extend the project with new functionality.

## Future Plans

- **Color Picker Tool**: A tool to change the brush color dynamically.
- **Shape Drawing Tool**: Add pre-defined shapes like circles, rectangles, and lines to the canvas.
- **Undo/Redo Functionality**: Allow users to undo and redo actions.
- **Gesture Customization**: Users can customize gestures for tools.

## Installation

Follow these steps to set up and run Virtual Painter:

1. **Clone the Repository**:

   ```bash
   git clone <repository_url>
   cd virtual-painter
   ```

2. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Ensure `requirements.txt` includes the following:

   ```
   opencv-python
   numpy
   pillow
   mediapipe
   tkinter
   ```

4. **Run the Application**:
   ```bash
   python camera.py
   ```

## Usage

- Launch the application and allow access to your camera.
- Use the following tools:
  - **Brush**: Use your index finger to draw on the canvas.
  - **Eraser**: Use your index finger to erase parts of the drawing.
  - **Save**: Hold your middle and index fingers over the save tool to save the current canvas as a PNG file.
- Press `q` to exit the application.

## Modular Design

The project is built with modularity in mind. Each tool (e.g., Brush, Eraser, Save) is implemented as a separate class inheriting from a base `Tool` class. This design ensures:

- **Ease of Extension**: Adding new tools is straightforward. Create a new class inheriting from `Tool`, define its `use` method, and add it to the `ToolsManager`.
- **Pluggable Architecture**: Tools can be swapped or updated with minimal changes to the core code.

To add a new tool:

1. Implement a new class in `tools.py`.
2. Define its position, dimensions, and behavior.
3. Add the new tool to the `ToolsManager` in `camera.py`.

Example:

```python
from virtualpainter.tools import NewTool

# Add the new tool to the manager
new_tool = NewTool(position=(x, y))
tool_manager.add_tool(new_tool)
```

## Project Structure

```
virtual-painter/
├── tools.py               # Contains tool implementations (Brush, Eraser, Save)
├── tools_manager.py       # Manages the tools and their interactions
├── hand_detection.py      # Hand detection and tracking logic
└── utils.py               # Functions to implement tools
camera.py              # Main application script
requirements.txt       # Python dependencies
README.md              # Project documentation
```

## Contribution

We welcome contributions to enhance the functionality and usability of Virtual Painter. If you have ideas for new tools or features, feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.
