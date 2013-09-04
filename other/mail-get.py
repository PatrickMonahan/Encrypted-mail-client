import imaplib,email,os,getpass
imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
imap.login('padmon29@gmail.com','ihee7Jau')
imap.select('INBOX')



def getAttachment(msg):
	print 'in getAttachment'	
	for part in msg.walk():
		#if(part.get_content_type() == 'multipart/mixed'):
		#	name1 = part.get_filename()			
		#	f1 = open(name1,"w")
		#	f1.write(part.get_payload)			
	


		if part.get_content_type() == 'application/octet-stream': #or part.get_content_type() == 'text/plain':
			name = part.get_filename()	
			f = open("temp/"+name,"w")
			f.write(part.get_payload())		 
					

typ, data = imap.search(None,'SUBJECT',"encrypted mail!!!")
for num in data[0].split():
	typ, data = imap.fetch(num,'(RFC822)')
	msg = email.message_from_string(data[0][1])
	getAttachment(msg)
	print 'Done!'


