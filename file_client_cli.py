import socket
import json
import base64
import logging

server_address = ('0.0.0.0', 7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False

def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb+') as fp:
            fp.write(isifile)
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename=""):
    with open(filename, 'rb') as fp:
        filecontent = base64.b64encode(fp.read()).decode()
    command_str = f"UPLOAD {filename} {filecontent}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print(f"File {filename} berhasil diupload")
        return True
    else:
        print("Gagal")
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print(f"File {filename} berhasil dihapus")
        return True
    else:
        print("Gagal")
        return False

if __name__ == '__main__':
    server_address = ('172.16.16.101', 6668)
    remote_list()
    remote_get('example.jpg')
    remote_upload('newfile.txt')
    remote_delete('newfile.txt')
