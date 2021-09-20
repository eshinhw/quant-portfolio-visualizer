import smtplib
from email.message import EmailMessage
import credentials

def sendEmail(subject, curr_pos, filters, watchlist):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = credentials.GMAIL_ADDRESS
    msg["To"] = credentials.GMAIL_ADDRESS

    msg.add_alternative(
        f"""\

        <!DOCTYPE html>
        <html>
            <body>
                <p> Hello Investors,<br> Below is the daily summary of your portfolio and updated stock watchlist.<br> Have a good evening :) </p>
                <h1> Portfolio Overview </h1>
                <h3> Investment Summary </h3>
                {curr_pos}
                <h1> Watchlist - S&P500 Discounted Stocks </h1>
                <h3> Conditional Filters </h3>
                {filters}
                <br>
                {watchlist}
            </body>
        </html>
    """,
        subtype="html",
    )
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(credentials.GMAIL_ADDRESS, credentials.GMAIL_PW)
        smtp.send_message(msg)