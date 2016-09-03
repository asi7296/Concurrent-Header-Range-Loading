#!/usr/bin/env python
import httplib, sys, argparse, threading

# instatntiate argparse
arg_parser = argparse.ArgumentParser()

# Global var declaration, holds the command line args
url = None
num_req = None
bytes_per_range_header = None
output_file = None

'''
# validation and assigning of the arguments to global vars
if len(sys.argv) != 9: 
	sys.exit('Invalid # of arguments passed, please view README.txt to view usage details')
# get args, irrespective of order
else:
	for arg in range(len(sys.argv)):
		if sys.argv[arg] == '-w' :
			url = sys.argv[arg+1]
		if sys.argv[arg] == '-n' :
			num_req = sys.argv[arg+1]
		if sys.argv[arg] == '-r' :
			bytes_per_range_header = sys.argv[arg+1]
		if sys.argv[arg] == '-O' :
			output_file = sys.argv[arg+1]
# validate types of each arg
if not (type(url) == 'str' and type(num_req) == 'int' and type(bytes_per_range_header) == 'int' and type(output_file) == 'str'):
	sys.exit('Invalid types for aguments, please view README.txt for usage details')
'''
# validation of the args
arg_parser.add_argument('-w', required=True, dest='URL', type=str)
arg_parser.add_argument('-n', required=True, dest='NumConcurrentRequests', type=int)
arg_parser.add_argument('-r', required=True, dest='BytesPerRangeHeader', type=int)
arg_parser.add_argument('-O', required=True, dest='OutputFileName', type=str)
#assigning of the arguments to global vars
args = arg_parser.parse_args()
url = args.URL
num_req = args.NumConcurrentRequests
bytes_per_range_header =  args.BytesPerRangeHeader
output_file =  args.OutputFileName

# make sure client is setting a .html
if not '.html' in output_file:
	sys.exit('Please create a valid output file. View README.txt for proper usage details')

#storing the first half of the url in server_name
if '/' in url : 
	server_name = url[ : url.index('/')]
else:
	server_name = url
print server_name
# storing the requested page on the server - localhost/pageName
file_present = '/' in url
if(not file_present):
	file_req = '/'
else:
	file_req = url[ url.index('/'): ]
print file_req

########################
# add to readme - if 'localhost' is visited, apache2 webserver
# welcome message will be used
########################


# Getting the size of the page through the header
connection = httplib.HTTPConnection(server_name)
connection.request('HEAD', file_req)
response = connection.getresponse()
headers = response.getheaders()
content_length = headers[0][1] #first element of response obj, 2nd element of the the tuple ie 1st element

# stored the html content returned from the requests
page_content = [None] * num_req

# Thread class
class threaded_connection(threading.Thread):
	def __init__(self, threadIndex, start_byterange, end_byterange):
		threading.Thread.__init__(self)
		self.start_byterange = start_byterange
		self.end_byterange = end_byterange
		self.threadIndex = threadIndex
	def run(self):
		connection = httplib.HTTPConnection(server_name)
		connection.request('GET', file_req, headers={'Range' : 'bytes=' + str(start_byterange) + '-' +  str(end_byterange)})
		response = connection.getresponse()
		# put reponse.read() content into list at index i
		page_content[self.threadIndex] = response.read()
		connection.close()	

# variables used to define headers, start and end byte ranges
start_byterange = 0
end_byterange = bytes_per_range_header - 1

#  list of threads
threads = []

# If user enters huge values, where the server will give 'unsatisfiable' range error, get the entire page through one connection
if (num_req * bytes_per_range_header) >= int(content_length):
	connection = httplib.HTTPConnection(server_name)
	connection.request('GET', file_req)
	response = connection.getresponse()
	page_content = (response.read())
	connection.close()
else:
	# loop over number of requests client wants
	for connection in range (0, num_req):
		#create a thread for each client	
		#print str(start_byterange) + ' . ' + str(end_byterange)
		new_conn = threaded_connection(connection, start_byterange, end_byterange)
		new_conn.start()
		new_conn.run()
		threads.append(new_conn)

		start_byterange += bytes_per_range_header
		end_byterange += bytes_per_range_header 

# wait for all treads to complete
for thread in threads:
	thread.join()

# format page_content into string, then write to file
op_file_data = ''.join(page_content)

# write output to the file
file_obj = open(output_file, 'w')
file_obj.write(str(op_file_data))
file_obj.close()

sys.exit(output_file + ' has been written to the same directory as this program')