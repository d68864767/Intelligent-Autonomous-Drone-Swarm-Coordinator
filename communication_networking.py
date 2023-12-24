```python
# Import necessary libraries
from drone_control_module import DroneControlModule
from swarm_coordination_algorithms import SwarmCoordinationAlgorithms
import socket
import threading
import json

class CommunicationNetworking:
    def __init__(self, drone_ids, host='localhost', port=12345):
        self.swarm = SwarmCoordinationAlgorithms(drone_ids)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(len(drone_ids))
        self.connections = []

    def connect_all(self):
        """Connect to all drones in the swarm"""
        self.swarm.connect_all()

    def disconnect_all(self):
        """Disconnect from all drones in the swarm"""
        self.swarm.disconnect_all()

    def accept_connections(self):
        """Accept connections from all drones in the swarm"""
        for i in range(len(self.swarm.drones)):
            conn, addr = self.server.accept()
            self.connections.append(conn)
            print(f"Drone {i+1} connected from {addr}")

    def send_data(self, data):
        """
        Send data to all drones in the swarm
        :param data: The data to be sent
        """
        for conn in self.connections:
            conn.sendall(json.dumps(data).encode())

    def receive_data(self):
        """
        Receive data from all drones in the swarm
        :return: A list of data received from each drone
        """
        data = []
        for conn in self.connections:
            data.append(json.loads(conn.recv(1024).decode()))
        return data

    def close_connections(self):
        """Close connections to all drones in the swarm"""
        for conn in self.connections:
            conn.close()

if __name__ == "__main__":
    # Test the CommunicationNetworking class
    comm = CommunicationNetworking(['drone1', 'drone2', 'drone3'])
    comm.connect_all()
    comm.accept_connections()
    comm.send_data({"command": "takeoff"})
    data = comm.receive_data()
    print(data)
    comm.close_connections()
    comm.disconnect_all()
```
