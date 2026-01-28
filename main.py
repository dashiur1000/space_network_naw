from GitHub.space_network_lib import SpaceNetwork
from space_network_lib import SpaceEntity, Packet
import time
from space_network_lib import CommsError, TemporalInterferenceError, DataCorruptedError, LinkTerminatedError, OutOfRangeError

class Satellite(SpaceEntity):
   def __init__(self, name, distance_from_earth):
       super().__init__(name, distance_from_earth)

   def receive_signal(self, packet: Packet):
        if isinstance(packet, RelayPacket):
            inner_packet = packet.data
            print(f"Unwrapping and forwarding to {inner_packet.receiver.name}")
            attempt_transmission(my_net, inner_packet)
        else:
            print(f"Final destination reached: {packet.data}")



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

class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):
        super().__init__(data=packet_to_relay, sender=sender, receiver=proxy)

    def __repr__(self):
        return f"RelayPacket(Relaying [{self.data}] to {self.receiver} from {self.sender})"







Earth = Satellite("Earth", 0)
Sat1 = Satellite("Sat1", 100)
Sat2 = Satellite("Sat2", 200)
my_net = SpaceNetwork(level=3)
p_final = Packet("Hello from Earth!!", Sat1, Sat2)
p_earth_to_sat1 = RelayPacket(p_final, Earth,Sat1)


try:
   attempt_transmission(my_net, p_earth_to_sat1)
except BrokenConnectionError:
   print("Transmission failed")