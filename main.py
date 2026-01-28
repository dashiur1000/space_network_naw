from GitHub.space_network_lib import SpaceNetwork
from space_network_lib import SpaceEntity, Packet
import time
from space_network_lib import TemporalInterferenceError, DataCorruptedError
class Satellite(SpaceEntity):
   def __init__(self, name, distance_from_earth):
       super().__init__(name, distance_from_earth)
       self.distance_from_earth = distance_from_earth
   def receive_signal(self, packet: Packet):
       print(f"[{self.name}] received: {packet}")


def attempt_transmission(network, packet):
   while True:
       try:
           network.send(packet)
           break
       except TemporalInterferenceError:
           print("Interference, waiting...")
           time.sleep(2)
       except DataCorruptedError:
           print("Data corrupted, retrying...")








Sat1 = Satellite("Sat1", 100)
Sat2 = Satellite("Sat2", 200)
my_net = SpaceNetwork(level=3)
Packet1 = Packet("Hello", Sat1, Sat2)
attempt_transmission(my_net, Packet1)