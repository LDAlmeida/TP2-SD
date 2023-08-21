import socket
import subprocess

def main():

    server_ip = "192.168.1.1"  # Endereço IP do servidor de sincronização
    server_port = 12345  # Porta de sincronização
    
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", server_port))
            s.listen()
            print("Aguardando conexão...")
            conn, addr = s.accept()
            print(f"Conexão estabelecida com {addr}")
            data = conn.recv(1024)
            if data:
                adjusted_time = float(data.decode())                             
                
                command = f"date -s '@{adjusted_time}'"

                # Executa o comando e captura a saída
                result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Verifica o resultado
                if result.returncode == 0:
                    print("Data e hora atualizadas com sucesso.")
                else:
                    print("Erro ao atualizar a data e hora:")
                    print(result.stderr)

        conn.close()



if __name__ == "__main__":

    main()

