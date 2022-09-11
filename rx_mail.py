from imap_tools import MailBox, AND

# Get date, subject and body len of all emails from INBOX folder
with MailBox('imap.gmail.com').login('XXXX@gmail.com', 'PASSWORD') as mailbox:
    for msg in mailbox.fetch(AND(seen=False)):
        print(msg.from_, msg.subject, msg.text)