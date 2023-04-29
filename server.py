import socket
import multiprocessing
import re

HOST = 'localhost'
PORT = 2222
connections_count = 0
pattern = re.compile('''\d+''')
tmp_data = 0
temp = 0
i = 1
mas = []

def handle_client(conn, client_id, logs):
    global i
    while True:

        data = conn.recv(1024)
        if not data:
            break
        data_str = data.decode('utf-8')
        match = re.findall(pattern, data_str)
        if match:
            logs[client_id].append(match[0])
            mas.append(int(match[0]))
            global tmp_data
            tmp_data = match[0]
        if client_id >= 2 and tmp_data==logs[client_id][-1]:
            print(">>Robbers were caught successfully")
            conn.close()
        print(data_str)
    conn.close()


def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        global i
        global mas
        client_id = i
        logs = dict()
        logs[client_id] = []
        mas = []
        while True:
            conn, addr = s.accept()
            print(f'Connected by {addr}')

            print(client_id+54)

            process = multiprocessing.Process(target=handle_client, args=(conn, client_id, logs))
            i += 1
            process.start()

if __name__ == '__main__':
    print(">>Server goes brrrrrrrrrr...")
    main()
