import filecmp
 
d1 = "logs/"
d2 = "logs-sample-permutation/"
files = ['h1-cwnd.txt', 'h1-recvd-packets.txt',
		 'h2-cwnd.txt', 'h2-recvd-packets.txt',
		 'h3-cwnd.txt', 'h3-recvd-packets.txt',
		 'h4-cwnd.txt', 'h4-recvd-packets.txt',
		 'h5-cwnd.txt', 'h5-recvd-packets.txt',
		 'h6-cwnd.txt', 'h6-recvd-packets.txt',
		 'h7-cwnd.txt', 'h7-recvd-packets.txt',
		 'h8-cwnd.txt', 'h8-recvd-packets.txt',
		 'h9-cwnd.txt', 'h9-recvd-packets.txt',
		 'h10-cwnd.txt', 'h10-recvd-packets.txt',
		 'h11-cwnd.txt', 'h11-recvd-packets.txt',
		 'h12-cwnd.txt', 'h12-recvd-packets.txt',
		 'h13-cwnd.txt', 'h13-recvd-packets.txt',
		 'h14-cwnd.txt', 'h14-recvd-packets.txt',
		 'h15-cwnd.txt', 'h15-recvd-packets.txt',
		 'h16-cwnd.txt', 'h16-recvd-packets.txt',
		 'h17-cwnd.txt', 'h17-recvd-packets.txt',
		 'h18-cwnd.txt', 'h18-recvd-packets.txt',
		 'h19-cwnd.txt', 'h19-recvd-packets.txt',
		 'h20-cwnd.txt', 'h20-recvd-packets.txt',
		 'h21-cwnd.txt', 'h21-recvd-packets.txt',
		 'h22-cwnd.txt', 'h22-recvd-packets.txt',
		 'h23-cwnd.txt', 'h23-recvd-packets.txt',
		 'h24-cwnd.txt', 'h24-recvd-packets.txt',
		 'h25-cwnd.txt', 'h25-recvd-packets.txt',
		 'h26-cwnd.txt', 'h26-recvd-packets.txt',
		 'h27-cwnd.txt', 'h27-recvd-packets.txt',
		 'h28-cwnd.txt', 'h28-recvd-packets.txt',
		 'h29-cwnd.txt', 'h29-recvd-packets.txt',
		 'h30-cwnd.txt', 'h30-recvd-packets.txt',
		 'h31-cwnd.txt', 'h31-recvd-packets.txt',
		 'h32-cwnd.txt', 'h32-recvd-packets.txt',
		 'h33-cwnd.txt', 'h33-recvd-packets.txt',
		 'h34-cwnd.txt', 'h34-recvd-packets.txt',
		 'h35-cwnd.txt', 'h35-recvd-packets.txt',
		 'h36-cwnd.txt', 'h36-recvd-packets.txt',
		 'h37-cwnd.txt', 'h37-recvd-packets.txt',
		 'h38-cwnd.txt', 'h38-recvd-packets.txt',
		 'h39-cwnd.txt', 'h39-recvd-packets.txt',
		 'h40-cwnd.txt', 'h40-recvd-packets.txt',
		 'h41-cwnd.txt', 'h41-recvd-packets.txt',
		 'h42-cwnd.txt', 'h42-recvd-packets.txt',
		 'h43-cwnd.txt', 'h43-recvd-packets.txt',
		 'h44-cwnd.txt', 'h44-recvd-packets.txt',
		 'h45-cwnd.txt', 'h45-recvd-packets.txt',
		 'h46-cwnd.txt', 'h46-recvd-packets.txt',
		 'h47-cwnd.txt', 'h47-recvd-packets.txt',
		 'h48-cwnd.txt', 'h48-recvd-packets.txt',
		 'h49-cwnd.txt', 'h49-recvd-packets.txt',
		 'h50-cwnd.txt', 'h50-recvd-packets.txt',
		 'h51-cwnd.txt', 'h51-recvd-packets.txt',
		 'h52-cwnd.txt', 'h52-recvd-packets.txt',
		 'h53-cwnd.txt', 'h53-recvd-packets.txt',
		 'h54-cwnd.txt', 'h54-recvd-packets.txt',
		 'recvd-flows.txt'
		]

# convert Windows \r\n to Unix \n
for filename in files:
	filepath = 'logs/'+filename
	with open(filepath) as f:  # default is 'rt' read text mode.
		data = f.read()

	with open(filepath, 'w', newline='\n') as f: # write with Unix new lines.
		f.write(data)
 
# deep comparison
match, mismatch, errors = filecmp.cmpfiles(d1, d2, files, shallow=False)
print("Match:", match)
print("Mismatch:", mismatch)
print("Errors:", errors)


