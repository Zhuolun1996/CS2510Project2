#README

##Description
This project would simulate message transmission in P2PNetwork

##Manual
###Arguments:  
-C, --clients, Number of clients, e.g. 10  
-B, --backups, Number of backups, e.g. 3  
-S, --nodes, Number of storage nodes, e.g. 3  
-M, --files, Number of Files, e.g. 10    
-N, --requests, Number of Requests, e.g. 10  
-F, --frequency, Request Frequency, e.g. 10 --> wait 0.1 second between two requests  
-L, --length, File Length, e.g. 1   
-O, --output, Output mode, `clean` || `debug` || `false`  

###Example
`python3 main.py -C 3 -B 3 -S 5 -M 10 -N 20 -F 1000 -L 1 -O clean`   
output:
```
Server 10000 loop running in thread: Thread-1
Server 10001 loop running in thread: Thread-2
Server 10002 loop running in thread: Thread-6
Server 10003 loop running in thread: Thread-11
Server 100 loop running in thread: Thread-17
Server 101 loop running in thread: Thread-25
Server 102 loop running in thread: Thread-33
Server 103 loop running in thread: Thread-41
Server 104 loop running in thread: Thread-49
clean directory success
clean directory success
clean directory success
Server10000 shutdown
Server ('127.0.0.1', 50100) timeout
Request Fault Tolerance Schema
Server 10000 loop running in thread: Thread-164
=== Get File List From Directory Server ===
File List: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
=== Get File List From Node ===
File List: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 3
Content: Test File3
=== Read File ===
File Name: 4
Content: Test File4
=== Read File ===
File Name: 5
Content: Test File5
=== Read File ===
File Name: 6
Content: Test File6
=== Read File ===
File Name: 7
Content: Test File7
=== Read File ===
File Name: 8
Content: Test File8
=== Read File ===
File Name: 9
Content: Test File9
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 3
Content: Test File3
=== Read File ===
File Name: 4
Content: Test File4
=== Read File ===
File Name: 5
Content: Test File5
=== Read File ===
File Name: 6
Content: Test File6
=== Read File ===
File Name: 7
Content: Test File7
=== Read File ===
File Name: 8
Content: Test File8
=== Read File ===
File Name: 9
Content: Test File9
Server100 shutdown
Server101 shutdown
Server102 shutdown
Server103 shutdown
Server ('127.0.0.1', 50202) timeout
Request Fault Tolerance Schema
Server ('127.0.0.1', 50203) timeout
Request Fault Tolerance Schema
Server ('127.0.0.1', 50201) timeout
Request Fault Tolerance Schema
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 3
Content: Test File3
=== Read File ===
File Name: 4
Content: Test File4
=== Read File ===
File Name: 5
Content: Test File5
=== Read File ===
File Name: 6
Content: Test File6
=== Read File ===
File Name: 7
Content: Test File7
=== Read File ===
File Name: 8
Content: Test File8
=== Read File ===
File Name: 9
Content: Test File9
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 3
Content: Test File3
=== Read File ===
File Name: 4
Content: Test File4
=== Read File ===
File Name: 5
Content: Test File5
=== Read File ===
File Name: 6
Content: Test File6
=== Read File ===
File Name: 7
Content: Test File7
=== Read File ===
File Name: 8
Content: Test File8
=== Read File ===
File Name: 9
Content: Test File9
Server 100 loop running in thread: Thread-246
Server 101 loop running in thread: Thread-255
Server 102 loop running in thread: Thread-264
Server 103 loop running in thread: Thread-273
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 3
Content: Test File3
=== Read File ===
File Name: 4
Content: Test File4
=== Read File ===
File Name: 5
Content: Test File5
=== Read File ===
File Name: 6
Content: Test File6
=== Read File ===
File Name: 7
Content: Test File7
=== Read File ===
File Name: 8
Content: Test File8
=== Read File ===
File Name: 9
Content: Test File9
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 3
Content: Test File3
=== Read File ===
File Name: 4
Content: Test File4
=== Read File ===
File Name: 5
Content: Test File5
=== Read File ===
File Name: 6
Content: Test File6
=== Read File ===
File Name: 7
Content: Test File7
=== Read File ===
File Name: 8
Content: Test File8
=== Read File ===
File Name: 9
Content: Test File9
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 0
Content: Test File0
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 1
Content: Test File1
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
=== Read File ===
File Name: 2
Content: Test File2
Server10000 shutdown
======= Statistic Data: Server 50100 ======
Message Send: 52
Message Recv: 52
Bytes Send: 12241
Bytes Recv: 3113
Average Response Time: 1.68463134765625
======= Statistic Data: Server 50101 ======
Message Send: 136
Message Recv: 136
Bytes Send: 18168
Bytes Recv: 15432
Average Response Time: 1.3728999641273432
Server10001 shutdown
======= Statistic Data: Server 50102 ======
Message Send: 26
Message Recv: 26
Bytes Send: 1355
Bytes Recv: 7822
Average Response Time: 0.2669208233173077
Server10002 shutdown
======= Statistic Data: Server 50103 ======
Message Send: 25
Message Recv: 25
Bytes Send: 1305
Bytes Recv: 7708
Average Response Time: 0.3332568359375
Server10003 shutdown
======= Statistic Data: Server 50200 ======
Message Send: 7
Message Recv: 7
Bytes Send: 729
Bytes Recv: 397
Average Response Time: 1.1792035784040178
Server100 shutdown
======= Statistic Data: Server 50201 ======
Message Send: 3
Message Recv: 3
Bytes Send: 161
Bytes Recv: 285
Average Response Time: 5.990478515625
Server101 shutdown
======= Statistic Data: Server 50202 ======
Message Send: 3
Message Recv: 3
Bytes Send: 161
Bytes Recv: 285
Average Response Time: 2.2123209635416665
Server102 shutdown
======= Statistic Data: Server 50203 ======
Message Send: 3
Message Recv: 3
Bytes Send: 161
Bytes Recv: 285
Average Response Time: 3.3863932291666665
Server103 shutdown
======= Statistic Data: Server 50204 ======
Message Send: 113
Message Recv: 113
Bytes Send: 6331
Bytes Recv: 5545
Average Response Time: 0.735962994330752
Server104 shutdown
======= Statistic Data: Server 50000 ======
Message Send: 150
Message Recv: 150
Bytes Send: 7955
Bytes Recv: 8023
Average Response Time: 2.473640950520833
======= Statistic Data: Server 50001 ======
Message Send: 2
Message Recv: 2
Bytes Send: 68
Bytes Recv: 184
Average Response Time: 0.7869873046875
======= Statistic Data: Server 50002 ======
Message Send: 2
Message Recv: 2
Bytes Send: 68
Bytes Recv: 184
Average Response Time: 0.8756103515625
```