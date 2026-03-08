import customtkinter as ctk

# Set appearance and theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("lavender.json")

#### Main functionality ####
# dictonary to store user inputs and calculated values
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

# function to add task to dictonary and display in task list
def add_task():
    name = task_name.get()
    time = task_time.get()
    urgency = round(urgency_slider.get())
    # basic validation to ensure all fields are filled and time is a number
    if name and time and urgency:
        d['tasks'].append(name)
        d['times'].append(int(time))
        d['urgency'].append(int(urgency))
        # display task in task list
        task_list.insert("end", f"{name} | {time} min | urgency {urgency}\n")
        # clear input fields for next entry
        task_name.delete(0, "end")
        task_time.delete(0, "end")
        urgency_slider.set(5)

# function to generate schedule based on user inputs and sorting preference
def generate_schedule():
    # clear previous output
    output.delete("1.0", "end")
    start_entry = f"{start_hr.get()}:{start_min.get()}"
    end_entry = f"{end_hour.get()}:{end_min.get()}"

    # convert start and end times to minutes and calculate total working time
    d['start'] = time_to_minutes(start_entry)
    d['end'] = time_to_minutes(end_entry)
    d['workingTime'] = d['end'] - d['start']

    # check if total task time exceeds working time and display warning if it does
    if d['workingTime'] < sum(d['times']):
        output.insert("end", "WARNING: Tasks exceed available working time!\n\n")

    # sort tasks based on user preference (time or urgency)
    sort_choice = sort_var.get()
    if sort_choice == "time":
        sorted_tasks = sorted(zip(d['tasks'], d['times']), key=lambda x: x[1], reverse=True)
    else:
        sorted_tasks = sorted(zip(d['tasks'], d['urgency']), key=lambda x: x[1], reverse=True)
   
    # create a timetable based on sorted tasks and calculate start times for each task
    taskTimetable =[d['start']]
    # calculate start time for each task by adding the duration of the previous task to the start time of the previous task
    for i in range(len(sorted_tasks)):
        taskTimetable.append(taskTimetable[i] + sorted_tasks[i][1])
    # convert timetable from minutes back to time strings for output
    for i in range(len(taskTimetable)):
        taskTimetable[i] = minutes_to_time(taskTimetable[i])
    # display the generated schedule in the output textbox
    output.insert("end", "Your Task Schedule\n")
    output.insert("end", f"Start time: {taskTimetable[0]}\n\n")
    # loop through sorted tasks and display each task with its corresponding start time in the output textbox
    for i in range(len(sorted_tasks)):
        output.insert("end", f"{taskTimetable[i+1]}  {sorted_tasks[i][0]}\n")


#### Main window setup ####
app = ctk.CTk()
app.title("Daily Task Manager")
app.geometry("700x700")

title = ctk.CTkLabel(app, text="Daily Task Manager", font=("Arial", 22, "bold"))
title.pack(pady=20)

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

urgency_value = ctk.StringVar(value="5")

urgency_label = ctk.CTkLabel(task_frame, textvariable=urgency_value)
urgency_label.pack()

def update_urgency(value):
    urgency_value.set(str(round(value)))

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

#### Generate Schedule Button ####

generate_btn = ctk.CTkButton(main_frame, text="Generate Schedule", command=generate_schedule)
generate_btn.pack(pady=15)

#### Output Schedule to the user ####

output = ctk.CTkTextbox(main_frame, height=250)
output.pack(fill="both", expand=True, pady=10)

# start the main event loop to run the application
app.mainloop()