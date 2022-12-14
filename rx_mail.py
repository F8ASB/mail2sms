from imap_tools import MailBox, AND

# reception des nouveaux mails uniquement, du sujet, et du messsage
with MailBox('imap.gmail.com').login('XXXX@gmail.com', 'PASSWORD') as mailbox:
    for msg in mailbox.fetch(AND(seen=False)):
        print(msg.from_, msg.subject, msg.text)
