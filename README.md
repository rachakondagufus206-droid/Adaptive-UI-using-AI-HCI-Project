## AI-Based Adaptive Task Manager
### Project Overview

AI Based Adaptive Task Manager is a Python desktop application designed for the purpose of showing adaptive task management for human-computer interaction. The application stores the categories of tasks and uses the information about interactions and determines a preferred category. The interface adapts to forecasted preference in use of application.

### Technologies Used

The application is written in Python main programming language. The GUI is designed using Tkinter and the machine learning capabilities are implemented using scikit-learn. The preferred task category is predicted using a Decision Tree Classifier.

### Main Features

There is an Application for Work, Study, and Personal task categories. This includes task addition, task completion, interaction tracking, adaptive recommendations and interface reset. The list of title, description, category selection and recommendation will change based on the anticipated preference.

### Adaptive Behavior

The category selections of the tasks are recorded as interaction history throughout use of the application. The Decision Tree is used to analyse the frequency of interactions, and to determine the category of the observed activity. The elements of the graphical interface that are automatically changed are shown in the predicted category.

### Sample Testing

The combinations of Work, Study, and Personal tasks vary when people are tested to show evidence of adaptive behaviour. Study-focused interface and automatic preference to Study category can result from repeated Study interactions. Other interactions may alter the prediction and show runtime adaptation.

### Installation

Python 3.x and scikit-learn are required to run the application. tkinter comes pre-installed with most desktop environments and all standard Python installations. The application can be started by running the adaptive_task_manager.py file.

### Project Files

The entire adaptive task manager application is contained in the file adaptive_task_manager.py. The README.md file contains project details, setup instructions, project features and testing information. 

### Project Purpose

The project is an example of the use of artificial intelligence for personalized human-computer interaction. History of interaction is used for preferences prediction and interface behavior adaptation. The implementation introduces a simple example of an adaptive user interface that is implemented with the support of AI.
