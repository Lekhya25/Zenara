# Zenara: Crafting Success One Productive Moment at a Time

Zenara is a comprehensive productivity tool designed to integrate various essential features into a singular platform. It aims to enhance productivity by providing a seamless experience that combines task management, collaboration, and innovative productivity enhancements.

Watch demo [here](https://github.com/Lekhya25/Zenara/blob/main/Zenara_DemoVideo_compressed.mp4)


## Problem Statement

Existing productivity tools lack comprehensive integration and may not incorporate essential features like a Pomodoro timer, hindering users' ability to tailor their workspace for optimal productivity and focus.

## Features

- **Pomodoro Timer**
  - Start, pause, resume, and customize work/break lengths
  - Sound notifications
- **Calendar Scheduling**
  - Add, view, and manage events
- **To-Do List**
  - Add, edit, delete tasks
- **Attendance Calculator**
  - Calculate and manage attendance
- **CGPA Calculator**
  - Calculate CGPA with intuitive forms
- **Notes**
  - Add, view, and manage notes
- **User Authentication**
  - Secure login, signup, and logout functionalities


## Future Work

- User Feedback and Analytics
- Mobile Responsiveness
- Integration with Calendar Apps
- Customizable Themes
- Progress Tracking
- Community and Support

## References

- [Mozilla Developer Network (MDN)](https://developer.mozilla.org/en-US/docs/Learn/CSS)
- [W3Schools](https://www.w3schools.com)
- [GeeksforGeeks](https://www.geeksforgeeks.org/html-complete-guide/)
- [Stack Overflow](https://stackoverflow.com/tags/html/info)
- [Python Tutorial](https://www.pythontutorial.net/python-concurrency/python-threading/)
- [DataCamp](https://www.datacamp.com/tutorial/sqlalchemy-tutorial-examples)
- [Real Python](https://realpython.com/intro-to-python-threading/)
- [FullCalendar](https://fullcalendar.io/)
- [Bootstrap](https://getbootstrap.com/)

---

## How to Download and Run the Project

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Git

### Instructions

1. **Clone the Repository**

   Open your terminal or command prompt and run the following command to clone the repository:

   ```bash
   git clone https://github.com/Lekhya25/zenara.git
   cd zenara

2. **Create a Virtual Environment**

    It's a good practice to create a virtual environment for your project. Run the following commands:

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies**

      Install the required Python packages using pip:

      ```bash
      pip install -r requirements.txt
      
4. **Set Up the Database**

      If you're using SQLite (as indicated), the database should be created automatically. If using another database like MySQL, ensure you update the SQLALCHEMY_DATABASE_URI in config.py accordingly and create the necessary database.

5. **Run the Application**

    Start the Flask application by running:

    ```bash
    flask run
    
6. **Access the Application**

      Open your web browser and go to http://127.0.0.1:5000 to access Zenara.

## Notes
 * Make sure to keep your virtual environment activated whenever you are working on the project.
 * If you face any issues, check the error messages in the terminal for guidance.
