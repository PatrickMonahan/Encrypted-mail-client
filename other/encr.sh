#!/bin/bash    
set -e

#openssl verify cert/bob.pem -CAfile cacert.pem||{"Certificate not verified";exit 1;}

#openssl x509 -inform pem -in cert/certificate.pem -pubkey -noout > publickey.pem

#do hash function on text, using sha1 to get the message digest
openssl dgst -sha1 < mail1.txt > results/digest.txt

#use senders private key to create signed digest
openssl rsautl -sign -inkey cert/privatekey.pem < results/digest.txt > results/digest-signed.dat

#encrypt the email file with the password
openssl enc -aes-128-cbc -salt -pass file:password.txt < mail1.txt > results/encrtext.dat
#encryt the password with the public key
openssl rsautl -encrypt -pubin -inkey cert/publickey.pem < password.txt > results/encrpass.txt
