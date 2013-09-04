import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders


gmail_user = "padmon29@gmail.com"
gmail_pwd = "ihee7Jau"

def mail(to, subject, textf, attach, attach2 = None,attach3 = None,attach4 = None):
   msg = MIMEMultipart()
   text = open(textf).read()
   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   part2 = MIMEBase('application', 'octet-stream')
   part2.set_payload(open(attach2, 'rb').read())
   Encoders.encode_base64(part2)
   part2.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach2))
   msg.attach(part2)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()


receiver=raw_input('Please enter receiver:')
  
#download receivers cert
#os.system("wget http://macneill.cs.tcd.ie/~pmonahan/myca/certs/"+receiver+".crt -O certs/temp/"+receiver+".crt")

#verify the certificate is correct
#if os.system("openssl verify certs/temp/"+receiver+".crt -CAfile certs/trusted/myca.crt| grep OK"):
#	print "Error "+receiver+"'s certificate cannot be verified"
#	exit(0)

#extract the public key.
#os.system("openssl x509 -inform pem -in certs/temp/"+receiver+".crt -pubkey -noout > certs/temp/publickey.pem")

#get the digest of the mail using sha1
os.system("openssl dgst -sha1 < mail1.txt > temp/digest.txt")

#encrypt the digest with the private key of the sender
os.system("openssl rsautl -sign -inkey certs/privatekey.pem < temp/digest.txt > temp/digest-signed.txt")

#aes block encrypt the mail file
os.system("openssl enc -aes-128-cbc -salt -pass file:certs/password.txt < mail1.txt> temp/encrtext.txt")

#encrypt the password file with the receivers public key
os.system("openssl rsautl -encrypt -pubin -inkey certs/temp/publickey.pem < certs/password.txt > temp/encrpass.txt")

#os.system("mutt -s \"hello\" pmonahan@tcd.ie -a ../results/encrpass.txt -a ../results/digest-signed.txt <../results/encrtext.txt")


mail("padmon29@gmail.com",
   "encrypted mail!!!",
   "temp/encrtext.txt",
   "temp/encrpass.txt",
   "temp/digest-signed.txt")
