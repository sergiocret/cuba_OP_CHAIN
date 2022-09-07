import subprocess
class mailer:
  def __init__(self,sbj,txt):
    self.SENDMAIL = "mailx" # sendmail location
    self.TO = 'sergio.creti@cmcc.it'
    self.FROM = "\'sergio.creti@cmcc.it (CMCC Team)\'"
    sbj = sbj.replace(":"," ")
    txt = txt.replace(":"," ")
    txt = txt.replace("!","\n")
    self.SUBJECT = 'CMCC-OP '+sbj
    self.TEXT = txt
#  @staticmethod
  def send(self):
    # Prepare actual message
    msg="""%s -r %s -s \'%s\' %s <<EOF
    %s
EOF""" % (self.SENDMAIL, self.FROM, self.SUBJECT, self.TO, self.TEXT)
    # Send the mail
    try:
      print(msg)
      p = subprocess.call(msg,shell=True)
    except OSError as e:
      print("There is a problem with the email! Mail not sent!!")
      print(e)
