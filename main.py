from GitHub.space_network_lib import SpaceNetwork
from space_network_lib import SpaceEntity, Packet
import time
from space_network_lib import CommsError, TemporalInterferenceError, DataCorruptedError, LinkTerminatedError, OutOfRangeError
class Satellite(SpaceEntity):
   def __init__(self, name, distance_from_earth):
       super().__init__(name, distance_from_earth)
       self.distance_from_earth = distance_from_earth
   def receive_signal(self, packet: Packet):
       print(f"[{self.name}] received: {packet}")


class BrokenConnectionError(CommsError):
   pass


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
       except LinkTerminatedError:
           print("Link lost")
           raise BrokenConnectionError
       except OutOfRangeError:
           print("Target out of range")
           raise BrokenConnectionError








Sat1 = Satellite("Sat1", 100)
Sat2 = Satellite("Sat2", 200)
my_net = SpaceNetwork(level=3)
Packet1 = Packet("Hello", Sat1, Sat2)


try:
   attempt_transmission(my_net, Packet1)
except BrokenConnectionError:
   print("Transmission failed")