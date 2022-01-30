import os
import smtplib
import bot_vars

# retrieve bot email credentials used for user authentication
async def get_credentials():
    return os.getenv('BOT_EMAIL_USER'), os.getenv('BOT_EMAIL_PASS')

# send authentication email to unauthenticated users
async def send_auth_email(user):
    BOT_EMAIL, BOT_PASS = await get_credentials()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(BOT_EMAIL, BOT_PASS)
    msg = f'Hello {bot_vars.users[user.netid]},\n\nCopy and paste the following code into the #auth channel: !verify {user.passkey}\n\n-Sincerely, UTK Auth Bot'
    s.sendmail(BOT_EMAIL, user.netid+bot_vars.email_tag, msg)
    s.quit()