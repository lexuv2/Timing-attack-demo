import requests as re
from time import perf_counter_ns
from multiprocessing import Pool
import time
from matplotlib import pyplot as plt


url = 'http://localhost:5000/auth'
batch_size = 5000
threads = 16
garbage_collector = 0

def test_for_combination(login , password):
    sum = 0
    elements = 0
    times = []
    
    for x in range(batch_size):
        r = re.post(url, json={'username': login, 'password': password})
        time_taken = r.elapsed.microseconds
        if garbage_collector:
            if (elements > 10 and time_taken > (sum/elements)*4):
                #print(f"ignore time {time_taken}ms")
                
                pass
            else:
                #print(f"time_sumed {time_taken}")
                elements+=1
                sum += time_taken
        else:
            elements+=1
            sum+=time_taken
            times.append(time_taken)
    
        
    return (sum / elements,times)

def test_for_combination_threaded(login , password):
    sum = 0
    with Pool(threads) as p:
        for x in range(batch_size):
            r = p.apply_async(re.post, args=(url,), kwds={'json': {'username': login, 'password': password}})
            time_taken = r.get().elapsed.microseconds
            sum += time_taken
    return sum*threads / batch_size


#print("good",test_for_combination_threaded('admin', 'ping2024'))
#print("good",test_for_combination('admin', 'ping2024'))
#print("bad",test_for_combination_threaded('gueuhre', 'ping2a24'))



(average , times) = test_for_combination('admin', 'ping2024')

