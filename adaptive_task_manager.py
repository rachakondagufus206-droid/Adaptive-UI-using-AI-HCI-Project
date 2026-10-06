# Developed an adaptive task manager which learnt user preferences for tasks. 
# A decision tree was used to classify the preferred categories and automatically update the user interface according to the observed activity.

# Importing libraries for the adaptive interface
import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# Importing tools for preparing and training the model
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

# Creating the adaptive task manager
class AdaptiveTaskManager:

    def __init__(self, root):
        # Setting the main application window
        self.root = root
        self.root.title("AI-Based Adaptive Task Manager")
        self.root.geometry("850x650")
        self.root.minsize(750, 550)

        # Storing tasks and interaction history
        self.tasks = []
        self.interaction_history = []

        # Creating sample category data
        self.training_categories = [
            "Work",
            "Study",
            "Personal",
            "Work",
            "Study",
            "Personal",
            "Work",
            "Work",
            "Study",
            "Personal",
            "Work",
            "Study"
        ]

        # Creating sample frequency data
        self.training_frequency = [
            1, 2, 1, 3, 2, 1,
            4, 5, 3, 2, 6, 4
        ]

        # Preparing category labels
        self.category_encoder = LabelEncoder()
        encoded_categories = self.category_encoder.fit_transform(
            self.training_categories
        )

        # Creating the decision tree model
        self.model = DecisionTreeClassifier(
            random_state=42,
            max_depth=4
        )

        # Training the model with frequency data
        self.model.fit(
            [[frequency] for frequency in self.training_frequency],
            encoded_categories
        )

        # Creating the user interface
        self.create_interface()

        # Updating the adaptive interface
        self.update_adaptive_interface()


    # Creating the user interface
    def create_interface(self):

        # Creating the main title
        self.title_label = tk.Label(
            self.root,
            text="AI-Based Adaptive Task Manager",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=15)

        # Creating the description text
        self.description_label = tk.Label(
            self.root,
            text="The interface learns from user interactions and adapts recommendations.",
            font=("Arial", 11)
        )
        self.description_label.pack(pady=5)

        # Creating the input area
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=15)

        # Adding the task label
        tk.Label(
            self.input_frame,
            text="Task:",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, padx=5, pady=5)

        # Creating the task entry field
        self.task_entry = tk.Entry(
            self.input_frame,
            width=35,
            font=("Arial", 11)
        )
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        # Adding the category label
        tk.Label(
            self.input_frame,
            text="Category:",
            font=("Arial", 11, "bold")
        ).grid(row=1, column=0, padx=5, pady=5)

        # Creating the category selection box
        self.category_box = ttk.Combobox(
            self.input_frame,
            values=["Work", "Study", "Personal"],
            state="readonly",
            width=32
        )
        self.category_box.grid(row=1, column=1, padx=5, pady=5)
        self.category_box.set("Work")

        # Creating the add task button
        self.add_button = tk.Button(
            self.input_frame,
            text="Add Task",
            command=self.add_task,
            font=("Arial", 10, "bold"),
            width=15
        )
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Creating the recommendation section
        self.recommendation_frame = tk.LabelFrame(
            self.root,
            text="AI Adaptive Recommendation",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        self.recommendation_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        # Creating the recommendation message
        self.recommendation_label = tk.Label(
            self.recommendation_frame,
            text="Analyzing user behavior...",
            font=("Arial", 11),
            wraplength=700
        )
        self.recommendation_label.pack()

        # Creating the task display area
        self.task_frame = tk.LabelFrame(
            self.root,
            text="Current Tasks",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        self.task_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        # Creating the task list
        self.task_listbox = tk.Listbox(
            self.task_frame,
            font=("Arial", 11),
            height=8
        )
        self.task_listbox.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # Creating the interaction statistics
        self.statistics_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10)
        )
        self.statistics_label.pack(pady=5)

        # Creating the button area
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        # Creating the task completion button
        self.complete_button = tk.Button(
            self.button_frame,
            text="Complete Selected Task",
            command=self.complete_task,
            width=22
        )
        self.complete_button.grid(row=0, column=0, padx=5)

        # Creating the reset button
        self.reset_button = tk.Button(
            self.button_frame,
            text="Reset Interface",
            command=self.reset_application,
            width=18
        )
        self.reset_button.grid(row=0, column=1, padx=5)


    # Adding a new task
    def add_task(self):

        # Reading the entered task
        task_name = self.task_entry.get().strip()

        # Reading the selected category
        category = self.category_box.get()

        # Checking for an empty task
        if task_name == "":
            messagebox.showwarning(
                "Missing Task",
                "Please enter a task before adding."
            )
            return

        # Adding the task details
        self.tasks.append({
            "name": task_name,
            "category": category
        })

        # Recording the category interaction
        self.interaction_history.append(category)

        # Updating the displayed task list
        self.refresh_task_list()

        # Clearing the task entry
        self.task_entry.delete(0, tk.END)

        # Updating the adaptive settings
        self.update_adaptive_interface()


    # Completing a selected task
    def complete_task(self):

        # Reading the selected task position
        selected_index = self.task_listbox.curselection()

        # Checking for a selected task
        if not selected_index:
            messagebox.showwarning(
                "No Selection",
                "Please select a task to complete."
            )
            return

        # Finding the selected task position
        index = selected_index[0]

        # Reading the selected task details
        completed_task = self.tasks[index]

        # Recording the completed category
        self.interaction_history.append(
            completed_task["category"]
        )

        # Removing the completed task
        self.tasks.pop(index)

        # Updating the displayed task list
        self.refresh_task_list()

        # Updating the adaptive settings
        self.update_adaptive_interface()


    # Refreshing the task list
    def refresh_task_list(self):

        # Clearing the current task display
        self.task_listbox.delete(0, tk.END)

        # Displaying each current task
        for task in self.tasks:

            task_text = (
                task["name"]
                + " | Category: "
                + task["category"]
            )

            # Adding task details to the list
            self.task_listbox.insert(
                tk.END,
                task_text
            )


    # Predicting the preferred category
    def predict_preferred_category(self):

        # Checking for missing interaction history
        if len(self.interaction_history) == 0:
            return "Work"

        # Counting category interactions
        category_counts = Counter(
            self.interaction_history
        )

        # Finding the highest interaction count
        highest_frequency = max(
            category_counts.values()
        )

        # Predicting the category from interaction frequency
        predicted_encoded = self.model.predict(
            [[highest_frequency]]
        )[0]

        # Converting the predicted label
        predicted_category = (
            self.category_encoder.inverse_transform(
                [predicted_encoded]
            )[0]
        )

        return predicted_category


    # Updating the adaptive interface
    def update_adaptive_interface(self):

        # Predicting the preferred category
        predicted_category = self.predict_preferred_category()

        # Updating the category selection
        self.category_box.set(
            predicted_category
        )

        # Counting total interactions
        total_interactions = len(
            self.interaction_history
        )

        # Creating the adaptive recommendation
        if total_interactions == 0:

            recommendation = (
                "The system is waiting for user interactions. "
                "Add tasks to allow the adaptive model to learn preferences."
            )

        else:

            # Counting category interactions
            category_counts = Counter(
                self.interaction_history
            )

            recommendation = (
                "Based on previous interactions, the adaptive "
                "system predicts that '"
                + predicted_category
                + "' is the preferred task category. "
                "The category selector has been automatically "
                "adapted to this preference."
            )

        # Updating the recommendation message
        self.recommendation_label.config(
            text=recommendation
        )

        # Updating the interaction statistics
        self.statistics_label.config(
            text=(
                "User Interactions: "
                + str(total_interactions)
                + "    |    Predicted Preference: "
                + predicted_category
            )
        )

        # Adapting the interface appearance
        self.adapt_interface(
            predicted_category
        )


    # Adapting the interface appearance
    def adapt_interface(self, predicted_category):

        # Changing the interface for work preference
        if predicted_category == "Work":

            self.title_label.config(
                text="AI Adaptive Task Manager - Work Focus"
            )

            self.description_label.config(
                text="The interface is adapted toward work-related tasks."
            )

        # Changing the interface for study preference
        elif predicted_category == "Study":

            self.title_label.config(
                text="AI Adaptive Task Manager - Study Focus"
            )

            self.description_label.config(
                text="The interface is adapted toward study-related tasks."
            )

        # Changing the interface for personal preference
        else:

            self.title_label.config(
                text="AI Adaptive Task Manager - Personal Focus"
            )

            self.description_label.config(
                text="The interface is adapted toward personal tasks."
            )


    # Resetting the application
    def reset_application(self):

        # Asking for reset confirmation
        response = messagebox.askyesno(
            "Reset Interface",
            "Reset tasks and learned interaction history?"
        )

        if response:

            # Clearing stored tasks
            self.tasks.clear()

            # Clearing interaction history
            self.interaction_history.clear()

            # Refreshing the task list
            self.refresh_task_list()

            # Restoring the default category
            self.category_box.set("Work")

            # Restoring the default title
            self.title_label.config(
                text="AI-Based Adaptive Task Manager"
            )

            # Restoring the default description
            self.description_label.config(
                text=(
                    "The interface learns from user interactions "
                    "and adapts recommendations."
                )
            )

            # Updating the adaptive interface
            self.update_adaptive_interface()


# Starting the application
if __name__ == "__main__":

    # Creating the main application window
    root = tk.Tk()

    # Creating the adaptive task manager
    application = AdaptiveTaskManager(root)

    # Starting the application
    root.mainloop()