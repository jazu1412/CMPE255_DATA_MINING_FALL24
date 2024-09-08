# AI Todo Assistant

## Overview

The AI Todo Assistant is a Flask-based web application that helps users manage their tasks and generate personalized daily plans. It utilizes intelligent algorithms to optimize task scheduling based on priority, estimated time, deadlines, and flexibility.

## Features

- Add tasks with details such as title, description, priority, estimated time, deadline, and flexibility
- Generate optimized daily plans based on wake-up time and task characteristics
- Automatically adjust plans based on changes in task priorities or time constraints
- Track task statistics, including total tasks, completed tasks, and high priority tasks
- Intuitive user interface for easy task management

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/jazu1412/CMPE255_DATA_MINING_FALL24.git
   ```

2. Navigate to the project directory:
   ```
   cd AI-Pair-Programmer-Todo_assistant
   ```

3. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # For Unix/Linux
   venv\Scripts\activate  # For Windows
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up the database:
   ```
   python models.py
   ```

6. Start the Flask development server:
   ```
   cd AI-Pair-Programmer-Priority-assistant
   python3 -m flask run
   ```

7. Open your web browser and visit `http://localhost:5000` to access the AI Todo Assistant.

## Usage

- Use the "Add Task" form to create new tasks with relevant details.
- Click the "Generate Daily Plan" button to get an optimized schedule based on your wake-up time.
- Mark tasks as completed using the "Complete" button next to each task.
-  Mark tasks as Deleted using the "Delete" button next to each task.
- The dashboard provides an overview of task statistics.


## File Structure

- `app.py`: The main Flask application file.
- `models.py`: Defines the database models for tasks.
- `planner.py`: Contains the algorithms for generating and adjusting daily plans.
- `templates/`: Directory containing HTML templates for the web interface.
- `static/`: Directory containing static assets (CSS, JavaScript).

  
#![AI To-Do Assistant Interface](AI-Pair-Programmer-Todo_assistant/app/static/images/img-1.png)
#![AI To-Do Assistant Interface](AI-Pair-Programmer-Todo_assistant/app/static/images/img-2.png)

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- The AI Todo Assistant was inspired by the need for efficient task management and scheduling.
- Thanks to the open-source community for the various libraries and tools used in this project.

## Contact

For any questions or inquiries, please contact [vmjs1412@gmail.com](mailto:vmjs1412.com).
