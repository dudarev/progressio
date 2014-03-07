"""
Displays number of tasks open and closed in each day.
"""

import os
os.chdir('..')

import dateutil.parser

import matplotlib.pyplot as plt
from matplotlib.dates import (
    DateFormatter, WeekdayLocator, MONDAY)

from progressio.progressio import load_items


# load data

counts_done_at = {}
counts_added_at = {}

for i in load_items(is_done=True):
    if i.added_at:
        d = dateutil.parser.parse(i.added_at).date()
        counts_added_at[d] = counts_added_at.get(d, 0) + 1
    if i.done_at:
        d = dateutil.parser.parse(i.done_at).date()
        counts_done_at[d] = counts_done_at.get(d, 0) + 1


# plot data

def get_x_y(counts):
    """
    Returns x, y tuple (two lists).
    """
    return zip(*[(d, counts[d]) for d in counts])


ax = plt.subplot(111)

x, y = get_x_y(counts_added_at)
ax.bar(x, y, width=1)

x, y = get_x_y(counts_done_at)
ax.bar(x, [-i for i in y], width=1, color='r')

ax.plot([min(x), max(x)], [0, 0], 'k')


# axis are not shown since axis off below but
# formatting is used to show x-coordinate of the mouse pointer
loc = WeekdayLocator(byweekday=MONDAY, interval=2)
ax.xaxis.set_major_locator(loc)
ax.xaxis.set_major_formatter(DateFormatter('%b %d'))

ax.axis('off')

plt.show()
