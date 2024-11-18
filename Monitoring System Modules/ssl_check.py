import ssl
import socket
from datetime import datetime

def check_certificate(url):
    try:
        # remove "https://", "http://"from the url if present.
        hostname = url.replace("https://", "").replace("http://", "").split("/")[0]

        #establish a secure connection to fetch the ssl certificate
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        # get the certificate's expiration date

        expiry_date_str = cert['notAfter']
        expiry_date = datetime.strptime(expiry_date_str, "%b %d %H:%M:%S %Y %Z")

        #convert expiration date to a readeble string format
        expiry_date_formatted = expiry_date.strftime("%Y-%m-%d %H:%M:%S")

        # check if the certificate is expired
        if expiry_date < datetime.utcnow():
            return 'expired', expiry_date_formatted
        else:
            return 'valid' ,expiry_date_formatted
    except Exception as e:
        return 'failed', str(e)
    

#test url:
print(check_certificate('https://google.com'))
    

