from os import environ
from threading import Thread
from time import sleep
from requests import get
from requests_futures.sessions import FuturesSession


def request_cluster_1(url, content_type):
    print("Cluster 1: Sending 1000 requests to: " + url)
    session = FuturesSession()
    
    for _ in range(1000):
      session.get(url,headers=content_type)


def request_cluster_2(url, content_type):
    print("Cluster 2: Sending 500 requests to: " + url)
    session = FuturesSession()
    
    for _ in range(500):
      session.get(url,headers=content_type)
      
    print("Sleeping for 60 sec...") 
    sleep(60)
    
    print("Sending 1000 requests to: " + url)
    for _ in range(1000):
      session.get(url, headers=content_type)
      

if __name__ == "__main__":
  print("Waiting 5 seconds for the instances to be created...")
  
  sleep(5)
  
  urlM4 = "http://ec2-34-230-68-122.compute-1.amazonaws.com"
  urlT2 = "http://ec2-34-224-168-183.compute-1.amazonaws.com"
  headers = {"content-type": "application/json"}
  
  cluster_1 = Thread(target=request_cluster_1, args=(urlM4 + "/cluster1", headers))
  cluster_2 = Thread(target=request_cluster_2, args=(urlT2 + "/cluster2", headers))
  
  cluster_1.start()
  print("Cluster 1 started")
  
  cluster_2.start()  
  print ("Cluser 2 started")
  
  cluster_1.join()
  print("Cluster 1 joined")
   
  cluster_2.join()
  print("Cluster 2 joined\n")
  
  print("Done!")
      
      

      
