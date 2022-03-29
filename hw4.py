import random

class Node():
    def __init__(self, name, send_neigh=None, recv_msgs=False):
        self.name = name
        self.send_neigh = send_neigh # neighbor it will send messages to
        self.recv_msgs = recv_msgs # check if it's receiving

        self.power = 100

        self.rate = 25*10000
        self.last_sent = 0 # time last sent message
        self.next_send = 0 # time until next message is sent

        self.recvd = "" # received message from other neighbor
        self.recvd_rate = 0 # rate from neighbor that sent message

        self.died = False

    def calc_power(self, msg):

        factor = 0
        if self.recv_msgs:
            factor = 0.002
        else:
            factor = 0.001

        self.power -= ( len(msg)*8 * (self.rate * (factor+1)) )

        if self.power <= 0:
            print("power level: ", self.power)
            self.died = True

        self.next_send = len(msg)*8 / self.rate

        self.rate *= (self.power * 0.01)

    def hacked(self):
        self.calc_power("HACKED")

    def recv(self, msg, rate):
        self.recvd += msg
        self.recvd_rate = rate

    def send_message(self):
        # Determined if neighbor sending msgs is suspicious
        msg = "ALIVE"
        if self.recvd_rate < self.rate:
            # SUS
            print("Previous node hacked")
            msg += self.name
        else:
            msg += "0"

        if self.recvd != "":
            msg += self.recvd
            self.recvd = ""

        print(self.name, " sent message: ", msg)

        # Send message along
        self.send_neigh.recv(msg, self.rate)

        # Calculate new power level
        self.calc_power(msg)

    def send(self, current_time=0):
        if self.died:
            return False

        if (current_time >= (self.last_sent + self.next_send)):
            self.send_message()
            self.last_sent = current_time
            return True
        

def main():
    
    hub = Node("h", None, True)
    d = Node("d", hub, True)
    c = Node("c", d, True)
    b = Node("b", c, True)
    a = Node("a", b, False)
    
    # a -> b -> c -> d -> HUB
    nodes = [d, c, b, a]

    hacker_picked = random.choice(nodes)
    print("Hacker picked to attack node: ", hacker_picked.name)
    c.hacked()

    current_time = 0
    while True:
        for n in nodes:
            success = n.send(current_time=current_time)
            if not success:
                # node has died!
                print(n.name, " Died!")
                return
        current_time += 1


if __name__ == "__main__":
    main()
