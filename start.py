
d = { 
    'tasks': [],
    'times': [],
    'start': '',
    'end': '',
    'workingTime': 0   
}
done = False

RED = '\033[91m'
BOLD = '\033[1m'
END = '\033[0m'

print('Welcome to your daily task manager! ')

#### Calculate working times ####
print('What times would you like to wake up, start and finish work today? ')
d['start'] = (input('Wake up time (24hr format, e.g. 07:00): '))
d['end'] = (input('Finish work time (24hr format, e.g. 17:00): '))

def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

d['start'] = time_to_minutes(d['start'])
d['end'] = time_to_minutes(d['end'])

# Minutes to work
d['workingTime'] = d['end'] - d['start']

print('Type "done" when you are finished entering your tasks ' \
    '\nEnter your tasks and how long they will take (minutes) one at a time:' \
    '\nExample: "Do the dishes, 30"')

while done == False:
    newtask = input()
    if newtask == 'done':
        done = True
    else:
        taskname = newtask.split(',')[0]
        tasktime = newtask.split(',')[1]
        d['tasks'].append(taskname)
        d['times'].append(int(tasktime))
print(d)

if d['workingTime'] < sum(d['times']):
    print(RED + BOLD +'Warning: Your tasks exceed your available working time! Good luck with that!' + END)

