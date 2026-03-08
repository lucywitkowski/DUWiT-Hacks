import customtkinter as ctk
import ollama
import threading

# Set appearance and theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("lavender.json")

#### Main functionality ####
# dictionary to store user inputs and calculated values
d = { 
    'tasks': [],
    'times': [],
    'urgency': [],
    'start': '',
    'end': '',
    'workingTime': 0   
}
# convert time string to minutes for easier calculations
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes
#convert minutes back to time string for output
def minutes_to_time(mins):
    hours = mins // 60
    minutes = mins % 60
    return f"{hours:02d}:{minutes:02d}"
# function to add a task to the list based on user input from the GUI, with validation for empty fields and non-numeric time input, and updates the task list display in the GUI
def add_task():
    # get user input from the task name, time, and urgency fields in the GUI
    name = task_name.get().strip()
    time = task_time.get().strip()
    urgency = round(urgency_slider.get())

    # Validation
    # check name and time are not empty
    if not name or not time:
        output.insert("end", "Please enter both task name and time.\n")
        return
    # check time is a number
    if not time.isdigit():
        output.insert("end", f"Invalid time '{time}'. Please enter a number.\n")
        task_time.delete(0, "end")
        return
    # once validated, add the task to the dictionary and update the task list display in the GUI
    d['tasks'].append(name)
    d['times'].append(int(time))
    d['urgency'].append(int(urgency))

    # update the task list display in the GUI with the new task, showing its name, time requirement, and urgency level
    task_list.insert("end", f"{name} | {time} min | urgency {urgency}\n")
    task_name.delete(0, "end")
    task_time.delete(0, "end")
    urgency_slider.set(5)

# function to generate schedule based on user inputs and sorting preference
def generate_schedule():
    # clear the output textbox before generating a new schedule
    output.delete("1.0", "end")
    start_entry = f"{start_hr.get()}:{start_min.get()}"
    end_entry = f"{end_hour.get()}:{end_min.get()}"
    # convert start and end times to minutes and calculate total working time available
    d['start'] = time_to_minutes(start_entry)
    d['end'] = time_to_minutes(end_entry)
    d['workingTime'] = d['end'] - d['start']
    # check if total task time exceeds available working time and display a warning in the output textbox if so
    if d['workingTime'] < sum(d['times']):
        output.insert("end", "WARNING: Tasks exceed available working time!\n\n")
    # determine sorting preference from the radio buttons in the GUI and sort the tasks accordingly, either by time required, urgency level, or using ollama's language model for a smart schedule
    sort_choice = sort_var.get()
    if sort_choice == "time":
        # sort by duration
        sorted_tasks = sorted(zip(d['tasks'], d['times']), key=lambda x: x[1], reverse=True)
    elif sort_choice == 'ai':
        # let ai sort it 
        run_ai_schedule()
        return
    else:
        # sort by urgency
        sorted_tasks = sorted(zip(d['tasks'], d['times'], d['urgency']), key=lambda x: x[2], reverse=True)
        # reduce to (task, duration) for scheduling loop
        sorted_tasks = [(task, duration) for task, duration, urgency in sorted_tasks]
    # Initialize
    taskTimetable = []
    current_time = d['start']
    sinceBreak = 0
    # Define break rules
    BREAK_INTERVAL = 90
    BREAK_DURATION = 15
    # Loop through sorted tasks and build the timetable, inserting breaks as needed based on the defined break rules
    for task, duration in sorted_tasks:
        # Insert breaks as needed before task
        while sinceBreak >= BREAK_INTERVAL:
            taskTimetable.append((current_time, "Break"))
            current_time += BREAK_DURATION
            sinceBreak = 0

        taskTimetable.append((current_time, task))
        current_time += duration
        sinceBreak += duration

    # Display schedule
    output.insert("end", "Your Task Schedule\n")
    output.insert("end", f"Start time: {minutes_to_time(d['start'])}\n\n")
    for time_min, task in taskTimetable:
        output.insert("end", f"{minutes_to_time(time_min)}  {task}\n")

# function to generate schedule using ollama's language model based on user inputs and rules for scheduling
def ollama_schedule():
    tasks = ''
    for task, time, urgency in zip(d['tasks'], d['times'], d['urgency']):
        tasks += f"{task} (time: {time} min, urgency: {urgency}/10)\n"
    # create a prompt for the language model that includes the user's tasks, their time requirements, urgency levels, and the rules for scheduling
    prompt = f"""
    I have the following tasks to complete today. Each task includes the estimated duration in minutes and an urgency rating from 1 (least urgent) to 10 (most urgent):

    Tasks:
    {tasks}

    My workday starts at {minutes_to_time(d['start'])} and ends at {minutes_to_time(d['end'])}.

    Please generate a detailed timetable for me following these rules:

    1. Prioritize tasks based on urgency, but try to fit in as many tasks as possible within the available working time.
    2. Avoid long stretches of continuous work. Schedule a 15-minute break every 90 minutes of work.
    3. If possible, alternate between long and short tasks to maintain focus and energy.
    4. Do not split tasks in the middle; each task should be scheduled in a single block.
    5. Include start and end times for each task and break in HH:MM format.
    6. If not all tasks can fit, clearly indicate which tasks could not be scheduled.
    7. Format the output in a clean timetable, e.g.:
    09:00 - 09:45 Task A
    09:45 - 10:30 Task B
    10:30 - 10:45 Break
    ...

    Please create the most efficient, balanced schedule possible that maximizes productivity and prevents burnout.
    """
    # send the prompt to the language model and return the generated schedule as a string
    response = ollama.chat(
        model ='llama3',
        messages=[{'role': 'user', 'content': prompt}]
    )
    # return the respose from the language model
    return response['message']['content']

# function to run the ollama scheduling in a separate thread to avoid freezing the GUI while waiting for the response from the language model
def run_ai_schedule():
    output.delete("1.0", "end")
    output.insert("end", "Generating smart schedule...\nPlease wait.\n")
    # define a worker function to run the ollama scheduling and update the output textbox with the generated schedule once it's received
    def worker():
        schedule = ollama_schedule()

        output.delete("1.0", "end")
        output.insert("end", schedule)
    # create and start a new thread to run the worker function
    thread = threading.Thread(target=worker)
    thread.start()
#### Main window setup ####
# create the main application window using customtkinter, set its title and size, and add a title label at the top of the window
app = ctk.CTk()
app.title("Daily Task Manager")
app.geometry("700x700")
# add a title label at the top of the window
# Header frame
header_frame = ctk.CTkFrame(app, fg_color="#6a5acd", corner_radius=15)
header_frame.pack(fill="x", pady=10, padx=10)

# Main title
title = ctk.CTkLabel(header_frame, text="Daily Task Manager", font=ctk.CTkFont(size=28, weight="bold"), text_color="white")
title.pack(pady=(10,0))

# Subtitle
subtitle = ctk.CTkLabel(header_frame, text="Plan your day efficiently and prevent burnout!", font=ctk.CTkFont(size=14, weight="normal"), text_color="white")
subtitle.pack(pady=(0,10))

# Make the window scrollable 
main_frame = ctk.CTkScrollableFrame(app)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

#### Top Frame (side by side inputs) ####
# create a frame to hold the time inputs and task entry side by side
top_frame = ctk.CTkFrame(main_frame)
top_frame.pack(fill="x", pady=10)
# configure the grid layout of the top frame to have 2 columns that expand equally to fill the available space
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)

#### Time Inputs (LEFT) ####
# create a frame to hold the time input widgets and arrange them in a grid layout
time_frame = ctk.CTkFrame(top_frame)
time_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# possible values for hours and minutes
hourVals = [f"{i:02d}" for i in range(24)]
minuteVals = ['00', '15', '30', '45']

# user enters start work  time
ctk.CTkLabel(time_frame, text="Start Time").grid(row=0, column=0, columnspan=3, pady=5)
# hour
start_hr = ctk.CTkComboBox(time_frame, values=hourVals, width=70)
start_hr.set("09")
start_hr.grid(row=1, column=0, padx=5)
# colon
ctk.CTkLabel(time_frame, text=":").grid(row=1, column=1)
#minute
start_min = ctk.CTkComboBox(time_frame, values=minuteVals, width=70)
start_min.set("00")
start_min.grid(row=1, column=2, padx=5)

#spacing 
ctk.CTkLabel(time_frame, text="   ").grid(row=1, column=3)

# user enters end of work time
ctk.CTkLabel(time_frame, text="End Time").grid(row=0, column=4, columnspan=3, pady=5)
# hour
end_hour = ctk.CTkComboBox(time_frame, values=hourVals, width=70)
end_hour.set("17")
end_hour.grid(row=1, column=4, padx=5)
# colon
ctk.CTkLabel(time_frame, text=":").grid(row=1, column=5)
# minute
end_min = ctk.CTkComboBox(time_frame, values=minuteVals, width=70)
end_min.set("00")
end_min.grid(row=1, column=6, padx=5)

#### Task Entry (RIGHT) ####

# create a frame to hold the task entry widgets and arrange them in a grid layout
task_frame = ctk.CTkFrame(top_frame)
task_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# create input fields for task name, time required, and urgency level, along with a button to add the task to the list
# task name input
ctk.CTkLabel(task_frame, text="Task").pack(pady=3)
task_name = ctk.CTkEntry(task_frame)
task_name.pack(pady=3)

# time required input
ctk.CTkLabel(task_frame, text="Minutes").pack(pady=3)
task_time = ctk.CTkEntry(task_frame)
task_time.pack(pady=3)

#urgency slider input
ctk.CTkLabel(task_frame, text="Urgency").pack(pady=3)
# create a slider for the user to input the urgency level of the task, with a range from 1 to 10 and a default value of 5, and display the current value of the slider in a label above it
urgency_value = ctk.StringVar(value="5")
urgency_label = ctk.CTkLabel(task_frame, textvariable=urgency_value)
urgency_label.pack()

# function to update the displayed urgency value when the slider is moved, rounding the slider value to the nearest whole number for display
def update_urgency(value):
    urgency_value.set(str(round(value)))

# create the urgency slider with a range from 1 to 10, allowing only whole number steps, and set its command to the update_urgency function to update the displayed value when the slider is moved
urgency_slider = ctk.CTkSlider(
    task_frame,
    from_=1,
    to=10,
    number_of_steps=9,
    command=update_urgency
)

urgency_slider.set(5)
urgency_slider.pack(pady=5)

# add task button 
add_btn = ctk.CTkButton(task_frame, text="Add Task", command=add_task)
add_btn.pack(pady=10)

#### Task List ####
# create a textbox to display the list of tasks added by the user, along with their time requirements and urgency levels
task_list = ctk.CTkTextbox(main_frame, height=120)
task_list.pack(fill="x", pady=10)

#### Sorting Option ####
# create a frame to hold the sorting option radio buttons and arrange them horizontally
sort_frame = ctk.CTkFrame(main_frame)
sort_frame.pack(pady=10)
# create radio buttons to allow the user to choose whether to sort tasks by time required or urgency level when generating the schedule
sort_var = ctk.StringVar(value="time")
# create radio button for sorting by time required and pack it into the sort frame
time_radio = ctk.CTkRadioButton(sort_frame, text="Sort by Time", variable=sort_var, value="time")
time_radio.pack(side="left", padx=10)
# create radio button for sorting by urgency level and pack it into the sort frame
urgency_radio = ctk.CTkRadioButton(sort_frame, text="Sort by Urgency", variable=sort_var, value="urgency")
urgency_radio.pack(side="left", padx=10)
# create radio button for sorting by ollama's language model and pack it into the sort frame
ollama_radio = ctk.CTkRadioButton(sort_frame, text="✨ Smart Schedule", variable=sort_var, value="ai")
ollama_radio.pack(side="left", padx=10)

#### Generate Schedule Button ####

# create a button to generate the schedule based on the user inputs and sorting preference, and set its command to the generate_schedule function
generate_btn = ctk.CTkButton(main_frame, text="Generate Schedule", command=generate_schedule)
generate_btn.pack(pady=15)

#### Output Schedule to the user ####

# create a textbox to display the generated schedule to the user after they click the "Generate Schedule" button, showing the start time and the scheduled tasks with their respective times
output = ctk.CTkTextbox(main_frame, height=250)
output.pack(fill="both", expand=True, pady=10)





# start the main event loop to run the application
app.mainloop()
