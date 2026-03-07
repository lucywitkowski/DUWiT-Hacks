import tkinter as tk
from tkinter import ttk

#### Set Up Data Structures and Variables ####
# store tasks, times, urgency, start and end times, and total working time in a dictionary
d = { 
    'tasks': [],
    'times': [],
    'urgency': [],
    'start': '',
    'end': '',
    'workingTime': 0   
}
# flag to indicate when the user is done entering tasks
done = False
# ANSI escape codes for colored and bold text
RED = '\033[91m'
BOLD = '\033[1m'
END = '\033[0m'
WHITE = '\033[37m'

# Welcome message
print(WHITE +'Welcome to your daily task manager! ')

#### Calculate working times ####
print('What times would you like to wake up, start and finish work today? ')
d['start'] = (input('Wake up time (24hr format, e.g. 07:00): '))
d['end'] = (input('Finish work time (24hr format, e.g. 17:00): '))

# functions to convert time between "HH:MM" format and total minutes for easier calculations
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

# function to convert minutes back to "HH:MM" format for display
def minutes_to_time(mins):
    hours = mins // 60
    minutes = mins % 60
    return f"{hours:02d}:{minutes:02d}"

# Convert start and end times to minutes for calculations
d['start'] = time_to_minutes(d['start'])
d['end'] = time_to_minutes(d['end'])

# Minutes to work
d['workingTime'] = d['end'] - d['start']

# Prompt user to enter tasks, times, and urgency
print('Type "done" when you are finished entering your tasks ' \
    '\nEnter your tasks and how long they will take (minutes) one at a time as well as urgency out of 10 (with 10 being most urgent)): ' \
    '\nExample: "Do the dishes, 30, 3" ')

# Loop to collect tasks until the user types "done"
while done == False:
    newtask = input()
    if newtask == 'done':
        done = True
    else:
        taskname = newtask.split(',')[0]
        tasktime = newtask.split(',')[1]
        taskurgency = newtask.split(',')[2]
        d['tasks'].append(taskname)
        d['times'].append(int(tasktime))
        d['urgency'].append(int(taskurgency))

# Check if total task time exceeds available working time and print a warning if so
if d['workingTime'] < sum(d['times']):
    print(RED + BOLD +'Warning: Your tasks exceed your available working time! Good luck with that!' + END)

# Ask user how they would like to sort their tasks and sort accordingly
sort_choice = input('How would you like to sort your tasks? (type "time" or "urgency") ')
if sort_choice == 'time':
    sorted_tasks = sorted(zip(d['tasks'], d['times']), key=lambda x: x[1], reverse=True) 
elif sort_choice == 'urgency':
    sorted_tasks = sorted(zip(d['tasks'], d['urgency']), key=lambda x: x[1], reverse=True)
else:
    print('Invalid input. Sorting by time...')
    sorted_tasks = sorted(zip(d['tasks'], d['times']), key=lambda x: x[1], reverse=True)

# Create a timetable for the tasks based on the sorted order and print it out
taskTimetable =[d['start']]
for i in range(len(sorted_tasks)):
    taskTimetable.append(taskTimetable[i] + sorted_tasks[i][1])
for i in range(len(taskTimetable)):
    taskTimetable[i] = minutes_to_time(taskTimetable[i])
print(BOLD + 'Your Task Schedule:' + END)
print(f'Start time: {taskTimetable[0]}')
for i in range(len(sorted_tasks)):
    print(f'{taskTimetable[i+1]}  {sorted_tasks[i][0]}')
