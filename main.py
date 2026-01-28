from GitHub.space_network_lib import SpaceNetwork
from space_network_lib import SpaceEntity, Packet
import time
class Satellite(SpaceEntity):
   def __init__(self, name, distance_from_earth):
       super().__init__(name, distance_from_earth)
       self.distance_from_earth = distance_from_earth
   def receive_signal(self, packet: Packet):
       print(f"[{self.name}] received: {packet}")






Sat1 = Satellite("Sat1", 100)
Sat2 = Satellite("Sat2", 200)
my_net = SpaceNetwork()
Packet1 = Packet("Hello", Sat1, Sat2)
my_net.send(Packet1)