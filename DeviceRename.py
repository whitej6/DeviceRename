import netmiko
from getpass import getpass

''' User input for password not displayed on screen '''
def define_password():
    password = None
    while not password:
        password = getpass('Enter TACACS+ Password: ')
        passwordverify = getpass('Re-enter TACACS+ Password to Verify: ')
        if not password == passwordverify:
            print('Passwords Did Not Match Please Try Again')
            password = None
    return password

''' Formatting devices.txt into list to be passed to for loop '''
def reformat_devices(devices):
    devices = devices.read()
    devices = devices.strip().splitlines()
    devdict = {}
    for line in devices:
        words = line.split()
        devdict.update({words[0]:words[1]})
    devices = devdict
    return devices

    
''' Common exceptions that could cause issues'''
exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
              netmiko.ssh_exception.NetMikoAuthenticationException)
print('~'*79)
print('~'*26+' Cisco Device Rename Script '+'~'*25)
print('~'*79)
''' Get Variables '''
username = input('Enter TACACS+ Username: ')
password = define_password()
devices = open('.\\devices\\devices.txt','r')
devices = reformat_devices(devices)
device_type = 'cisco_ios'
''' Loop for devices '''
for device in devices:
    try:
        ''' Connection Break '''
        print('*'*79)
        print('Connecting to:',device)
        ''' Connection Handler '''
        connection = netmiko.ConnectHandler(ip=devices[device], device_type=device_type, username=username, password=password)
        ''' Check if hostname is correct '''
        output = connection.send_command(' sh run | in hostname')
        if not device in output:
            print('Updating hostname')
            connection.send_command_timing('config t')
            connection.send_command_timing('hostname '+device)
            connection.send_command_timing('end')
            connection.send_command_timing('write memory')
        else:
            print('Device has correct hostname')
            pass
    except exceptions as exception_type:
        print('Failed to ', device, exception_type)
print('*'*79)

