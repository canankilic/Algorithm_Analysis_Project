# Question 2: Greedy Algorithm
# Esmanur Yorulmaz - 210201008
# Canan Kılıç - 220201037

import csv # to read .csv files
from datetime import datetime  # to understand the conferences time


def read_csv_files(dataset): # read .csv files function
    conferance_sessions = []  # we have 3 different dataset, stores all the sessions
    with open(dataset, 'r') as file:
        read_file = csv.DictReader(file)
        for row in read_file: # the start and end time is 3th and 4th column, it parses them and convert into Hour/Minute format
            start_time = datetime.strptime(row['start_time'].strip(), '%H:%M')
            end_time = datetime.strptime(row['end_time'].strip(), '%H:%M')

            conferance_sessions.append({ # append all session properties
                'name': row['name'],
                'subjects': row['subjects'],
                'start': start_time,
                'end': end_time
            })
    return conferance_sessions


def greedy_alg_schedule_session(conferance_sessions): # greedy algorithm function to schedule sessions
    conferance_sessions.sort(key=lambda x: x['end']) # sort sessions by their end_time to decide which sessions is proper for next
    suitable_sessions = []  # list for suitable and selected sessions
    last_end_time = datetime.min  # to decide which session will be next based on the last sessions end time


    for session in conferance_sessions:  # select non-overlapping sessions
        if session['start'] >= last_end_time:
            suitable_sessions.append(session)  #add session to the list
            last_end_time = session['end']

    return suitable_sessions


if __name__ == "__main__":
    # three different datasets
    arranged_data = read_csv_files('schedule_data.csv')
    arranged_data_2 = read_csv_files('schedule_data2.csv')
    arranged_data_3 = read_csv_files('schedule_data3.csv')

    # apply the greedy algorithm to find the maximum number of sessions for each dataset
    greedy_max_session = greedy_alg_schedule_session(arranged_data)
    greedy_max_sessions2 = greedy_alg_schedule_session(arranged_data_2)
    greedy_max_sessions3 = greedy_alg_schedule_session(arranged_data_3)

    print("Selected sessions maximizing the number of events:\nFirst dataset:")
    for session in greedy_max_session:
        print(
            f"{session['name']} \tSubject: {session['subjects']} \tStart: {session['start'].strftime('%H:%M')} - End: {session['end'].strftime('%H:%M')}")

    print("\n\nSecond dataset:")
    for session in greedy_max_sessions2:
        print(
            f"{session['name']} \tSubject: {session['subjects']} \tStart: {session['start'].strftime('%H:%M')} - End: {session['end'].strftime('%H:%M')}")

    print("\n\nThird dataset:")
    for session in greedy_max_sessions3:
        print(
            f"{session['name']} \tSubject: {session['subjects']} \tStart: {session['start'].strftime('%H:%M')} - End: {session['end'].strftime('%H:%M')}")
