import smtplib, os,getpass,urllib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from BeautifulSoup import BeautifulSoup


def send_mail(send_from, send_to, subject, text, server="smtp.gmail.com",    
username=None,password=None,url=''):
	assert type(send_to)==list

	msg = MIMEMultipart()
	msg['From'] = send_from
	msg['To'] = str(send_to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject

	msg.attach( MIMEText(text,'plain') )
	msg.attach( MIMEText('<br/><img src="'+str(url)+'"/>','html'))
	err=[]
	smtp = smtplib.SMTP(server)
	smtp.ehlo()
	smtp.starttls()
	smtp.ehlo()
	if not password:
		password=getpass.getpass("%s 's password :"%(username))
	smtp.login(username,password)
	for sendadd in send_to:
		err.append(smtp.sendmail(send_from, sendadd, msg.as_string()))
	smtp.close()
	return err



def getfile(url="http://www.xkcd.com"):
	page=urllib.urlopen(url).read()
	soup=BeautifulSoup(page)
	div=soup.findAll('div',{'id':'comic'})[0]
	img=div.findAll('img')[0]
	return img['src']

page='''
		<br/>
		Send to (Comma seperated values) : <input type="text" name="address"/>
		<br/>
		Subject : <input type="text" name="subject"/>
		<br/>
		Text : <input type="text" name="text"/>
		<br/>
		Username : <input type="text" name="user"/>
		<br/>
		Password : <input type="password" name="password"/>
		<br/>
		<input type="submit" value="Send Mail"/>
		</form>
		'''
def index(req):
	global page
	req.content_type="text/html"
	return """
		<form action="test.py/mail" method="GET">
			Enter comic number : <input type="text" name="comic"/>
			<input type="submit"/>
		</form>
		"""
urlw='';
def mail(req,comic):
	global page,urlw
	req.content_type='text/html'
	url=getfile('http://www.xkcd.com/'+str(comic)+'/')
	urlw=url
	return '<br/><img src="'+str(url)+'"/><form action="sendmail" method="POST"><input type="text" name="comic" style="display:none" value="'+str(comic)+'"/>'+page

def sendmail(req,password,comic,address,user,subject,text,**kwargs):
	global urlw
	req.content_type="text/html"
	address=address.split(",")
	err=send_mail(send_from="No name",\
		send_to=address,
		subject=subject,
		text=text,
		username=user,
		password=password,url=urlw)
	return """<script>alert('Mail Sent Successfully/Error code """+str(err)+"""');
			location.href='/test.py'</script>"""

