from typing import Dict
import random
import string
import time

FIX_TEMPLATE = '8=FIX.4.2|9=362|35=D|1={}|11={}|15={}|34={}|37=qdir900a570744044|38=100|39={}|40={}|43=N|44=28.47|47=A|54=1|55=NEP|59=5|60=20151216-20:55:19.136|100=ARCX|109=BECCAP|207=XNYS|376=ETB08|526=570744044|1040=qdir900a'
AMOUNT_OF_SAMPLES = 10000


# Generates random string by length
def random_string(length: int) -> str:
    return ''.join(random.choice(string.ascii_letters) for m in range(length))


# Create samples of FIX messages in order to not give same message to the benchmarks
def create_samples() -> list:
    result = []
    for i in range(AMOUNT_OF_SAMPLES):
        result.append(FIX_TEMPLATE.format(
            random_string(4),
            random_string(10),
            random_string(1),
            random_string(2),
            random_string(5),
            random_string(6)
        ))

    return result


# Elegant implementation of FIX parsing
def parse_fix_event(event: str) -> Dict[int, str]:
    result = dict()
    for item in event.split('|'):
        tag, _, value = item.partition('=')
        result[int(tag)] = value

    return result


# FIX parsing in 1 iteration - without split method
def parse_fix_event_faster(event: str) -> Dict[int, str]:
    result = dict()

    current_tag = []
    current_value = []
    is_reading_tag = True

    for i in event:
        if i == '|':
            result[int(''.join(current_tag))] = ''.join(current_value)
            current_tag.clear()
            current_value.clear()
            is_reading_tag = True
        elif i == '=':
            is_reading_tag = False
        else:
            if is_reading_tag:
                current_tag.append(i)
            else:
                current_value.append(i)

    return result


def benchmark_method(method_obj):
    samples = create_samples()

    print(f"Benchmarks for {str(method_obj)}:")
    start = time.process_time()

    for i in samples:
        method_obj(i)

    end = time.process_time()
    print(f'Took {(end-start)/AMOUNT_OF_SAMPLES} usec per message')

    print()


benchmark_method(parse_fix_event)
benchmark_method(parse_fix_event_faster)

