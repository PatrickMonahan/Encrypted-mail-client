#!/bin/bash    
set -e

#decrypt password with my private key
openssl rsautl -decrypt -inkey cert/privatekey.pem < results/encrpass.txt > decresult/password.txt

#decrypt message with password
openssl enc -aes-128-cbc -d -pass file:decresult/password.txt < results/encrtext.dat > decresult/mail.txt

#verify the hash is correct
#openssl rsautl -verify -inkey cert/publickey.pem -pubin < results/digest-signed.dat > decresult/digest-sender.txt


#or compare hashes
#get sha1 of the message 
openssl dgst -sha1 < decresult/mail.txt > decresult/digest-local.txt
#use the senders public key to decrypt digest
openssl rsautl -pubin -inkey cert/publickey.pem < results/digest-signed.dat > decresult/digest-sender.txt
#compare the 2
diff decresult/digest-{local,sender}.txt

