import time
import threading
import socket

class ClockSynchronizer:
    def __init__(self, ntp_server_ip, client_ips, sync_interval):
        self.ntp_server_ip = ntp_server_ip
        self.client_ips = client_ips
        self.sync_interval = sync_interval
        self.clock_offset = 0

    def get_ntp_time(self):
        return time.time()

    def calculate_rtt(self, client_ip):

        start_time = time.time()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((client_ip, 12345))
            end_time = time.time()
        rtt = end_time - start_time
        s.close()
        return rtt

    def adjust_clock(self, rtt):

        self.clock_offset = rtt / 2

    def synchronize_clocks(self):
        while True:
            try:
                ntp_time = self.get_ntp_time()
                for client_ip in self.client_ips:
                    rtt = self.calculate_rtt(client_ip)
                    time.sleep(2)
                    self.adjust_clock(rtt)
                    adjusted_time = ntp_time + self.clock_offset
                    self.adjust_client_clock(client_ip, adjusted_time)
                    print(f"Cliente {client_ip}: enviado Epoch {adjusted_time}")
                time.sleep(self.sync_interval)
            except Exception as e:
                print(e)

    def adjust_client_clock(self, client_ip, adjusted_time):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((client_ip, 12345))
            s.sendall(str(adjusted_time).encode())
            time.sleep(1)



def main():
    ntp_server_ip = "192.168.1.1"
    client_ips = ["192.168.0.200", "192.168.0.201"]
    sync_interval = 15

    synchronizer = ClockSynchronizer(ntp_server_ip, client_ips, sync_interval)
    synchronization_thread = threading.Thread(target=synchronizer.synchronize_clocks)
    synchronization_thread.start()

if __name__ == "__main__":
    main()


