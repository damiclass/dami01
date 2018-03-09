#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import os

counter=0
request_time=0
http_code_5xx=0
http_code_2xx=0
http_code_3xx=0
http_code_4xx=0

class file_read:
    def __init__(self, logname):
        self.logname = logname

    def file_readlines(self, line):


        if '"message" =>' in line:	  # 如果一行中有 message 再打印
	    global request_time
	    global counter
	    global http_code_5xx
	    global http_code_4xx
   	    
	    global http_code_3xx
	    global http_code_2xx

	    counter=counter+1

	    if ( counter % 20 == 0 ):     # 取模 每出10行 输出一次
	    	#print counter
                print ("sending http_counter to pushgateway",counter)
                os.environ['http_counter']=str(counter)    # python定义的变量 通过在Linux中临时设置一个环境变量 然后 bash 可以获取传参
                os.popen(" echo \"http_counter $http_counter\" ")
                os.popen(" echo \"http_counter $http_counter\" | curl --data-binary @- http://localhost:9091/metrics/job/pushgateway/instance/localhost:9091")

###############################################################################

            list=line.split()             # 按空格分割 之后 返回的是 list 列表
	    #print list[7] 		  # 需要哪个字段直接按list的方式取就可以了 比如第7就是 响应时间
	    num=list[7]	 
	    request_time=float(request_time)+float(num)
	    if ( counter % 10 == 0 ):     # 取模 每出10行 输出一次 request
	    	#print ('avg_http_time:',  round(request_time/10,3)   )   # round 做四舍五入 
    	        request_time=round(request_time/10,3)            # 每10次 计算一次平均 http_time, 然后清零	
		print ("sending request_time to pushgateway",request_time)
		os.environ['request_time']=str(request_time)    # python定义的变量 通过在Linux中临时设置一个环境变量 然后 bash 可以获取传参
 	    	os.popen(" echo \"http_request_time $request_time\" ")
	    	os.popen(" echo \"http_request_time $request_time\" | curl --data-binary @- http://localhost:9091/metrics/job/pushgateway/instance/localhost:9091")
    	        request_time=0            # 每10次 计算一次平均 http_time, 然后清零	

###############################################################################
	    code=list[11]
	    if ( int(code) <= 599 ) and ( int(code) >= 500 ):
		http_code_5xx=http_code_5xx+1 
		#print ('http_code_5xx:', http_code_5xx)
	    if ( int(code) <= 499 ) and ( int(code) >= 400 ):
		http_code_4xx=http_code_4xx+1
		#print ('http_code_4xx:', http_code_4xx)
	    if ( int(code) <= 399 ) and ( int(code) >= 300 ):
		http_code_3xx=http_code_3xx+1
		#print ('http_code_3xx:', http_code_3xx)
	    if ( int(code) <= 299 ) and ( int(code) >= 200 ):
		http_code_2xx=http_code_2xx+1
		#print ('http_code_2xx:', http_code_2xx)

	    if ( counter % 20 == 0 ):     # 取模 每出10行 输出一次 http_code
                print ("sending http_code_5xx to pushgateway",http_code_5xx)
                os.environ['http_code_5xx']=str(http_code_5xx)    # python定义的变量 通过在Linux中临时设置一个环境变量 然后 bash 可以获取传参
                os.popen(" echo \"http_code_5xx $http_code_5xx\" ")
                os.popen(" echo \"http_code_5xx $http_code_5xx\" | curl --data-binary @- http://localhost:9091/metrics/job/pushgateway/instance/localhost:9091")


                print ("sending http_code_4xx to pushgateway",http_code_4xx)
                os.environ['http_code_4xx']=str(http_code_4xx)    # python定义的变量 通过在Linux中临时设置一个环境变量 然后 bash 可以获取传参
                os.popen(" echo \"http_code_4xx $http_code_4xx\" ")
                os.popen(" echo \"http_code_4xx $http_code_4xx\" | curl --data-binary @- http://localhost:9091/metrics/job/pushgateway/instance/localhost:9091")


                print ("sending http_code_3xx to pushgateway",http_code_3xx)
                os.environ['http_code_3xx']=str(http_code_3xx)    # python定义的变量 通过在Linux中临时设置一个环境变量 然后 bash 可以获取传参
                os.popen(" echo \"http_code_3xx $http_code_3xx\" ")
                os.popen(" echo \"http_code_3xx $http_code_3xx\" | curl --data-binary @- http://localhost:9091/metrics/job/pushgateway/instance/localhost:9091")

                print ("sending http_code_2xx to pushgateway",http_code_2xx)
                os.environ['http_code_2xx']=str(http_code_2xx)    # python定义的变量 通过在Linux中临时设置一个环境变量 然后 bash 可以获取传参
                os.popen(" echo \"http_code_2xx $http_code_2xx\" ")
                os.popen(" echo \"http_code_2xx $http_code_2xx\" | curl --data-binary @- http://localhost:9091/metrics/job/pushgateway/instance/localhost:9091")


###############################################################################
    def file_readline(self):
        f = open(self.logname, 'r')
        f.seek(0, 2)

        while True:
            offset = f.tell()
            line = f.readline()
            if not line:
                f.seek(offset)
                time.sleep(3)
            else:
                self.file_readlines(line)
        f.close()

if __name__ == '__main__':
    a = file_read('./logstash.stdout')
    a.file_readline()
