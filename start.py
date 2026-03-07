
d = { 
    'tasks': [],
    'times': [],
    'urgency': [],
    'start': '',
    'end': '',
    'workingTime': 0   
}
done = False

RED = '\033[91m'
BOLD = '\033[1m'
END = '\033[0m'
WHITE = '\033[37m'

print(WHITE +'Welcome to your daily task manager! ')

#### Calculate working times ####
print('What times would you like to wake up, start and finish work today? ')
d['start'] = (input('Wake up time (24hr format, e.g. 07:00): '))
d['end'] = (input('Finish work time (24hr format, e.g. 17:00): '))

def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def minutes_to_time(mins):
    hours = mins // 60
    minutes = mins % 60
    return f"{hours:02d}:{minutes:02d}"

d['start'] = time_to_minutes(d['start'])
d['end'] = time_to_minutes(d['end'])

# Minutes to work
d['workingTime'] = d['end'] - d['start']

print('Type "done" when you are finished entering your tasks ' \
    '\nEnter your tasks and how long they will take (minutes) one at a time as well as urgency out of 10 (with 10 being most urgent)): ' \
    '\nExample: "Do the dishes, 30, 3" ')

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
print(d)

if d['workingTime'] < sum(d['times']):
    print(RED + BOLD +'Warning: Your tasks exceed your available working time! Good luck with that!' + END)

sort_choice = input('How would you like to sort your tasks? (type "time" or "urgency") ')
if sort_choice == 'time':
    sorted_tasks = sorted(zip(d['tasks'], d['times']), key=lambda x: x[1], reverse=True) 
elif sort_choice == 'urgency':
    sorted_tasks = sorted(zip(d['tasks'], d['urgency']), key=lambda x: x[1], reverse=True)

taskTimetable =[d['start']]
for i in range(len(sorted_tasks)):
    taskTimetable.append(taskTimetable[i] + sorted_tasks[i][1])
    print(taskTimetable)
for i in range(len(taskTimetable)):
    taskTimetable[i] = minutes_to_time(taskTimetable[i])

print(BOLD + str(taskTimetable) +','+ str(sorted_tasks) + END)
