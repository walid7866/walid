import pexpect

# Connection parameters
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'

# Start SSH session
session = pexpect.spawn(f'ssh {username}@{ip_address}', encoding='utf-8', timeout=20)

# Wait for password prompt
response = session.expect(['Password: ', pexpect.TIMEOUT, pexpect.EOF])

# Check for connection issues
if response != 0:
    print(f"Connection Issue: Can't connect to {ip_address}. Check your credentials and network.")
    exit()

# Enter SSH password
session.sendline(password)
login_response = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

# Check authentication success
if login_response != 0:
    print(f"Login Failed: Incorrect password for {username}. Please try again.")
    exit()

# Enter enable mode
session.sendline('enable')
enable_response = session.expect(['Password: ', pexpect.TIMEOUT, pexpect.EOF])

# Validate access to enable mode
if enable_response != 0:
    print("Access Denied: Unable to enter enable mode. Check your enable password.")
    exit()

# Provide enable password
session.sendline(password_enable)
enable_auth_response = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Confirm entry into enable mode
if enable_auth_response != 0:
    print("Failed to enter enable mode. Double-check your input.")
    exit()

# Switch to configuration mode
session.sendline('configure terminal')
config_response = session.expect([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

# Confirm entry into configuration mode
if config_response != 0:
    print('Error: Unable to access configuration mode. Check your commands.')
    exit()

# Set the hostname
session.sendline('hostname R1')
hostname_response = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

# Verify hostname change
if hostname_response != 0:
    print('Error: Could not set hostname. Please check the command.')
    exit()

# Save the running configuration
session.sendline('end')  # Exit configuration mode
session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
session.sendline('write memory')  # Save the configuration
save_response = session.expect(['Destination filename [running-config]?', pexpect.TIMEOUT, pexpect.EOF])

# Handle the prompt to confirm saving
if save_response == 0:
    session.sendline('')  # Press Enter to confirm
    session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Exit enable mode
session.sendline('exit')
session.sendline('exit')

# Display success message
print('-----------------------------------')
print(f'Successfully connected to: {ip_address}')
print(f'User Logged In: {username}')
print(f'Using Password: {password}')
print('-----------------------------------')

# Close the SSH session
session.close()
