# Import for modbus RTU
import struct
from serial import PARITY_NONE
from serial import Serial
from umodbus.client.serial import rtu as modbus_rtu

# Import for modbus TCP 
import socket
from socket import socket as Socket
from umodbus import conf
from umodbus.client import tcp as modbus_tcp

# List of used device address
_DEVICE_ADDRESS_LIST = []

# List of used serial port for modbus RTU
# Note : Several instrument instances can share the same serialport
_SERIALPORTS_LIST = [] 


# Default value of modbus device id 
_MODBUS_DEVICE_ID_DEFAUlT = 0x00

# Default value of serial port for modbus RTU
_SERIAL_PORT_DEFAUlT = None
_SERIAL_BAUD_DEFAUlT = 9600
_SERIAL_BYTESIZE_DEFAUlT = 8
_SERIAL_PARITY_DEFAUlT = PARITY_NONE
_SERIAL_STOPBIT_DEFAUlT = 1
_SERIAL_TIMEOUT_DEFAUlT = 0.1

# List of socket ip address for modbus TCP
# Note : Several instrument instances can not share the same ip address
_TCP_SOCKET_IP_LIST = []

# Default value of tcp/ip socket for modbus TCP
_TCP_SOCKET_IP_DEFAULT = '10.10.100.254'
_TCP_SOCKET_PORT_DEFAULT = 8899



class device_rtu(Serial):

    def __init__(self):
        """ Initialize modbus RTU object """

        # modbus configuration (default)
        self.device_id  = _MODBUS_DEVICE_ID_DEFAUlT

        # serial port configuration (default) for modbus using pySerial 
        self.serialport = Serial()
        self.serialport.close()
        self.serialport.port = _SERIAL_PORT_DEFAUlT
        self.serialport.baudrate = _SERIAL_BAUD_DEFAUlT
        self.serialport.bytesize = _SERIAL_BYTESIZE_DEFAUlT
        self.serialport.parity  = _SERIAL_PARITY_DEFAUlT
        self.serialport.stopbit = _SERIAL_STOPBIT_DEFAUlT
        self.serialport.timeout = _SERIAL_TIMEOUT_DEFAUlT # in second
        

    def config(self, device_id=_MODBUS_DEVICE_ID_DEFAUlT, port=_SERIAL_PORT_DEFAUlT, 
                     baudrate=_SERIAL_BAUD_DEFAUlT, 
                     bytesize=_SERIAL_BYTESIZE_DEFAUlT, 
                     parity=_SERIAL_PARITY_DEFAUlT, 
                     stopbit=_SERIAL_STOPBIT_DEFAUlT, 
                     timeout=_SERIAL_TIMEOUT_DEFAUlT):
        
        """ Config modbus RTU device. 
            Example, device address (or ID), 
                     serial port configuration for modbus RTU device 
            
            Argument :
            device_id (int)  : Modbus device address number
            port (string)    : Serial port (or comport) of client device which will be used with modbus device, Example, "COM5", "COM14" etc.
            baudrate (int)   : Baudrate of serial communication for modbus RTU. Example, 4800, 9600, 19200 etc.
            bytesize (int)   : Byte-size of serial communication. Normally, it should be 8-bit per byte
            parity (char)    : Parity of serial comm. Use these defines in file " serial.py". 
                               => PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
            stopbit (int)    : Stopbit of serial comm. Can be 1, 1.5, 2 bit(s)
            timeout (float)  : Timeout of serial comm. in second. Example, 0.1 = 100 msec
        """
        
        # modbus configuration
        self.device_id  = device_id

        # serial port configuration
        self.serialport.port = port
        self.serialport.baudrate = baudrate
        self.serialport.bytesize = bytesize 
        self.serialport.parity   = parity
        self.serialport.stopbit  = stopbit
        self.serialport.timeout  = timeout # in second

        # open serial port     
        try:  
            if not self.serialport.is_open:
                self.serialport.open()
            # A struct with configuration for serial port.
            # Uncomment this section when use in linux OS.
            #serial_rs485 = struct.pack('hhhhhhhh', 1, 0, 0, 0, 0, 0, 0, 0)
            #fh = port.fileno() 
            #fcntl.ioctl(fh, 0x542F, serial_rs485)

        except Exception as e:
            print("Error from serial port config...")
            print(e)
        
        # Print a configuration status
        print("configuration completed.")
        if port not in _SERIALPORTS_LIST:
            _SERIALPORTS_LIST.append(port)
        else:
            print("Warning : More than 1 device are sharing the same serial port")

        if device_id not in _DEVICE_ADDRESS_LIST:
            _DEVICE_ADDRESS_LIST.append(device_id)
        else:
            print("Warning : More than 1 device are using the same address! Please use another device address.")


    def write_coil(self, coil_address, write_value):
        """ Modbus command : write single coil data (function code = 05)

            @Argument :
            coil_address (int16) : Coil address where to write a coil data
            write_value (int)    : write value
        """

        # Generate modbus RTU message
        message = modbus_rtu.write_single_coil(slave_id=self.device_id, address=coil_address, value=write_value)

        # Send message via serial port
        if self.serialport.is_open:
            response = modbus_rtu.send_message(message, self.serialport)
            print("response={}".format(response))
        else:
            print("Cannot send data. Serial port is closed.")


    def write_register(self, register_address, write_value):
        """ Modbus command : Write data to single register (function code = 06)

            Argument :
            register_address (int16) : Address where to write a data
            write_value (int16)      : Write data 
        """

        # Generate modbus RTU message
        message = modbus_rtu.write_single_register(slave_id=self.device_id, address=register_address, value=write_value)

        # Send message via serial port
        if self.serialport.is_open:
            response = modbus_rtu.send_message(message, self.serialport)
            print("response={}".format(response))
        else:
            print("Cannot send data. Serial port is closed.")


    def write_registers(self, start_register_address, write_values):
        """ Modbus command : Write data to multiple registers (function code = 16)

            Argument :
            start_register_address (int16) : Start address where to write a data
            write_values (int16)           : Write data(s) 
        """

        # Generate modbus RTU message
        message = modbus_rtu.write_multiple_registers(slave_id=self.device_id, starting_address=start_register_address, values=write_values)

        # Send message via serial port
        if self.serialport.is_open:
            response = modbus_rtu.send_message(message, self.serialport)
            print("response={}".format(response))
        else:
            print("Cannot send data. Serial port is closed.")


    def read_coils(self, start_coil_address, number_of_coil):
        """ Modbus command : Read coil data(s) (function code = 01)

            @Argument :
            start_coil_address (int16) : Start coil address where to read a coil data
            number_of_coil (int)       : number of coil(s) to read

            @Return :
            response : Coil data (Byte)
                        The coils in the response message are packed as one coil per bit of the
                        data field. Status is indicated as 1= ON and 0= OFF.
        """

        # Generate modbus RTU message
        message = modbus_rtu.read_coils(slave_id=self.device_id, starting_address=start_coil_address, quantity=number_of_coil)

        # Send message via serial port
        if self.serialport.is_open:
            response = modbus_rtu.send_message(message, self.serialport)
            print("response={}".format(response))
        else:
            print("Cannot send data. Serial port is closed.")
        
        return response
        

    def read_holding_registers(self, start_register_address, number_of_registers):
        """ Modbus command : Read data to holding registers (function code = 03)

            @Argument :
            start_register_address (int16) : Start address where to read a data
            number_of_registers (int)      : number of register(s) in register-line where to read a data

            @Return :
            response : Read data(s). Return as list of read data (sequently) if number_of_register > 1
        """

        # Generate modbus RTU message
        message = modbus_rtu.read_holding_registers(slave_id=self.device_id, starting_address=start_register_address, quantity=number_of_registers)

        # Send message via serial port
        if self.serialport.is_open:
            response = modbus_rtu.send_message(message, self.serialport)
            print("response={}".format(response))
        else:
            print("Cannot send data. Serial port is closed.")
    
        return response


    def read_input_registers(self, start_register_address, number_of_registers):
        """ Modbus command : Read data to input registers (function code = 04)

            @Argument :
            start_register_address (int16) : Start address where to read a data
            number_of_registers (int)      : number of register(s) in register-line where to read a data

            @Return :
            response : Read data(s). Return as list of read data (sequently) if number_of_register > 1
        """

        # Generate modbus RTU message
        message = modbus_rtu.read_input_registers(slave_id=self.device_id, starting_address=start_register_address, quantity=number_of_registers)

        # Send message via serial port
        if self.serialport.is_open:
            response = modbus_rtu.send_message(message, self.serialport)
            print("response={}".format(response))
        else:
            print("Cannot send data. Serial port is closed.")
        
        return response



class device_tcp(Socket):
    
    def __init__(self):
        """ Initialize modbus TCP object """

        # modbus configuration (default)
        self.device_id  = _MODBUS_DEVICE_ID_DEFAUlT

        # TCP socket configuration (default) for modbus 
        self.tcp_socket = None
        self.socket_ip   = _TCP_SOCKET_IP_DEFAULT
        self.socket_port = _TCP_SOCKET_PORT_DEFAULT
    

    def config(self, device_id=_MODBUS_DEVICE_ID_DEFAUlT, socket_ip=_TCP_SOCKET_IP_DEFAULT, socket_port=_TCP_SOCKET_PORT_DEFAULT):
        """ Config modbus TCP device. 
            Example, device address (or ID), 
                     tcp socket configuration for modbus TCP device 
            
            Argument :
            device_id (int)  : Modbus device address number
            socket_ip (string)  : Socket IP number, Example, '192.168.1.1'.
            socket_port (int)   : Socket Port number. Example, 502.
        """
        self.device_id = device_id
        self.socket_ip   = socket_ip
        self.socket_port = socket_port

        # Print a configuration status
        print("configuration completed.")
        if socket_ip not in _TCP_SOCKET_IP_LIST:
            _TCP_SOCKET_IP_LIST.append(socket_ip)
        else:
            print("Warning : More than 1 device are sharing the same ip address. Please use another ip address.")

        if device_id not in _DEVICE_ADDRESS_LIST:
            _DEVICE_ADDRESS_LIST.append(device_id)
        else:
            print("Warning : More than 1 device are using the same device address! Please use another device address.")


    def _connect(self):
        """ Connect TCP socket to modbus device """
        # connect tcp socket to remote IP address of modbus device   
        try:  
            self.tcp_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.connect((self.socket_ip, self.socket_port))

        except Exception as e:
            print("Error during socket connection...")
            print(e)
    

    def _disconnect(self):
        """ Disconnect TCP socket from modbus device """
        # disconnect TCP socket from remote IP address of modbus device   
        try:  
            self.tcp_socket.close()

        except Exception as e:
            print("Error during socket disconnection...")
            print(e)
    

    def write_coil(self, coil_address, write_value):
        """ Modbus command : write single coil data (function code = 05)

            @Argument :
            coil_address (int16) : Coil address where to write a coil data
            write_value (int)    : write value
        """
        # Generate modbus TCP message
        message = modbus_tcp.write_single_coil(slave_id=self.device_id, address=coil_address, value=write_value)

        # Send message via TCP socket
        self._connect()
        response = modbus_tcp.send_message(message, self.tcp_socket)
        print("response={}".format(response))
        self._disconnect()


    def write_register(self, register_address, write_value):
        """ Modbus command : Write data to single register (function code = 06)

            Argument :
            register_address (int16) : Address where to write a data
            write_value (int16)      : Write data 
        """
        # Generate modbus TCP message
        message = modbus_tcp.write_single_register(slave_id=self.device_id, address=register_address, value=write_value)

        # Send message via TCP socket
        self._connect()
        response = modbus_tcp.send_message(message, self.tcp_socket)
        print("response={}".format(response))
        self._disconnect()


    def write_registers(self, start_register_address, write_values):
        """ Modbus command : Write data to multiple registers (function code = 16)

            Argument :
            start_register_address (int16) : Start address where to write a data
            write_values (int16)           : Write data(s) 
        """

        # Generate modbus TCP message
        message = modbus_tcp.write_multiple_registers(slave_id=self.device_id, starting_address=start_register_address, values=write_values)

        # Send message via TCP socket
        self._connect()
        response = modbus_tcp.send_message(message, self.tcp_socket)
        print("response={}".format(response))
        self._disconnect()

        
    def read_coils(self, start_coil_address, number_of_coil):
        """ Modbus command : Read coil data(s) (function code = 01)

            @Argument :
            start_coil_address (int16) : Start coil address where to read a coil data
            number_of_coil (int)       : number of coil(s) to read

            @Return :
            response : Coil data (Byte)
                        The coils in the response message are packed as one coil per bit of the
                        data field. Status is indicated as 1= ON and 0= OFF.
        """

        # Generate modbus TCP message
        message = modbus_tcp.read_coils(slave_id=self.device_id, starting_address=start_coil_address, quantity=number_of_coil)

        # Send message via TCP socket
        self._connect()
        response = modbus_tcp.send_message(message, self.tcp_socket)
        print("response={}".format(response))
        self._disconnect()

        return response
        

    def read_holding_registers(self, start_register_address, number_of_registers):
        """ Modbus command : Read data to holding registers (function code = 03)

            @Argument :
            start_register_address (int16) : Start address where to read a data
            number_of_registers (int)      : number of register(s) in register-line where to read a data

            @Return :
            response : Read data(s). Return as list of read data (sequently) if number_of_register > 1
        """

        # Generate modbus RTU message
        message = modbus_tcp.read_holding_registers(slave_id=self.device_id, starting_address=start_register_address, quantity=number_of_registers)

        # Send message via TCP socket
        self._connect()
        response = modbus_tcp.send_message(message, self.tcp_socket)
        print("response={}".format(response))
        self._disconnect()
    
        return response


    def read_input_registers(self, start_register_address, number_of_registers):
        """ Modbus command : Read data to input registers (function code = 04)

            @Argument :
            start_register_address (int16) : Start address where to read a data
            number_of_registers (int)      : number of register(s) in register-line where to read a data

            @Return :
            response : Read data(s). Return as list of read data (sequently) if number_of_register > 1
        """

        # Generate modbus RTU message
        message = modbus_tcp.read_input_registers(slave_id=self.device_id, starting_address=start_register_address, quantity=number_of_registers)

        # Send message via TCP socket
        self._connect()
        response = modbus_tcp.send_message(message, self.tcp_socket)
        print("response={}".format(response))
        self._disconnect()
        
        return response


    

    
