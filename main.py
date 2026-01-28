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
            print(f"[{self.name}] Unwrapping and forwarding to {inner_packet.receiver.name}")
            attempt_transmission(my_net, inner_packet)
        else:
            print(f"[{self.name}] Final destination reached: {packet.data}")



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

def smart_send_packet(entities, packet, network):
    start = entities.index(packet.sender)
    end = entities.index(packet.receiver)
    path = entities[start+1:end]
    current_packet = packet
    for proxi in reversed(path):
        current_packet = RelayPacket(current_packet, current_packet.sender, proxi)
    attempt_transmission(network, current_packet)






Earth = Satellite("Earth", 0)
Sat1 = Satellite("Sat1", 100)
Sat2 = Satellite("Sat2", 200)
Sat3 = Satellite("Sat3", 300)
Sat4 = Satellite("Sat2", 400)
all_entities = [Earth, Sat1, Sat2, Sat3, Sat4]
my_net = SpaceNetwork(level=3)
p_final = Packet("Hello from Earth!!", Earth, Sat4)

try:
   smart_send_packet(all_entities, p_final, my_net)
except BrokenConnectionError:
   print("Transmission failed")