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
    return devices

''' Formatting script.txt into list to send config commands to device '''
def reformat_script(script):
    script = script.read()
    script = script.strip().splitlines()
    return script

''' Common exceptions that could cause issues'''
exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
              netmiko.ssh_exception.NetMikoAuthenticationException)

print('~'*79)
print('~'*30+' Cisco Script Push '+'~'*30)
print('~'*79)
''' Get Variables '''
username = input('Enter TACACS+ Username: ')
password = define_password()
devices = open('.\\devices\\devices.txt','r')
devices = reformat_devices(devices)
script = open('.\\script\\script.txt','r')
script = reformat_script(script)
device_type = 'cisco_ios'
''' Loop for devices '''
for device in devices:
    try:
        ''' Connection Break '''
        print('*'*79)
        print('Connecting to:',device)
        ''' Connection Handler '''
        connection = netmiko.ConnectHandler(ip=device, device_type=device_type, username=username, password=password)
        ''' Sending config commands to device '''
        connection.send_config_set(script)
        connection.send_command('wr')
        connection.disconnect()
        print('Script has completed for:',device)

    except exceptions as exception_type:
        print('Failed to ', device, exception_type)
