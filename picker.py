import argparse, os, sys, glob
import smtplib, random

everyone='everyone.dat'
not_yet='not_yet.dat'

def picker(everyone, not_yet):
    emails=[]
    # Get the list ofpeople who haven't written yet
    filein=open(not_yet,'r')
    for line in filein:
        line=line.strip('\n')
        emails.append(line)
    if len(emails)==0:
       print "not_yet.dat is empty. Copying everyone.dat again."
       os.system('cp everyone.dat not_yet.dat')
       filein=open(not_yet,'r')
       for line in filein:
           line=line.strip('\n')
           emails.append(line)
       print emails
    
    # Pick one of them at random
    writer=random.choice(emails)
    print writer,"has been chosen to post in the blog next week." 
     
    # Generate a new not_yet.dat file without the person who was selected this time
    newnotyet=open('newnotyet.dat','w')
    for email in emails:
        if email==writer:
           #print email, "is not going to be printed in newnotyet.dat"
           continue
        line=email+'\n'
        newnotyet.write(line)
    os.system("mv newnotyet.dat not_yet.dat")

    witnesses=[]
    filein=open(everyone,'r')
    for line in filein:
        line=line.strip('\n')
        if line==writer:
           continue
        witnesses.append(line)
    witness=random.choice(witnesses)
    
    print witness, "will be told."
    return writer, witness

def send_email(writer,witness):
    writer_email="Subject: YOU are going to write for the Writing Fairy next Week\nDear Human,\nThe Writing Fairy will be very pleased to read your work next week. If said work can't be delivered in time, please let my Personal Assistant know at joan.clark88@gmail.com (DO NOT REPLY TO THIS EMAIL!)"
    witness_email="Subject: "+writer+" is going to write for the Writing Fairy next Week\nDear Human,\nThe Writing Fairy has decided to read "+writer+"'s work next week."
    print "Initialising smtp...."
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    print "Trying to login...."
    smtpObj.login('writing.fairy2018@gmail.com','newcastle2018')
    print "Sending writer email to", writer
    smtpObj.sendmail('writing.fairy2018@gmail.com', writer, writer_email)
    print "Sending witness email to", witness
    smtpObj.sendmail('writing.fairy2018@gmail.com', witness, witness_email)
    #Send all confirmations to Joan in case the program stops working
    smtpObj.sendmail('writing.fairy2018@gmail.com', "joan.clark88@gmail.com", witness_email)

if __name__=="__main__":
    print "Let's get down to business"

    writer,witness=picker(everyone, not_yet)
    send_email(writer,witness)
