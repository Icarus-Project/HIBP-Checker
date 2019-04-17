#!/usr/bin/python3.4 
import requests
import time
import argparse
import sys
import os

PWNED_API_URL = "https://haveibeenpwned.com/api/v2/breachedaccount/"

def get_args():
	parser = argparse.ArgumentParser(description='Verifica HaveIBeenPowned?.')
	parser.add_argument("-a", dest="address",help="Single email address to be checked")
	parser.add_argument("-f", dest="filename",help="File to be checked with one email addresses per line")
	parser.add_argument("-o", dest="output_file", help="File to save output")

	args = parser.parse_args()
	
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	return parser.parse_args()

def check_mail(email_list,output_file):
	sleep = 1.6
	
	for mail in email_list:
		mail = mail.strip()
		check = requests.get(PWNED_API_URL + mail)
		
		if str(check.status_code) == "200":
			c = "[!] " + mail + " appare nel database!"

		elif str(check.status_code) == "404":
			c = "[~] " + mail + " Tutto ok!"

		elif str(check.status_code) == "429":
			c = "[x] " + mail + " Superato limite richieste"
			sleep += 1

		time.sleep(sleep)
		
		if (output_file):
			with open(output_file, "a") as out_file:
				out_file.write(c)
				out_file.write("\n")
		else:
			print(c)	

def main():
	email_list = []
	opts = get_args()
	
		
	if opts.address:
		email_list = [opts.address]
		check_mail(email_list,opts.output_file)
		
	elif opts.filename:
		print("Selezionato file di mail",opts.filename)
		with open(str(opts.filename), "r") as mail_list:
			check_mail(mail_list,opts.output_file)
			#print(mail,type(mail))


if __name__ == '__main__':
        main()

