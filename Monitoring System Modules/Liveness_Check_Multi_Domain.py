import requests
import json
import concurrent.futures
from queue import Queue
import time

#start time
start_time = time.time()

urls_queue = Queue()
analyzed_urls_queue = Queue()

with open('urls.txt', 'r') as infile: #load urls into queue
    for line in infile:
        urls_queue.put(line.strip())

print(f'Total URLs to check:{urls_queue.qsize()}')

def check_url():
    while not urls_queue.empty():
        url = urls_queue.get()
        result = {'url': url, 'status_code': 'Down'}
        try:
            response = requests.get(f'http://{url}', timeout=1)
            if response.status_code == 200:
                result['status_code'] = 'Alive'
        except requests.exceptions.RequestException:
            result['status_code'] = 'Down'
        finally:
            analyzed_urls_queue.put(result) # add result to analyzed queue
            urls_queue.task_done()

#generate report after all URLs are analyzed
def generate_report():
    result = []
    urls_queue.join() # wait for all url checks to finish

    #collect result from analyzed queue
    while not analyzed_urls_queue.empty():
        result.append(analyzed_urls_queue.get())
        analyzed_urls_queue.task_done()

    #write result to json file
    with open('report.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)
    print('Report generated in report.json')

#Run url check in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as liveness_threads_pool:
    #submit url check tasks
    futures = [liveness_threads_pool.submit(check_url) for _ in range(20)]
    #generate report after task complete
    liveness_threads_pool.submit(generate_report)

urls_queue.join() #ensure all urls are processed

#measure end time
end_time = time.time()
elpased_time = end_time - start_time

print(f'URL liveness check complete in {elpased_time:.2f} seconds.')
