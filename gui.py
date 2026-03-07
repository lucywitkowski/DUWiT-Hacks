import customtkinter as ctk

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("lavender.json")

# ===== Original data structure =====
d = { 
    'tasks': [],
    'times': [],
    'urgency': [],
    'start': '',
    'end': '',
    'workingTime': 0   
}

def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def minutes_to_time(mins):
    hours = mins // 60
    minutes = mins % 60
    return f"{hours:02d}:{minutes:02d}"

# ===== Functions =====

def add_task():
    name = task_name.get()
    time = task_time.get()
    urgency = task_urgency.get()

    if name and time and urgency:
        d['tasks'].append(name)
        d['times'].append(int(time))
        d['urgency'].append(int(urgency))

        task_list.insert("end", f"{name} | {time} min | urgency {urgency}")

        task_name.delete(0, "end")
        task_time.delete(0, "end")
        task_urgency.delete(0, "end")


def generate_schedule():

    output.delete("1.0", "end")

    d['start'] = time_to_minutes(start_entry.get())
    d['end'] = time_to_minutes(end_entry.get())
    d['workingTime'] = d['end'] - d['start']

    if d['workingTime'] < sum(d['times']):
        output.insert("end", "WARNING: Tasks exceed available working time!\n\n")

    sort_choice = sort_var.get()

    if sort_choice == "time":
        sorted_tasks = sorted(zip(d['tasks'], d['times']), key=lambda x: x[1], reverse=True)
    else:
        sorted_tasks = sorted(zip(d['tasks'], d['urgency']), key=lambda x: x[1], reverse=True)

    taskTimetable =[d['start']]

    for i in range(len(sorted_tasks)):
        taskTimetable.append(taskTimetable[i] + sorted_tasks[i][1])

    for i in range(len(taskTimetable)):
        taskTimetable[i] = minutes_to_time(taskTimetable[i])

    output.insert("end", "Your Task Schedule\n")
    output.insert("end", f"Start time: {taskTimetable[0]}\n\n")

    for i in range(len(sorted_tasks)):
        output.insert("end", f"{taskTimetable[i+1]}  {sorted_tasks[i][0]}\n")


# ===== Main Window =====

app = ctk.CTk()
app.title("Daily Task Manager")
app.geometry("520x650")

title = ctk.CTkLabel(app, text="Daily Task Manager", font=("Arial", 22, "bold"))
title.pack(pady=20)


# ===== Time Inputs =====

time_frame = ctk.CTkFrame(app)
time_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(time_frame, text="Wake Up Time (HH:MM)").pack(pady=5)
start_entry = ctk.CTkEntry(time_frame)
start_entry.pack(pady=5)

ctk.CTkLabel(time_frame, text="Finish Work Time (HH:MM)").pack(pady=5)
end_entry = ctk.CTkEntry(time_frame)
end_entry.pack(pady=5)


# ===== Task Entry =====

task_frame = ctk.CTkFrame(app)
task_frame.pack(pady=15, padx=20, fill="x")

ctk.CTkLabel(task_frame, text="Task").pack(pady=3)
task_name = ctk.CTkEntry(task_frame)
task_name.pack(pady=3)

ctk.CTkLabel(task_frame, text="Minutes").pack(pady=3)
task_time = ctk.CTkEntry(task_frame)
task_time.pack(pady=3)

ctk.CTkLabel(task_frame, text="Urgency (1-10)").pack(pady=3)
task_urgency = ctk.CTkEntry(task_frame)
task_urgency.pack(pady=3)

add_btn = ctk.CTkButton(task_frame, text="Add Task", command=add_task)
add_btn.pack(pady=10)


# ===== Task List =====

task_list = ctk.CTkTextbox(app, height=120)
task_list.pack(padx=20, pady=10, fill="x")


# ===== Sorting Option =====

sort_frame = ctk.CTkFrame(app)
sort_frame.pack(pady=10)

sort_var = ctk.StringVar(value="time")

time_radio = ctk.CTkRadioButton(sort_frame, text="Sort by Time", variable=sort_var, value="time")
time_radio.pack(side="left", padx=10)

urgency_radio = ctk.CTkRadioButton(sort_frame, text="Sort by Urgency", variable=sort_var, value="urgency")
urgency_radio.pack(side="left", padx=10)


# ===== Generate Button =====

generate_btn = ctk.CTkButton(app, text="Generate Schedule",command=generate_schedule)
generate_btn.pack(pady=15)


# ===== Output =====

output = ctk.CTkTextbox(app, height=180)
output.pack(padx=20, pady=10, fill="both", expand=True)


app.mainloop()