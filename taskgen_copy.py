from drs import drs
import random
import copy
overalU = []
result = []
taskset = []
tasks = dict()

periods = []
WCET = []
tasksetPeriods = []
tasksetWCET = []


for i in range(1,11):
    overalU.append(i/10)
print(overalU)

for i in range(len(overalU)-1):
    a = overalU[i]
    b = overalU[i+1]
    print(a,b)
    drsResult = drs(7,random.uniform(a,b))
    print(drsResult)
    result.append(drsResult)


for i in range(len(result)):
    for j in range(len(result[i])):
        tasks[j]= {}
        T = random.randint(10,1000)
        tasks[j]["Period"] = T
        tasks[j]["WCET"] = int(T*result[i][j])
        tasks[j]["Secure"] = random.randint(0,1)
        tasks[j]["Observer"] = 0
        print(tasks)
    taskset.append(copy.deepcopy(tasks))
    tasks.clear()

print(taskset)