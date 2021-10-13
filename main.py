import os
import signal
import sys
import time
from functools import partial

FILE_TO_PROCESS = 'process_this.txt'
FILE_TO_CONTINUE_FROM = 'continue_from_here.txt'  # should not exist initially

def load_file(FILE):
    """helper function to load file containing state"""
    with open(FILE, 'r') as f:
        state = f.readlines()
        state = set(map(str.strip, state))
    return state

def load_state():
    """function to decide whether to continue from saved_state"""
    if os.path.exists(FILE_TO_CONTINUE_FROM):
        # if saved state exist, continue from saved state
        return load_file(FILE_TO_CONTINUE_FROM)

    return load_file(FILE_TO_PROCESS)

def dump_state(state, target=FILE_TO_CONTINUE_FROM):
    with open(target, 'w') as f:
        f.writelines('\n'.join(state))

def save_state_on_interrupt(STATE, signalNumber, frame):
    """signal handler. saving state when interrupt received"""
    print('\nInterrupt Received\nSaving state...')

    # get unprocessed state
    unprocessed_state = STATE[0] - STATE[1]

    # dump state
    dump_state(unprocessed_state)
    sys.exit(1)

def save_state_on_time_passing(f, STATE):
    """save state by periodically checking time elapsed"""
    seconds = 0
    last_invoked = time.time()

    def timer_wrapper(*args, **kwargs):
        nonlocal last_invoked
        nonlocal seconds
        elapsed_time = time.time() - last_invoked

        if elapsed_time > 5:
            last_invoked = time.time()
            seconds += 5

            print(f'\n{seconds} seconds have passed\nSaving state...')
            unprocessed_state = STATE[0] - STATE[1]
            dump_state(unprocessed_state)

        return f(*args, **kwargs)
    return timer_wrapper

def save_state_on_n_processed_state(f, STATE):
    """save state by periodically checking count of processed state"""
    count = 5

    def counter_wrapper(*args, **kwargs):
        unprocessed_state = STATE[0] - STATE[1]

        if len(STATE[1]) != 0 and len(unprocessed_state) % count == 0:  # isn't just starting & have processed n states
            print(f'\n{count} state have been processed\nSaving state...')
            dump_state(unprocessed_state)

        return f(*args, **kwargs)
    return counter_wrapper

# @save_state_on_time_passing
def process_state(processed_state, state):
    print(f'processing state: {state}')
    processed_state.add(state)
    time.sleep(1)

def save_state_handler(f, save_state_by_function, STATE):
    """take a processing function to run & a state to keep track of"""
    f = save_state_by_function(f, STATE)  # decorate running function
    return f

if __name__ == '__main__':
    # reference
    # signal: https://stackabuse.com/handling-unix-signals-in-python/
    # partial: https://stackoverflow.com/a/31709094/8996974

    some_state = load_state()
    processed_state = set()

    STATE = (some_state, processed_state)  # tuple for easier lookups
    signal.signal(signal.SIGINT, partial(save_state_on_interrupt, STATE))

    # output current process id
    print('My PID is:', os.getpid())
    
    # add save state by time passing to process_state
    # process_state = save_state_handler(process_state, save_state_on_time_passing, STATE)
    process_state = save_state_handler(process_state, save_state_on_n_processed_state, STATE)

    # simulate processing some state
    for state in some_state:
        process_state(processed_state, state)
