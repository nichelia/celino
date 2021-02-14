import grpc
import sys
from clearly.utils import logo
from clearly.client import ClearlyClient


def configure_host_and_port():
    host = "clearly-server"
    port = 12223

    if len(sys.argv) == 2:
        host = sys.argv[1]
    if len(sys.argv) == 3:
        port = sys.argv[2]
    
    return host, port


def establish_connection_with_server(host, port, timeout:int=10):
    channel = grpc.insecure_channel('{}:{}'.format(host, port))
    try:
        grpc.channel_ready_future(channel).result(timeout=timeout)
        return True
    except grpc.FutureTimeoutError:
        return False


def main():
    print(logo.render('client') + '\n')

    host, port = configure_host_and_port()

    while not establish_connection_with_server(host, port):
        print("Waiting to establish connection to the clearly server...")
        
    clearlycli = ClearlyClient(host, port)
    clearlycli.capture()


if __name__ == "__main__":
    main()