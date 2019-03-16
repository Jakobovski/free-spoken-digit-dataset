from __future__ import print_function
import time
import math

"""
Prompts you to say numbers.

Start this, and then hit "Record" in Audacity.
http://www.audacityteam.org/download/
When you start Audacity, look in the bottom-left and set the Project Rate (Hz) to 8000.

It takes about 30 minutes to record a full dataset.

Tips:
- Turn off your screen saver before you start!
- Try a short recording session first to make sure everything works OK before doing the full recording.


When done, export the audio as one big .wav file and use 'split_and_label_numbers.py'
to make the labeled dataset.
"""

DELAY_BETWEEN_NUMBERS = 3
REPEATS_PER_NUMBER = 3


def wait_until(t):
    while time.time() < t:
        time.sleep(0.01)


def generate_number_sequence():
    # We want the numbers jumbled up (helps eliminate any previous-number effects)
    # This function scrambles the numbers in a deterministic way so that we can remember
    # what the order was later.
    # A deterministic shuffle makes labeling easy, makes pausing / resuming the experiment easy, etc.
    nums = [str(i) for i in range(10) for set_num in range(REPEATS_PER_NUMBER)]
    for i in range(len(nums)):
        target = int(round(math.pi * i)) % len(nums)
        (nums[i], nums[target]) = (nums[target], nums[i])
    return nums


def show_numbers():
    nums = generate_number_sequence()

    print("Get ready...")
    time.sleep(1)

    t_start = time.time()
    for i, num in enumerate(nums):
        if (float(i)/len(nums) * 100) % 10 == 0:
            print("\n====", float(i)/len(nums)*100, "% done====\n")
        else:
            print("")

        t_next_display = t_start + (i + 1) * DELAY_BETWEEN_NUMBERS
        t_next_blank = t_next_display + 2.5

        # display a number
        wait_until(t_next_display)
        print(num)

        # blank
        wait_until(t_next_blank)

if __name__ == '__main__':
    show_numbers()
