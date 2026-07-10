from operations import encode_message, decode_message
from key_generator import gen_keys

keys = gen_keys()
open_key = keys[0]
private_key = keys[1]

encode_message('message_source.txt','encoded.txt', open_key)
decode_message('encoded.txt','decoded.txt',private_key)

decode_message('message_source.txt','digital_sign.txt', private_key)
encode_message('digital_sign.txt', 'check_truth_sign.txt', open_key)