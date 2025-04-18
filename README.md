# PCEA Cipher

A Python-based encryption and decryption algorithm inspired by the rotations of a Professor’s Cube. PCEA (Professor’s Cube Encryption Algorithm) scrambles text into hexadecimal using cube-like moves, dynamic key scheduling, and diffusion. Perfect for exploring custom cryptography or encrypting fun messages!

## Features

- **Encryption & Decryption**:
  - Encrypts any text into a hexadecimal string using a key and customizable rounds.
  - Decrypts the hexadecimal back to the original text with the same key and rounds.
- **Cube-Inspired Moves**:
  - Rotates segments of the text’s ASCII values (like cube faces) based on key-derived binary pairs.
  - Includes right/left rotations and position swaps for scrambling.
- **Dynamic Key Scheduling**:
  - Expands the key into round-specific values for better diffusion.
  - Uses XOR and state mixing to entangle the key with the text.
- **Flexible Rounds**: Adjust the number of encryption rounds (default 10) for varying complexity.
- **Command-Line Interface**: Input plaintext, key, and rounds interactively.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/RbbSukhRkhe/PCEA.git
   cd PCEA
   ```

2. **Ensure Python**: PCEA requires Python 3.6+ and has no external dependencies. Verify your Python version:

   ```bash
   python --version
   ```

3. **Run the Script**: Execute the main script (assumed `pcea.py`):

   ```bash
   python pcea.py
   ```

## Usage

Run the script and follow the prompts to encrypt or decrypt text:

1. **Encrypt**:

   - Enter your plaintext (e.g., `ITEC618`).
   - Provide a key (e.g., `Python`).
   - Specify the number of rounds (e.g., `10`).
   - Output: A hexadecimal string (e.g., `7b4e2f1a9c`).

2. **Decrypt**:

   - Use the same key and rounds to decrypt the hexadecimal back to the original text.

Example:

```bash
$ python pcea.py
Please enter the data to be encrypted: ITEC618
Plaintext key: Python
Please enter the number of rounds: 10
Encrypted text: 7b4e2f1a9c3d5e
Decrypted text: ITEC618
```

## Contributing

Love cryptography? Fork the repo and add your own twists! Ideas for new moves, stronger diffusion, or a GUI interface are welcome. Please include tests and update the README for new features.

1. Fork the project.
2. Create a feature branch (`git checkout -b feature/NewMove`).
3. Commit your changes (`git commit -m 'Add diagonal rotation'`).
4. Push to the branch (`git push origin feature/NewMove`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Note

PCEA is an educational project for learning cryptography, not a production-ready cipher. It’s vulnerable to attacks due to its custom design and lacks formal security proofs. For real-world encryption, use established algorithms like AES.

---

Built with ☕ by Sukhanpreet Singh Dhillon. Try encrypting your name and see what you get!
