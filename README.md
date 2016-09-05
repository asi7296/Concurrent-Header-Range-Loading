# Concurrent-Header-Range-Loading

A script written to understand how content is received through a GET request to a webpage, through concurrent threads requesting data in ranges, specified in the headers.

<br><br>
<b>Execution</b><br>
./asn1.py -w <url> -n <number of concurrent requests> -r <bytes in one range header> -O <output-file>
<br><Br><i>Examples:</i>
./asn1.py -w localhost/page1.html -n 20 -r 2 -O Myopfile.html
./asn1.py -w www.google.com -n 1 -r 20 -O Myopfile.html<br>
<i>Type checking has been enabled, and the order of the parameters can be changed.</i>
<br>./asn1 -r 2 -O Myopfile.html -w localhost/page1.html -n 20
./asn1 -r 20 -O Myopfile.html -w www.coursera.org -n 200

*** Apart from general on-the-web URLs, a sample 'page1.html' file has also been created in the localhost'
For running the program with this file, please set the '-w' flag = localhost/page1.html


If (number of requests x bytes per header range) > (the size of the page), a single thread runs and recieves the entire page.
If (number of requests x bytes per header range) < (the size of the page), partial html will be recieved.


The output file has to be named with a .html extention and will be saved in the same directory as the asn1.py file.

<b>General description</b><br>
The arguments are validated and are assigned to variables.<br>
(number of requests x bytes per header range) is calculated.<br>
A HEAD request is sent to the URL to get the size of the webpage.<br>
If (number of requests x bytes per header range) is greater than the size of the webpage, a simple GET request is sent to the URL to recieve the content of the page.<br>
Else : an array of thread class objects are created ( = # of requests ), which are then assigned the range of bytes to fetch, and carry out the fetch from the URL.<br>
The byte range is then increased for the next thread. (eg. 20b -range, T1 : 0-19, T2 : 20-39 and so on)<br>
The script then waits for all the thread to finish their 'run' function.<br>
All the content is stored in a list, whose index is mapped to the thread created. (eg. T1 - index 0, T2 - index 1 ... )<br>
The list is finally converted to a string and is then written to the ouput file (which has already been validated to have a .html extension) to the same directory as the program.<br>
This output file can then be viewed in a browser.<br>
