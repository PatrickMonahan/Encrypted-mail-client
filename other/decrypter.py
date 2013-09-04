
sender = raw_input("Who is this message from? : ")

#download sender's cert
os.system("wget http://macneill.cs.tcd.ie/~pmonahan/myca/certs/"+sender+".crt -O certs/temp/"+sender+".crt")

#verify the certificate is correct
if os.system("openssl verify certs/temp/"+sender+".crt -CAfile certs/trusted/myca.crt| grep OK"):
	print "Error "+sender+"'s certificate cannot be verified"
	exit(0)


#extract the public key.
os.system("openssl x509 -inform pem -in certs/temp/"+sender+".crt -pubkey -noout > certs/temp/publickey.pem")


#decrypt password with my private key
os.system("openssl rsautl -decrypt -inkey certs/privatekey.pem < temp/encrpass.txt > temp/password.txt")

#decrypt message with password
os.system("openssl enc -aes-128-cbc -d -pass file:temp/password.txt < temp/encrtext.dat > inbox/mail.txt")

#get sha1 of the message 
os.system("openssl dgst -sha1 < inbox/mail.txt > temp/digest-local.txt")
#use the senders public key to decrypt digest
os.system("openssl rsautl -pubin -inkey certs/temp/publickey.pem < temp/digest-signed.txt > temp/digest-sender.txt")
#compare the 2
os.system("diff ../decresult/digest-{local,sender}.txt")
