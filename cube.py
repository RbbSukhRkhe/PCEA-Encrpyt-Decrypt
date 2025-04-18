def text_to_decimal(text):
    """Convert text to list of ASCII decimal values."""
    return [ord(char) for char in text]


def decimal_to_text(decimals):
    """Convert list of decimal values to text."""
    return ''.join(chr(d % 256) for d in decimals)


def decimal_to_hex(decimals):
    """Convert decimal list to hexadecimal string."""
    return ''.join(f'{d:02x}' for d in decimals)


def hex_to_decimal(hex_str):
    """Convert hexadecimal string to decimal list."""
    return [int(hex_str[i:i + 2], 16) for i in range(0, len(hex_str), 2)]


def rotate_right(arr, start, end):
    """Rotate segment of array right (clockwise)."""
    if start < 0 or end > len(arr) or start >= end:
        return arr
    segment = arr[start:end]
    segment = [segment[-1]] + segment[:-1]
    return arr[:start] + segment + arr[end:]


def rotate_left(arr, start, end):
    """Rotate segment of array left (counterclockwise)."""
    if start < 0 or end > len(arr) or start >= end:
        return arr
    segment = arr[start:end]
    segment = segment[1:] + [segment[0]]
    return arr[:start] + segment + arr[end:]


def swap(arr, pos1, pos2):
    """Swap two positions in the array."""
    arr = arr.copy()
    pos1, pos2 = pos1 % len(arr), pos2 % len(arr)
    arr[pos1], arr[pos2] = arr[pos2], arr[pos1]
    return arr


def initial_cube_turn(state, key):
    """Apply initial rotation based on key sum."""
    key_sum = sum(text_to_decimal(key))
    shift = key_sum % len(state)
    return state[-shift:] + state[:-shift]


def reverse_initial_cube_turn(state, key):
    """Reverse the initial rotation."""
    key_sum = sum(text_to_decimal(key))
    shift = key_sum % len(state)
    return state[shift:] + state[:shift]


def key_to_binary_pairs(key):
    """Convert key to 4-bit binary pairs."""
    key_decimals = text_to_decimal(key)
    key_hex = ''.join(f'{d:02x}' for d in key_decimals)
    key_bin = bin(int(key_hex, 16))[2:].zfill(len(key_hex) * 4)
    padding = (4 - len(key_bin) % 4) % 4
    key_bin += '0' * padding
    return [key_bin[i:i + 4] for i in range(0, len(key_bin), 4)]


def expand_key(key, length, rounds):
    """Generate a more dynamic key schedule for diffusion."""
    key_decimals = text_to_decimal(key)
    key_len = len(key_decimals)
    schedule = []
    for r in range(rounds):
        round_key = []
        seed = sum(key_decimals) + r  # Introduce round dependency
        for i in range(length):
            # Use a simple mixing function for better diffusion
            val = (key_decimals[i % key_len] * 31 + seed + i) % 256
            round_key.append(val)
        schedule.append(round_key)
    return schedule


def apply_diffusion(state, round_key):
    """Apply XOR diffusion with round key."""
    return [s ^ k for s, k in zip(state, round_key)]


def mix_state(state):
    """Mix the entire state for better diffusion (simple substitution layer)."""
    mixed = state.copy()
    for i in range(len(mixed)):
        mixed[i] = (mixed[i] * 17 + mixed[(i - 1) % len(mixed)]) % 256
    return mixed


def reverse_mix_state(state):
    """Reverse the mixing step (approximate inverse)."""
    mixed = state.copy()
    for i in range(len(mixed) - 1, -1, -1):
        prev = mixed[(i - 1) % len(mixed)]
        mixed[i] = ((mixed[i] - prev) * pow(17, -1, 256)) % 256
    return mixed


def apply_move(state, bits, round_num):
    """Apply a single move based on 4-bit pair with round influence."""
    length = len(state)
    # Bit 1: Left half or Right half
    half = length // 2
    start = 0 if bits[0] == '1' else half
    end = half if bits[0] == '1' else length
    # Bit 2: Clockwise or Counterclockwise
    clockwise = bits[1] == '1'
    # Bit 3: Inverse direction
    if bits[2] == '1':
        clockwise = not clockwise
    # Apply rotation with round number influence
    if clockwise:
        state = rotate_right(state, start, end)
    else:
        state = rotate_left(state, start, end)
    # Bit 4: Transpose with round-based positions
    if bits[3] == '1':
        i = (round_num + int(bits, 2)) % length
        state = swap(state, i, (i + 1) % length)
    return state


def reverse_move(state, bits, round_num):
    """Reverse a single move based on 4-bit pair."""
    length = len(state)
    half = length // 2
    start = 0 if bits[0] == '1' else half
    end = half if bits[0] == '1' else length
    # Reverse transpose first
    if bits[3] == '1':
        i = (round_num + int(bits, 2)) % length
        state = swap(state, i, (i + 1) % length)
    # Invert Bit 2 for reverse direction
    clockwise = bits[1] == '0'
    if bits[2] == '1':
        clockwise = not clockwise
    if clockwise:
        state = rotate_right(state, start, end)
    else:
        state = rotate_left(state, start, end)
    return state


def encrypt(plaintext, key, rounds=3):
    """Encrypt plaintext using enhanced PCEA."""
    state = text_to_decimal(plaintext)
    state = initial_cube_turn(state, key)
    binary_pairs = key_to_binary_pairs(key)
    key_schedule = expand_key(key, len(state), rounds)

    for r in range(rounds):
        # Apply moves with round number influence
        for i, bits in enumerate(binary_pairs):
            state = apply_move(state, bits, r)
        # Apply diffusion
        state = apply_diffusion(state, key_schedule[r])
        # Mix the entire state
        state = mix_state(state)

    return decimal_to_hex(state)


def decrypt(ciphertext, key, rounds=3):
    """Decrypt ciphertext using enhanced PCEA."""
    state = hex_to_decimal(ciphertext)
    binary_pairs = key_to_binary_pairs(key)
    key_schedule = expand_key(key, len(state), rounds)

    for r in range(rounds - 1, -1, -1):
        # Reverse mixing
        state = reverse_mix_state(state)
        # Reverse diffusion
        state = apply_diffusion(state, key_schedule[r])
        # Reverse moves
        for i, bits in enumerate(reversed(binary_pairs)):
            state = reverse_move(state, bits, r)

    state = reverse_initial_cube_turn(state, key)
    return decimal_to_text(state)


# Test case
#    plaintext = "ITEC618"
#    key = "Python"
rounds = 10


plaintext = input("Please enter the data to be encryped:")
key = input("Plaintext key: ")
rounds = int(input("Please enter the number to rounds: "))
ciphertext = encrypt(plaintext, key, rounds)
print(f"Encrypted text: {ciphertext}")
print()
print(f"Decrypted text: {decrypt(ciphertext, key, rounds)}")