from multiprocessing import Process, Pipe
from time import sleep


# Take the maximum out of recv counter and internal counter element-wise
def get_recv_counter(recv_counter, counter):
    for i in range(len(counter)):
        counter[i] = max(recv_counter[i], counter[i])
    return counter


# Simulate the event in the process - increase internal counter
def event(process_id, counter):
    counter[process_id] += 1
    print(f'Something happened in {process_id}. Local counter {counter}')
    return counter


# Simulate sending a message - increase internal counter and send it with a pipe
def send_message(pipe, process_id, counter):
    counter[process_id] += 1
    pipe.send(counter)
    print(f'Message sent from {process_id}. Local counter {counter}')
    return counter


# Simulate receiving a message - increase internal counter and then update it according to receiver's counter
def recv_message(pipe, process_id, counter):
    counter[process_id] += 1
    timestamp = pipe.recv()
    counter = get_recv_counter(timestamp, counter)
    print(f'Message received at {process_id}. Local counter {counter}')
    return counter


# Processes functions - receive pipes
# Sets parameters (process number, internal counter)
def process_one(pipe12):
    process_id = 0
    counter = [0, 0, 0]

    counter = send_message(pipe12, process_id, counter)
    counter = send_message(pipe12, process_id, counter)
    counter = event(process_id, counter)
    counter = recv_message(pipe12, process_id, counter)
    counter = event(process_id, counter)
    counter = event(process_id, counter)
    counter = recv_message(pipe12, process_id, counter)
    # Sleep until all processes are done
    sleep(1)
    print(f"Final counter for {process_id} is {counter}")


def process_two(pipe21, pipe23):
    process_id = 1
    counter = [0, 0, 0]

    counter = recv_message(pipe21, process_id, counter)
    counter = recv_message(pipe21, process_id, counter)
    counter = send_message(pipe21, process_id, counter)
    counter = recv_message(pipe23, process_id, counter)
    counter = event(process_id, counter)
    counter = send_message(pipe21, process_id, counter)
    counter = send_message(pipe23, process_id, counter)
    counter = send_message(pipe23, process_id, counter)
    # Sleep until all processes are done
    sleep(1)
    print(f"Final counter for {process_id} is {counter}")


def process_three(pipe32):
    process_id = 2
    counter = [0, 0, 0]

    counter = send_message(pipe32, process_id, counter)
    counter = recv_message(pipe32, process_id, counter)
    counter = event(process_id, counter)
    counter = recv_message(pip32, process_id, counter)
    # Sleep until all processes are done
    sleep(1)
    print(f"Final counter for {process_id} is {counter}")


if __name__ == '__main__':
    # Create pipes for process communications
    pipe12, pipe21 = Pipe()
    pip23, pip32 = Pipe()

    # Create processes
    process1 = Process(target=process_one, args=(pipe12,))
    process2 = Process(target=process_two, args=(pipe21, pip23))
    process3 = Process(target=process_three, args=(pip32,))

    # Start the processes and wait until they are finished
    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
