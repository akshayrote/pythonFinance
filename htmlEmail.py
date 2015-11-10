# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

# Define these once; use them twice!
strFrom = 'roteakshay9@gmail.com'
strTo = 'akshay.rote@gmail.com'

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'test message'
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('related')
msgRoot.attach(msgAlternative)


# We reference the image in the IMG SRC attribute by the ID we give it below
msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br>Nifty!'+'Hi Akshay', 'html')
msgAlternative.attach(msgText)

# Send the email (this example assumes SMTP authentication is required)
import smtplib
smtp = smtplib.SMTP()
smtp.connect('smtp.gmail.com:587')
smtp.ehlo()
smtp.starttls()
smtp.login('roteakshay9@gmail.com', '****')
smtp.sendmail(strFrom, strTo, msgRoot.as_string())
smtp.quit()