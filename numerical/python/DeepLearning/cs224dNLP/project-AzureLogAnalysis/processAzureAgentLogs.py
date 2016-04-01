import re
#If no data is given, it should read this. Otherwise, read it from the path provided.

def parseLogs():
	f = open("data\\all_logs_ascii.txt")
	f2 = open("data\\agentlogs_tmp.txt", "w") #Temporarily write to disk so we don't ever have to run out of memory.

	log_set = {}

	for i in f:
		parsedStr = i.split(']')
		if len(parsedStr) > 1:
			msg = parsedStr[1]
			msg = msg.strip().lower()
			#Remmove IP addresses.
			msg = re.sub(r"\d{1,3}(?:\.\d{1,3}){3}", '__IP__', msg)
			#Remove HEX strings.
			msg = re.sub(r'0x[0-9a-fA-F]+', '__HEX__', msg)
			#Remove Ids.
			msg = re.sub(r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}', '__GUID__', msg)
			#Remove Ids.
			msg = re.sub(r'[0-9]{6}-[0-9]{4}.[0-9]{4}.[0-9]{4}', '__GUID__', msg)

			msg = re.sub(r'[a-fA-F0-9]{32}.secondaryreceiverworker_in_[0-9]{3}', '__ID1__', msg)
			
			msg = re.sub(r'[a-fA-F0-9]{32}.[a-fA-F0-9]{4}.[a-fA-F0-9]{32}.[a-fA-F0-9]{4}.secondaryreceiverworker_in_[0-9]{3}.[0-9]{1}.xml', '__ID2__', msg)

			msg = re.sub(r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{8}-[a-fA-F0-9]{12}-[a-fA-F0-9]{25}', '__ID3__', msg)

			msg = re.sub(r'[a-fA-F0-9]{32}.vhd', '__VHD__' , msg)

			msg_list = msg.split()
			for indx in xrange(len(msg_list)):
				if "incarnation=" in msg_list[indx]:
					msg_list[indx] = "Incarnation="
				if "entityid=" in msg_list[indx]:
					msg_list[indx] = "EntityId="
				if "context=" in msg_list[indx]:
					msg_list[indx] = "Context="
				if "context:" in msg_list[indx]:
					msg_list[indx] = "Context="
				if "imagename=" in msg_list[indx]:
					msg_list[indx] = "ImageName="

			msg = '--'.join(msg_list)
			f2.write(msg)
			f2.write('\n')
			if msg in log_set:
				log_set[msg] = log_set[msg] + 1
			else:
				log_set[msg] = 1

	f.close()
	f2.close()

	#What keys should we remove?
	keys_to_remove = {}
	for k in sorted(log_set, key = log_set.get, reverse=True):
		#print (k, log_set[k])
		if log_set[k] < 6:
			keys_to_remove[k] = 1


	f = open("data\\agentlogs_tmp.txt")
	f2 = open("data\\agentlogs_final.txt","w")

	for i in f:
		if i.strip() not in keys_to_remove:
			f2.write(i)
		else:
			f2.write("UNKK\n")

	f.close()
	f2.close()


if __name__ == "__main__":
	parseLogs()


