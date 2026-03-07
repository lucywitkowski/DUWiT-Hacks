d = { 
    'tasks': [],
    'times': []   
}
done = False

print('Welcome to your daily task manager! ')

#### Calculate working times
print('What times would you like to wake up, start and finish work today? ' \)


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