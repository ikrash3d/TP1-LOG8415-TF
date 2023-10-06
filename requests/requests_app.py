from os import environ
from threading import Thread
from time import sleep
from requests_futures.sessions import FuturesSession


def request_cluster_1(url, content_type):
    print("Cluster 1: Sending 1000 requests to: " + url)
    session = FuturesSession()
    futures = []
    
    for i in range(1000):
      future = session.get(url,headers=content_type)
      futures.append(future)
    
    print_futures(futures=futures)

def request_cluster_2(url, content_type):
    session = FuturesSession()
    futures = []
    
    print("Cluster 2: Sending 500 requests to: " + url)
    for _ in range(500):
      future = session.get(url,headers=content_type)
      futures.append(future)
      
    print_futures(futures=futures)
      
    print("Sleeping for 60 sec...\n") 
    sleep(60)
    
    futures = []
    
    print("Sending 1000 requests to: " + url)
    for _ in range(1000):
      future = session.get(url, headers=content_type)
      futures.append(future)
     
    print_futures(futures)

def print_futures(futures):
    responses = [future.result() for future in futures]
    
    for i, response in enumerate(responses):
      print(f"Response for request {i}: {response}")     

if __name__ == "__main__":
  print("Waiting 60 seconds for the instances to be created...\n")
  
  # sleep(60)
  
  load_balancer_url = "http://load-balancer-737662605.us-east-1.elb.amazonaws.com"
  headers = {"content-type": "application/json"}
  
  cluster_1 = Thread(target=request_cluster_1, args=(load_balancer_url + "/cluster1", headers))
  cluster_2 = Thread(target=request_cluster_2, args=(load_balancer_url + "/cluster2", headers))
  
  cluster_1.start()
  print("Cluster 1 started\n")
  
  cluster_2.start()  
  print ("Cluser 2 started\n")
  
  cluster_1.join()
  print("Cluster 1 joined\n")
   
  cluster_2.join()
  print("Cluster 2 joined\n")
  
  print("Done!\n")
      
      

      
