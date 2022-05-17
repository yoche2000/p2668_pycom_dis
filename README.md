# p2668_pycom_dis

This is a project in collaboration with EMSD on IoT Harmonization. This python library is a library for Pycom MCUs to implement IEEE P2668 standards.
Use the website http://iotlab.asuscomm.com:30031/ to generate the DIS (Digital Information System) and store the files in a SD card.
Connect the SD card to the Pycom board, and the library will automatically read it.


1. Generate an P2668 object. The object will be generated using the data in the 2 DIS files.
```
  my2668 = P2668()
```
2. Use following functions to print the DISs of a P2668 object in the output terminal.
```
  >>> my2668.get_phy_dis()
  >>> my2668.get_sen_dis()
```
3. P2668 objects can be printed, or transformed into string. Attributes of the P2668 objects will be printed.
```
  >>> print(my2668)
```
4. Using the connect() method will try to connect the Pycom board to the network servers. The data in to Pysical DIS has to be valid to successfully connect the pycom Board to the server.
```
  my2668.connect()
```
5. After connecting P2668 objects, the LoRa socket will be stored in the "socket" attribute of the object. It can be used to send messages and receive messages.

```
  ##Example program: Send the message "test" every 30 seconds to the network server.
  
  while True:
      payload = b'test'
      my2668.socket.send(payload)
      time.sleep(30)
```




