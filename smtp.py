import logging
import smtplib
import ssl

class SMTPClient:
    """ 
        SMTP Client 
        Sends e-mails over the SMTP protocol
    """

    def __init__(self, host: str, username: str, password: str, sender_address: str, port: int, use_ssl: bool = True, use_tls: bool = False):
        """ Constructor of SMTPClient """
        self.host = host
        self.username = username
        self.password = password
        self.sender_address = sender_address
        self.port = port
        self.use_ssl = use_ssl
        self.use_tls = use_tls
        self.context = ssl.create_default_context()

        if self.use_ssl and self.use_tls:
            raise ValueError("SMTPClient: SSL and TLS are both enabled, please check your configuration")
        if not self.use_ssl and not self.use_tls:
            logging.warning("SMTPClient: SSL and TLS are both disabled, insecure configuration")
        
        # Ensure that connection to SMTP server works
        self.verify_connection()

    def verify_connection(self):
        """ Verifies the connection with the SMTP server """
        try:
            with self.get_connection() as smtp_server:
                self.connect(smtp_server)
        except smtplib.SMTPHeloError:
            logging.fatal(f"SMTPClient: Connection to server {self.host}:{self.port} refused:")
            logging.exception()
        except smtplib.SMTPAuthenticationError:
            logging.fatal(f"SMTPClient: Username or Password on server {self.host}:{self.port} refused:")
            logging.exception()
        except Exception:
            logging.fatal(f"SMTPClient: Connection error on server {self.host}:{self.port}:")
            logging.exception()

    def connect(self, smtp_server):
        """ Connects and authenticates to the SMTP server """
        if self.use_tls:
            smtp_server.starttls(context=self.context)
        smtp_server.login(self.username, self.password)
        return smtp_server

    def get_connection(self):
        """ Builds a connection object for the SMTP server and returns it """
        if self.use_ssl:
            return smtplib.SMTP_SSL(self.host, self.port, self.context)
        else:
            return smtplib.SMTP(self.host, self.port)
