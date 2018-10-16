from functools import wraps
import time
import requests

def log(func):
    def wrapper(*args,**kwargs):
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_str = localtime +'\t' + func.__name__ + "was call\n"
        with open('run.log','a') as fn:
            fn.write(log_str)
        try:
            return func(*args,**kwargs)

        # except requests.ConnectionError:
        #     str = "A Connection error occurred."
        #     print(str)
        #
        # except requests.HTTPError:
        #     str = "An HTTP error occurred."
        #     print(str)
        #
        # except requests.URLRequired:
        #     str = "A valid URL is required to make a request."
        #     print(str)
        #
        # except requests.TooManyRedirects:
        #     str = "Too many redirects."
        #     print(str)
        #
        # except requests.ReadTimeout:
        #     str = "The server did not send any data in the allotted amount of time."
        #     print(str)
        #
        # except requests.Timeout:
        #     str = "The request timed out."
        #     print(str)
        #
        #
        # except requests.RequestException:
        #     str = "There was an ambiguous exception that occurred while handling your request."
        #     print(str)
        #
        except:
            pass

    return wrapper



