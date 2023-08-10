import socket
import pyperclip
import threading
import asyncio
import aioping
import sys

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
    udp.connect(("8.8.8.8", 80))
    local_ip = udp.getsockname()[0]
a = ".".join(local_ip.split(".")[:-1])
all_ip = (f"{a}.{i}" for i in range(256))

def connect(conn, name):
    while True:
        mess = conn.recv(8192).decode("utf-8")
        if mess == "get":
            print(f"\n[*] {name} still your data from clipboard\n")
            conn.send(f"PIZDA1234{pyperclip.paste()}".encode("utf-8"))
        elif mess[:9] == "PIZDA1234":
            pyperclip.copy(mess[9:])
            print(f"\n[*] {name} written data to your clipboard\n")
        else:
            print(f'\n{name}: ', mess, '\n')

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
    for addr in addrs:
        sock.connect(addr)
        if sock.recv(8192).decode("utf-8") == "[*] Connection: OK":
            sock.send("[*] Connection: OK".encode("utf-8"))
            client_name = sock.recv(8192).decode("utf-8")
            sock.send(user.encode("utf8"))
            print("[+] Server is active!!!")
            print(f"[*] Address of server {addr[0]}:{addr[1]}")
            print("[*] Connection: OK\n")
            break

    thr1 = threading.Thread(target=connect, args=(sock, client_name), daemon=True)
    thr2 = threading.Thread(target=receive, args=(sock, client_name))
    thr1.start()
    thr2.start()
    thr1.join()
    thr2.join()

async def check_host(host):
    try:
        await aioping.ping(host)
        return host
    except:
        return
    
async def port_is_open(host, port, timeout=10):
    try:
        _, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        writer.close()
        return host, port
    except:
        return

async def async_main():
    res = filter(None, await asyncio.gather(*[asyncio.ensure_future(check_host(ip)) for ip in all_ip]))
    tasks = []
    async with asyncio.Semaphore(300):
        for ip in res:
            tasks.append(asyncio.ensure_future(port_is_open(ip, 228)))
        data = await asyncio.gather(*tasks)
        global addrs
        addrs = list(filter(None, data))

try:    
    if __name__ == "__main__":
        if sys.argv[1] == "komi":
            asyncio.get_event_loop().run_until_complete(async_main())
            main()
        else:
            sys.exit(0)
except:
    sys.exit(0)