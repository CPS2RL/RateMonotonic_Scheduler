#!/usr/bin/env python3
# ------------------------------------------
# RM_scheduling.py: RM
# Author: Aguida Mohamed Anis
# ------------------------------------------
import json
import copy
import  random
from sys import *
from math import gcd
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import statistics as st
from collections import defaultdict
from operator import itemgetter

from sortedcontainers import SortedDict
tasks = dict()
tasks_copy= dict()
tasks_phases = dict()
runningTasks = dict()
RealTime_task = dict()
metrics = defaultdict(dict)
d = dict()
dList = {}
T = []
C = []
U = []
# For gantt chart
y_axis  = []
from_x = []
to_x = []

ExecIntervals = []
ExecStart = []
ExecFinish = []
ExecTemp= []


def createIDLE():
	global dList
	dList["TASK_IDLE"] = {"start": [], "finish": []}


def createTask(taskID,phase,period,priority,WCET,secure,observer):
	global hp
	global tasks
	global tasks_copy
	global tasks_phases
	global dList

	dList["TASK_%d"%taskID] = {"start":[],"finish":[]}
	tasks[taskID] = {}
	tasks_copy[taskID] = {}
	tasks_phases[taskID] = {}
	tasks[taskID]["Phase"] = phase
	tasks_phases[taskID]["Phase"] = phase

	tasks[taskID]["Period"] = period
	tasks[taskID]["Priority"] = priority
	tasks[taskID]["WCET"] = WCET
	tasks[taskID]["Secure"] = secure
	tasks[taskID]["Observer"] = observer
	tasks_copy[taskID]= tasks[taskID]


def jsonTask(tasks):
	with open('tasks.json','w') as outfile:
		json.dump(tasks,outfile,indent = 4)

def Hyperperiod():
	"""
	Calculates the hyper period of the tasks to be scheduled
	"""
	temp = []
	n = len(tasks)
	for i in range(n):
		temp.append(tasks[i]["Period"])
	HP = temp[0]
	for i in temp[1:]:
		HP = HP*i//gcd(HP, i)
	print ("\n Hyperperiod:",HP)
	return HP

def Schedulablity():
	"""
	Calculates the utilization factor of the tasks to be scheduled
	and then checks for the schedulablity and then returns true is
	schedulable else false.
	"""
	for i in range(len(tasks)):
		T.append(int(tasks[i]["Period"]))
		C.append(int(tasks[i]["WCET"]))
		u = int(C[i])/int(T[i])
		U.append(u)

	U_factor = sum(U)
	if U_factor<=1:
		print("\nUtilization factor: ",U_factor, "underloaded tasks")
		n=len(tasks)
		sched_util = n*(2**(1/n)-1)
		print("Checking condition: ",sched_util)

		count = 0
		T.sort()
		for i in range(len(T)):
			if T[i]%T[0] == 0:
				count = count + 1

		# Checking the schedulablity condition
		if U_factor <= sched_util or count == len(T):
			print("\n\tTasks are schedulable by Rate Monotonic Scheduling!")
			return True
		else:
			print("\n\tTasks are not schedulable by Rate Monotonic Scheduling!")
			return False
	print("\n\tOverloaded tasks!")
	print("\n\tUtilization factor > 1")
	return False

def estimatePriority(RealTime_task):
	"""
	Estimates the priority of tasks at each real time period during scheduling
	"""
	tempPeriod = hp
	P = -1    #Returns -1 for idle tasks
	for i in RealTime_task.keys():
		if (RealTime_task[i]["WCET"] != 0):
			if (tempPeriod > RealTime_task[i]["Period"] or tempPeriod > tasks[i]["Period"]):
				tempPeriod = tasks[i]["Period"] #Checks the priority of each task based on period
				P = i
	return P


def observer_func(t,counter):
	ExecStart.append(t)
	ExecFinish.append(t+1)

def prio(RealTime_task):
	min = hp
	P = -1  # Returns -1 for idle tasks
	index = -1
	C = []
	for i in RealTime_task.keys():
		if (RealTime_task[i]["WCET"] != 0):
			if (min > RealTime_task[i]["Priority"] or min > tasks_copy[i]["Priority"]):
				min = tasks_copy [i]["Priority"]
				P = min
				index = i
	C.append(index)
	C.append(P)
	return C






#def runTask(phase):
#	for i in tasks:
#		if (phase==tasks[i]["Phase"]):
#			runningTasks[i] = tasks[i]
def Simulation(hp):
	"""
	The real time schedulng based on Rate Monotonic scheduling is simulated here.
	"""

	# Real time scheduling are carried out in RealTime_task
	global RealTime_task
	#RealTime_task = copy.deepcopy(tasks)
	# validation of schedulablity neessary condition
	#for i in RealTime_task.keys():
	#	RealTime_task[i]["DCT"] = RealTime_task[i]["WCET"]
	#	if (RealTime_task[i]["WCET"] > RealTime_task[i]["Period"]):
	#		print(" \n\t The task can not be completed in the specified time ! ", i )

	# main loop for simulator
	counter = 0
	for t in range(hp):
		#if len(RealTime_task)<len(tasks):
		#	runTask(t)
			#print(runningTasks)
		#	RealTime_task = copy.deepcopy(runningTasks)
		#	print("Real time:",RealTime_task)
		#print(RealTime_task)
		# Determine the priority of the given tasks
		for i in range(len(tasks_phases)):
			if (t==tasks_phases[i]["Phase"]):
				tasks[i]= copy.deepcopy(tasks_copy[i])
				RealTime_task[i]=copy.deepcopy(tasks_copy[i])
		#priority = estimatePriority(RealTime_task)
		pr = prio(RealTime_task)
		if not (pr):
			priority = -1
		else:
			index = pr[0]
			priority = pr[1]
		if (priority != -1):    #processor is not idle
			if (RealTime_task[index]["Observer"]==1):
				observer_func(t,counter)
				counter = counter + 1
			print("\nt{}-->t{} :TASK{}".format(t,t+1,index))
			# Update WCET after each clock cycle
			RealTime_task[index]["WCET"] -= 1
			# For the calculation of the metrics
			dList["TASK_%d"%index]["start"].append(t)
			dList["TASK_%d"%index]["finish"].append(t+1)
			# For plotting the results
			y_axis.append("TASK%d"%index)
			from_x.append(t)
			to_x.append(t+1)

		else:    #processor is idle
			#print("\nt{}-->t{} :IDLE".format(t,t+1))
			# For the calculation of the metrics
			dList["TASK_IDLE"]["start"].append(t)
			dList["TASK_IDLE"]["finish"].append(t+1)
			# For plotting the results
			y_axis.append("IDLE")
			from_x.append(t)
			to_x.append(t+1)

		# Update Period after each clock cycle
		for i in RealTime_task.keys():
			RealTime_task[i]["Period"] -= 1
			if (RealTime_task[i]["Period"] == 0):
				#print(tasks_copy[i])
				RealTime_task[i] = copy.deepcopy(tasks_copy[i])

		#with open('RM_sched.json','w') as outfile2:
		#	json.dump(dList,outfile2,indent = 4)


def drawGantt():
	"""
	The scheduled results are displayed in the form of a
	gantt chart for the user to get better understanding
	"""

	i=0
	j=0
	print(len(ExecStart) - 2)
	while (j <= len(ExecFinish)-1):
		while (j < len(ExecFinish)-1) and (ExecFinish[j]==ExecStart[j+1]):
			j= j+1
		ExecTemp.append({"start":ExecStart[i],"finish":ExecFinish[j]})
		j=j+1
		i=j
	for i in tasks.keys():
		if (tasks[i]["Observer"]==1):
			print("Execution intervals of the observer task: \r\n",ExecTemp)
			break

	n= len(tasks)
	colors = ['red','green','blue','orange','yellow']
	fig = plt.figure()
	ax = fig.add_subplot(111)
	# the data is plotted from_x to to_x along y_axis
	ax = plt.hlines(y_axis, from_x, to_x, linewidth=20, color = colors[n-1])
	plt.title('Rate Monotonic scheduling')
	plt.grid(True)
	plt.xlabel("Real-Time clock")
	plt.ylabel("HIGH------------------Priority--------------------->LOW")
	plt.xticks(np.arange(min(from_x), max(to_x)+1, 1.0))
	plt.show()




def generateExecInter(hyperperiod,observerExec):
	ladder =[0] * hyperperiod
	for i in range(len(observerExec)):
		for j in range(observerExec[i]["start"],observerExec[i]["finish"]):
			ladder[j]=1
	return ladder

def timewindow(victimperiod,ladder):
	result = [0] * victimperiod
	for i in range(len(ladder)):
		result[i % victimperiod] += ladder[i]
	print(result)
	for i in range(len(result)):
		if result[i]==0:
			return i






if __name__ == '__main__':

	print("\n\n\t\t_RATE MONOTONIC SCHEDULER_\n")

	#Read_data()
	#IDLE task

	# from paper
	#createTask(0, 10, 3, 1, 0)
	#createTask(1,100,15,1,0)
	#createTask(2, 200, 15, 1, 0)
	#createTask(3,400,40,1,0)
	#createTask(4, 1000, 30, 0, 1)
	#createTask(5, 1000, 200, 1, 0)

	f = open("tasks.json")
	taskset1 = json.load(f)
	observerTaskID = 2
	taskIdentifier = 2


	for i in range(len(taskset1)):
		phase = taskset1[str(i)]["Phase"]
		period = taskset1[str(i)]["Period"]
		priority = taskset1[str(i)]["Priority"]
		WCET = taskset1[str(i)]["WCET"]
		secure = taskset1[str(i)]["Secure"]
		observer = taskset1[str(i)]["Observer"]
		createTask(i, phase, period, priority, WCET, secure, observer)



	#createTask(0, 2 ,11, 2, 1, 1, 0)
	#createTask(1,0, 15, 1, 3, 1, 0)
	#createTask(2, 0, 16, 0, 1, 0, 1)
	createIDLE()
	print(tasks)
	#print("hi tasks before",tasks_copy)
	#jsonTask(tasks)

	#sched_res = Schedulablity()
	#if sched_res == True:
	hp = Hyperperiod()
		#for i in range(len(tasks)):
		#	if (tasks[i]["Phase"]!=0):
		#		del tasks[i]
		#print("hi tasks after", tasks)
	Simulation(hp)
	drawGantt()
	ladder = generateExecInter(hp,ExecTemp)
	del tasks[observerTaskID]
	for i in range(len(tasks)):
		HighestPrio = prio(tasks)
		id = HighestPrio[0]
		victimPeriod = tasks[id]["Period"]
		arrival = timewindow(victimPeriod,ladder)
		print("Victim task ID:",HighestPrio[0])
		print("Arrival time: ",arrival)
		print("===================================")
		for i in range(arrival,len(ladder),victimPeriod):
			for j in range(tasks[id]["WCET"]):
				ladder[i+j]=taskIdentifier
		taskIdentifier+=1
		print(ladder)
		del tasks[id]




	#else:
		#Read_data()
		#sched_res = Schedulablity()
