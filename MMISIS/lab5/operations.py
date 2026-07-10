def message_to_file(filename, message):
    with open(filename, 'w') as file:
        file.write(message)

def encode_message(source,dest, open_key):
    exp, n = open_key
    with open(source, 'r') as file:
        message = int(file.read())
    encoded = pow(message, exp, n)
    message_to_file(dest, str(encoded))
    message_to_file('open_key.txt', str(open_key))

def decode_message(source, dest, private_key):
    dexp, n = private_key
    with open(source, 'r') as file:
        message = int(file.read())
    decoded = pow(message, dexp, n)
    message_to_file(dest, str(decoded))
    message_to_file('private_key.txt', str(private_key))

