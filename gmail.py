import getpass, os, imaplib, email
from OpenSSL.crypto import load_certificate, FILETYPE_PEM


def getAttachment(msg):
	print 'in getAttachment'	
	for part in msg.walk():
		if part.get_content_type() == 'application/octet-stream':
			open(part.getfilename,'w').write(part.get_payload)	 
			print 'writing to file!'			 
			 #if check(part.get_filename()):
			  #  return part.get_payload(decode=1)



def getMsg():
	subject = 'encrypted mail!!!'
	imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
	imap.login('padmon29@gmail.com','ihee7Jau')
	imap.select('Inbox')
	typ, data = imap.search(None,'(UNSEEN SUBJECT "%s")' % subject)
	for num in data[0].split():
		typ, data = imap.fetch(num,'(RFC822)')
		print 'msg'
		msg = email.message_from_string(data[0][1])
		getAttachment(msg)

getMsg()
#if __name__ == '__main__':
#  for msg in getMsg():
#    payload = getAttachment(msg,lambda x: x.endswith('.pem'))
#    if not payload:
#      continue#
#    try:
#      cert = load_certificate(FILETYPE_PEM,payload)
#    except:
#      cert = None
#    if cert:
#      cn = cert.get_subject().commonName
#      filename = "%s.pem" % cn
#      if not os.path.exists(filename):
#        open(filename,'w').write(payload)
#        print "Writing to %s" % filename
#      else:
#        print "%s already exists" % filename
