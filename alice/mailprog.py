import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import imaplib,email,os,getpass


def sign_in():
	who = raw_input("Sign in as:")
	while who != "bob" and who != "alice":
		who = raw_input("Sorry that is not a valid user\nSign in as:")
	receiver = who



def mail(to, subject, textf, attach, attach2 = None,attach3 = None,attach4 = None):
	

	gmail_user = "padmon29@gmail.com"
	gmail_pwd = "ihee7Jau"


	msg = MIMEMultipart()
	text = open(textf).read()
	msg['From'] = gmail_user
	msg['To'] = to
	msg['Subject'] = subject
	
	msg.attach(MIMEText(text))

	part = MIMEBase('application', 'octet-stream')
	part.set_payload(open(attach, 'rb').read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attach))
	msg.attach(part)

	part2 = MIMEBase('application', 'octet-stream')
	part2.set_payload(open(attach2, 'rb').read())
	Encoders.encode_base64(part2)
	part2.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attach2))
	msg.attach(part2)

	mailServer = smtplib.SMTP("smtp.gmail.com", 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(gmail_user, gmail_pwd)
	mailServer.sendmail(gmail_user, to, msg.as_string())
	# Should be mailServer.quit(), but that crashes...
	mailServer.close()



def get_Data(msg):
	for part in msg.walk():
		
		if part.get_content_type() == 'application/octet-stream': 
			print 'getting attachment'
			name = part.get_filename()	
			f = open("temp/"+name,"w")
			f.write(part.get_payload())		 
					
		elif part.get_content_type() == 'text/plain':
			f = open("temp/encrtext.txt","w")
			f.write(part.get_payload())


def get_Message():

	imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
	imap.login('padmon29@gmail.com','ihee7Jau')
	imap.select('INBOX')

	typ, data = imap.search(None,'SUBJECT',"encrypted mail!!!")
	for num in data[0].split():
		typ, data = imap.fetch(num,'(RFC822)')
		msg = email.message_from_string(data[0][1])
		getData(msg)
		print 'Done!'





def verify_cert(whoto):  
	#download receivers cert
	os.system("wget http://macneill.cs.tcd.ie/~pmonahan/myca/certs/"+whoto+".crt -O certs/temp/"+whoto+".crt")

	#verify the certificate is correct
	if os.system("openssl verify certs/temp/"+whoto+".crt -CAfile certs/trusted/myca.crt| grep OK"):
		print "Error "+whoto+"'s certificate cannot be verified"
		exit(0)

	#extract the public key.
	os.system("openssl x509 -inform pem -in certs/temp/"+whoto+".crt -pubkey -noout > certs/temp/publickey.pem")

	
def make_signature():
	#get the digest of the mail using sha1	
	os.system("openssl dgst -sha1 < mail1.txt > temp/digest.txt")

	#encrypt the digest with the private key of the sender
	os.system("openssl rsautl -sign -inkey certs/privatekey.pem < temp/digest.txt > temp/digest-signed.txt")


def encrypt_message():
	#aes block encrypt the mail file
	os.system("openssl enc -aes-128-cbc -salt -pass file:certs/password.txt < mail1.txt> temp/encrtext.txt")

	#encrypt the password file with the receivers public key
	os.system("openssl rsautl -encrypt -pubin -inkey certs/temp/publickey.pem < certs/password.txt > temp/encrpass.txt")

	#os.system("mutt -s \"hello\" pmonahan@tcd.ie -a ../results/encrpass.txt -a ../results/digest-signed.txt <../results/encrtext.txt")


def decrypt_Message():
	#decrypt password with my private key
	os.system("openssl rsautl -decrypt -inkey certs/privatekey.pem < temp/encrpass.txt > temp/password.txt")

	#decrypt message with password
	os.system("openssl enc -aes-128-cbc -d -pass file:temp/password.txt < temp/encrtext.txt > inbox/mail.txt")

def verify_Signature():
	#get sha1 of the message 
	os.system("openssl dgst -sha1 < inbox/mail.txt > temp/digest-local.txt")
	#use the senders public key to decrypt digest
	os.system("openssl rsautl -pubin -inkey certs/temp/publickey.pem < temp/digest-signed.txt > temp/digest-sender.txt")
	#compare the 2
	os.system("diff temp/digest-{local,sender}.txt")


sign_in()
action = raw_input("What would you like to do?(send/receive):")
if action == "receive":
	prep = "from"
else:
	prep = "to"
whoto = raw_input("Who would you like to "+action+" "+prep+":")

#verify_cert(whoto)

if action == "send":
	os.system("gedit mail1.txt")
	wait = raw_input("If you are happy with your message press <enter>")	
	make_signature()
	encrypt_message()

	mail("padmon29@gmail.com",
	   "encrypted mail!!!",
	   "temp/encrtext.txt",
	   "temp/encrpass.txt",
	   "temp/digest-signed.txt")
else:
	get_Message()
	decrypt_Message()
	verify_Signature()

