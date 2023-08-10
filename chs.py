import socket
import pyperclip
import threading
import sys

def connect(conn, name):
    while True:
        mess = conn.recv(8192).decode("utf-8")
        if mess == "get":
            print(f"\n[*] {name} still your data from clipboard\n")
            conn.send(f"PIZDA1234{pyperclip.paste()}".encode("utf-8"))
        elif mess[:9] == "PIZDA1234":
            pyperclip.copy(mess[9:])
            print(f"\n[*] {name} written data to your clipboard\n")
        elif mess != '':
            print(f'\n{name}: {mess}\n')

def receive(conn, name):
    while True:
        mess = input()
        if mess == "get":
            conn.send("get".encode("utf-8"))
            print("[*] Still data from clipboard OK\n")
        elif mess == "set":
            conn.send(f"PIZDA1234{pyperclip.paste()}".encode("utf-8"))
            print(f"[*] Your clipboard data send to {name}\n")
        elif mess == "exit":
            exit(0)
        else:
            conn.send(mess.encode("utf-8"))

def main():
    user = input("Enter your nickname: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.connect(("8.8.8.8", 80))
        local_ip = udp.getsockname()[0]
    sock.bind((local_ip, 228))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("[+] Waiting of connection...")
    while True:
        sock.listen()
        connection, address = sock.accept()
        try:
            connection.send("[*] Connection: OK".encode("utf-8"))
            if connection.recv(8192).decode("utf-8") == "[*] Connection: OK":
                print(f"[*] Connection from {address[0]}:{address[1]}\n")
                connection.send(user.encode("utf-8"))
                client_name = connection.recv(8192).decode('utf-8')
                thr1 = threading.Thread(target=connect, args=(connection, client_name), daemon=True)
                thr2 = threading.Thread(target=receive, args=(connection, client_name))
                thr1.start()
                thr2.start()
                thr1.join()
                thr2.join()
        except:
            pass

try:
    if __name__ == "__main__":
        if sys.argv[1] == "komi":
            main()
        else:
            sys.exit(0)
except:
    sys.exit(0)