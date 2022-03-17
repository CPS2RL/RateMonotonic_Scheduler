from drs import drs
import random
import copy
import json
import numpy as np
overalU = []
result = []
taskset = []
tasks = dict()

periods = np.arange(50, 1000, 50).tolist()
WCET = []
tasksetPeriods = []
tasksetWCET = []


for i in range(1,11):
    overalU.append(i/10)
print(overalU)
"""
for i in range(len(overalU)-1):
    a = overalU[i]
    b = overalU[i+1]
    drsResult = drs(7,random.uniform(a,b))
    result.append(drsResult)
"""
for i in range(10):
    a = 0.02 +0.1*i
    b = 0.08 +0.1*i
    tas = random.randint(3,10)
    drsResult = drs(tas,random.uniform(a,b))
    result.append(drsResult)

print(result)


for i in range(len(result)):
    for j in range(len(result[i])):
        tasks[j]= {}
        indexT = random.randint(0,len(periods)-1)
        T = periods[indexT]
        tasks[j]["Period"] = T
        tasks[j]["WCET"] = int(T*result[i][j])

        tasks[j]["Secure"] = random.randint(0,1)
        tasks[j]["Observer"] = 0
    taskset.append(copy.deepcopy(tasks))
    tasks.clear()

task = {"taskset":taskset}
with open('taskset1.json', 'w') as f:
    json.dump(task, f)