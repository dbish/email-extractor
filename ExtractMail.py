import imaplib, email, re, sys


def getText(message_instance):
	maintype = message_instance.get_content_maintype()
	if maintype == 'multipart':
		for part in message_instance.get_payload():
			if part.get_content_maintype() == 'text':
				return part.get_payload()
	elif maintype == 'text':
		return message_instance.get_payload()

def connectInbox(imap, username, password):
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(username, password)
	mail.select("inbox")
	return mail

def getNewMail(mailbox):
	result, data = mail.uid('search', None, "UnSeen")
	email_uids = ','.join(data[0].split())
	result, data = mail.uid('fetch', email_uids, '(RFC822)')
	return data

def compileRegex(searchStrings):
	regex = '|'.join(searchStrings)
	compiledRegex = re.compile(r"("+regex+")", re.IGNORECASE)
	return compiledRegex

def searchBody(messageBody, searchRegex):
	if searchRegex.search(messageBody):
		return True
	else:
		return False

def fileToList(fname):
	stringList = [line.strip() for line in open(fname)]
	return stringList

#read from args
#[1] = emailAddress
#[2] = password
#[3] = text file with a search string on each line
numArgs = len(sys.argv)
if numArgs < 4:
	print("usage: python MailExtraction <username@gmail.com> <password> <file name for search strings> ")
	sys.exit(2)

emailAd = sys.argv[1]
password = sys.argv[2]

#read in search strings
searchFile = sys.argv[3]
searchStrings = fileToList(searchFile)

validFrom = []

#intiialization, connect to email and compile search regex
mail = connectInbox('imap.gmail.com', emailAd, password)

searchProg = compileRegex(searchStrings)

#fetch unread emails and mark them as read
newMail = getNewMail(mail)

#find emails that contain the requested information in the email body
#TODO: store emails in database (for now printing subject to screen)
for message in newMail:
	rawMessage = message[1]
	emailMessage = email.message_from_string(rawMessage)
	if (emailMessage['From']):
		messageBody = getText(emailMessage)
		if searchBody(messageBody, searchProg):
			print("--------------")
			print(emailMessage['Subject'])	
	

