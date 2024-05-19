# CHUGG
Chugg is a web-based forum application designed to facilitate easy access to study materials and provide a platform for educational discussion among students globally. It operates using a user-friendly interface built with HTML, CSS, and JavaScript, and utilizes Flask, a lightweight Python web framework.


## Documentation
The Chugg application employs the MVC (Model-View-Controller) architectural pattern, with each component designed to handle specific aspects of the application's functionality:

- **Model**: Responsible for data-related logic, the models interact with an SQLite database, managing the storage and retrieval of user data and forum posts.
- **View**: The user interface is built with HTML and styled using CSS. Dynamic content is generated through Jinja templates, allowing for real-time updates and user interactions.
- **Controller**: The controllers process incoming requests, utilizing Flask to route these requests between the model and the view. This includes handling user registrations, forum posts, and responses.

Key Features and Functionality:
- **User Account System**: Users can register and log in, maintaining a secure and personalized experience.
- **Forum Posting**: Students can post questions, categorize them based on subjects or topics, and receive answers from peers.
- **Real-time Interactions**: Utilizing JavaScript, the forum supports real-time posting and responses without needing to refresh the page.
- **Data Managemen**t: Migrations directory suggests a system in place for handling database schema updates, ensuring the application adapts over time to new requirements.


## Installation
1. First clone the repository (if you do not have all the files stored already)
   
   git clone https://github.com/Radrados/agileProject.git

4. Navigate to the project director in terminal

5. (optional but recommended) Create a Python virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the required dependencies using the requirements.txt file:
```bash
pip install -r requirements.txt
```
Now your project should be ready to run


## Running the Applications
To run this project:

1. Set the Flask application environment variable:
```bash
export FLASK_APP=main.py
```


2. Run the application:
```bash
flask run
```
