import os
from tabulate import tabulate
import string

# Initialize Jobs through User Inputs
jobs = {}
print("Enter job details (format: arrival_time burst_time priority), type 'confirm' when done")
job_input = input("Enter first job / type 'confirm' to finish: ")

# Sample data if no inputs are given
sample_jobs = {
    'A': [0, 3],
    'B': [5, 5],
    'C': [6, 1]
}

#Splits the input
letter_index = 0
while job_input.lower() != 'confirm':
    job_details = job_input.split()
    job_name = string.ascii_uppercase[letter_index]
    jobs[job_name] = [int(job_details[0]), int(job_details[1]), int(job_details[2])]
    letter_index += 1
    job_input = input("Enter next job or type 'confirm' to finish: ")

# If no jobs were added, insert sample data
if not jobs:
    jobs = sample_jobs

# Initializations
jobs_section = f'JOBS: {jobs}'
jobs_to_q = jobs.copy()
ongoing = []
queue = []
completed = {}
currTime = 0
nT = 0
prev_ongoing = []

# GANTT'S CHART Simulation Loop
while True:
    # Get the jobs to the queue
    for job, details in jobs_to_q.items():
        if details[0] == currTime:
            queue.append(job)
            
    #sort queue based on priority then burst then name of job
    queue = sorted(queue, key=lambda x: (jobs[x][2], jobs[x][1]))


    # Handle completion of jobs and saving tat and wT
    if nT == currTime and ongoing:
        job_name = ongoing[0]
        tat = nT - jobs[job_name][0]
        wT = tat - jobs[job_name][1]
        completed[job_name] = {'tat': tat, 'wT': wT}
        del jobs_to_q[job_name]
        ongoing = []

    # Send jobs from the queue to ongoing
    if not ongoing and queue:
        eligible_jobs = [job for job in queue if currTime >= jobs[job][0]]
        if eligible_jobs:
            job_to_add = eligible_jobs[0]
            ongoing.append(job_to_add)
            queue.remove(job_to_add)
    
    #sort the list in completed
    sortedCompletion = dict(sorted(completed.items()))

    # Update the ETA of the current job
    if ongoing and prev_ongoing != ongoing:
        nT = currTime + jobs[ongoing[0]][1]
        prev_ongoing = ongoing.copy()

    # Print logs
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Completed:")
    print(tabulate([["Job", "Arrival Time", "Burst Time", "Turnaround Time", "Waiting Time"]] + 
                [[job, jobs[job][0], jobs[job][1], details['tat'], details['wT']] for job, details in sortedCompletion.items()], 
                headers="firstrow", tablefmt="pretty"))
    print(f"ETA of current job: {nT if ongoing else '-'}")
    print("")
    
    # Increment currTime to increase time
    currTime += 1

    # Break if all jobs have been completed
    if not jobs_to_q and not ongoing and not queue:
        break