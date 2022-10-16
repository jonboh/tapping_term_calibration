import math
from collections import defaultdict

import keyboard


def index_check(gen, check):
    for i, elem in enumerate(gen):
        if check(elem):
            return i
    return -1


def print_text():
    print('something about this is great\n')


def mean(values):
    return sum(values)/len(values)


def std(values):
    mean_ = mean(values)
    return math.sqrt(sum([(val - mean_)**2 for val in values])/(len(values)-1))


if __name__ == '__main__':
    modtapkeys = ('a', 'o', 'e', 'u', 'h', 't', 'n', 's')
    pinkies = (modtapkeys[0], modtapkeys[-1])
    rings = (modtapkeys[1], modtapkeys[-2])
    middels = (modtapkeys[2], modtapkeys[-3])
    indexes = (modtapkeys[3], modtapkeys[-4])
    recorded = keyboard.record(until='esc')
    events = list(recorded)
    modtap_time = defaultdict(lambda: list())
    for i, event in enumerate(events):
        if event.event_type == keyboard.KEY_DOWN and event.name in modtapkeys:
            offset = index_check(events[i:],
                                 lambda ev: ev.name == event.name and ev.event_type == keyboard.KEY_UP)
            if offset == -1:
                break  # last keys were not released
            event_up = events[i+offset]
            modtap_time[event.name].append(
                (event_up.time - event.time)*1000)
    for key in modtapkeys:
        times = modtap_time[key]
        if len(times) > 1:
            print(f'{key}: {mean(times)} +- {3*std(times)} | Max: {max(times)}')
    for name, keys in zip(['pinkies', 'rings', 'middels', 'indexes'],
                          [pinkies, rings, middels, indexes]):
        times = modtap_time[keys[0]]+modtap_time[keys[1]]
        if len(times) > 1:
            print(f'{name}: {mean(times)} +- {3*std(times)} | Max: {max(times)}')
