import threading
import time
import random

class BarberShop(threading.Thread):
  running = True
  def __init__(self, barber, numberOfSeats, customers, lock):
    threading.Thread.__init__(self)
    self.barber = barber
    self.numberOfSeats = numberOfSeats
    self.customers = customers
    self.lock = lock
    self.waitingCustomers = []
  def start(self):
    while self.running:
      self.enterBarberShop()
      self.barberGoToWork()
  def enterBarberShop(self):
    self.lock.acquire()
    if len(self.customers) <= 0: return
    customer = self.customers.pop()
    print "%s entered the shop looking for a seat" % customer.name
    if len(self.waitingCustomers) == self.numberOfSeats:
      print "The shop is full. %s is walking away" % customer.name
    else:
      self.waitingCustomers.append(customer)
      self.lock.release()
      self.barber.wakeUp()
  def barberGoToWork(self):
    self.lock.acquire()
    # True by default, blocking lock
    if len(self.waitingCustomers) > 0:
      customer = self.waitingCustomers[0]
      del self.waitingCustomers[0]
      self.lock.release()
      self.barber.cutHair(customer)
    else:
      self.lock.release()
      print "Aaah, all done, going to sleep"
      self.barber.sleep()
      print "Barber woke up"
class Customer(object):
  def __init__(self, name):
    self.name = name
class Barber(threading.Event):
  def __init__(self):
    threading.Event.__init__(self)
  def sleep(self):
    self.wait()
  def wakeUp(self):
    self.set()
  def cutHair(self, customer):
    self.clear()
    print "%s is having a haircut" % customer.name
    time.sleep(random.uniform(1, 10))
    print "%s is done" % customer.name
def BarberShopRun():
  shop = BarberShop(Barber(), 3, [
    Customer('Bragi'),
    Customer('Auja'),
    Customer('Iris'),
    Customer('Axel'),
    Customer('Andrea'),
    Customer('Agnar'),
    Customer('Mamma'),
    Customer('Solla'),
    Customer('Olla'),
    Customer('Berglind'),
    Customer('Bergdis'),
    Customer('Margret'),
    Customer('Brynjar'),
    Customer('Siggi'),
    Customer('Tomas'),
    Customer('Kristrun'),
    Customer('Heidrun')
  ], threading.Lock())
  shop.run()
  time.sleep(100)
  BarberShop.running = False
if __name__ == "__main__":
  BarberShopRun()
