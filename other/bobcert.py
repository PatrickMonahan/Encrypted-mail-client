extract a public key:

#openssl x509 -inform pem -in certificate.pem -pubkey -noout > publickey.pem

change - in


encrypt with the public key:
#openssl rsautl -encrypt -inkey public.pem -pubin -in file.txt -out file.ssl

decrypt a message:
#openssl rsautl -decrypt -inkey private-key.pem < test-encrypted.txt

this only works for small pieces of data for larger data block we have to usean AES block cipher, the sender makes up a key to encode the blocks with and will send this key to the receiver with the message

this actually works out faster

we have to first create a password within a file, eg hell in test.txt
we then encrypt the main file with this password:

#openssl enc -aes-128-cbc -salt -pass file:text.txt < mail1.txt > words.dat

we then encrypt the password file (text.txt) with the senders public key.

#openssl rsautl -encrypt -pubin -inkey public-key.pem < test.txt > test-encrypted.txt

then we have 2 files to send words.dat and test-encrypted-data.txt
