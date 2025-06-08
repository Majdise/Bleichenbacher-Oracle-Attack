# Bleichenbacher Attack Project

In modern cryptography, RSA encryption remains one of the most
widely used algorithms for securing communications. However, like
any cryptographic method, RSA is vulnerable to certain attacks,
particularly when poorly implemented or improperly configured.
One of the most significant vulnerabilities in RSA is the padding
oracle attack, specifically the Bleichenbacher attack, which exploits
weak validation of RSA padding during decryption. This type of
vulnerability can allow attackers to decrypt sensitive messages
without knowing the private key, potentially compromising entire
systems that rely on RSA for encryption.
The focus of this project is to explore the Bleichenbacher attack,
which demonstrates how an attacker can leverage such vulnerabilities
to break encrypted messages. To provide a deeper understanding
and enhance the practical value of this attack, our work
goes beyond the original implementation by incorporating three
optimizations that improve the efficiency and success of the attack.
Additionally, we introduce a noisy oracle, simulating more realistic,
real-world conditions where encryption systems often introduce
noise to hinder attackers.
We have developed a Capture the Flag (CTF) challenge centered
around the Bleichenbacher attack. This CTF allows participants to
engage with the attack hands-on, gaining insight into its workings
and the challenges associated with countering such vulnerabilities.
Through this project, we aim to provide a practical demonstration
of how these vulnerabilities can be exploited.

---

## 📁 Project Structure

The project is divided into two main libraries:

### 1. `attack` Library

Implements the Bleichenbacher attack in several forms:

- **Basic Attack**
- **Optimized Version**
- **Bad Version Oracle (BVO)**
- **Noisy Oracle (and countermeasures)**
- **OAEP Oracle Attack**

Also includes:
- Home-made RSA implementation
- PKCS#1 and SPKCS padding schemes

#### Optimizations Implemented:
- OAEP handling
- Parallel threading
- Trimmers
- Skipping-holes logic

#### Oracles Implemented:
- Bad Version Oracle (BVO)
- Noisy Oracle
- OAEP Oracle

---

## ▶️ Running the Attack Library

**Basic / Optimized / Noisy Versions:**

1. Run `Server.py`
2. Then run `Attacker_<version>.py` (replace `<version>` with `basic`, `opt`, or `noisy`)

**BVO Version:**

1. Run `Server_BVO.py`
2. Then run `Attacker_robin.py`

**OAEP Version:**

1. Run `Server_OAEP.py`
2. Then run `Attacker_OAEP.py`

⚠️ Note: Run files in the exact stated order.

---

## 🧪 Example Run Instructions (Translated Highlights)

- Choose a secret in the server script
- Set oracle strictness (noisy or regular)
- Run the attacker script and observe the attack progress and convergence
- Final output shows recovered secret and live progress updates

---

## 🔗 Resources

- All required files for players: attached, see **levels_explanation** folder.

---

## 🎯 CTF Library

### Leaked Message (`leaked_message.bin`)
For Level 0, players get a file encrypted with a Caesar cipher. Players are expected to extract the string using the `strings` utility and decipher it.

### Interface

- `ctf_player.py`: Used by the player to submit flags.
- `ctf_server.py`: Backend run by the operator. Handles flag validation, scoring, and level progression.

### Attackers

- `skeletons/`: Incomplete attack implementations (for player use)
- `solutions/`: Fully implemented versions (reference/solution)

### Servers

Each level has a specific server/player pair. For example:
- `sys1_server.py` → Level 1
- `sys1_player.py` → Level 1 Player Attack Script

> Servers should be kept running persistently and support multiple player connections concurrently.

---

## ⚙️ Additional Notes

- Ensure correct IP and socket settings for each environment.
- Some manual adjustments might be needed depending on the system configuration.

---

## 📂 Project File Structure

Here’s an overview of the key folders and files in the project:

### `attack/`
Contains the full implementations of Bleichenbacher attack variations.

- `Attacker_basic.py`, `Attacker_opt.py`, `Attacker_noisy.py`: Basic, optimized, and noisy oracle attack versions.
- `Attacker_robin.py`: Used for the Bad Version Oracle (BVO) attack.
- `Attacker_OAEP.py`: Specialized OAEP oracle attack.
- `Server.py`, `Server_BVO.py`, `Server_OAEP.py`: Server implementations for corresponding attacker versions.
- `RSA.py`: Custom RSA implementation with PKCS/SPKCS padding.
- `encrypted_message`, `public_key`: Data files for running the attack scenarios.

---

### `ctf/`
Implements the CTF game logic and environment.

#### `attackers/`

- `skeletons/`: Starter code for players.
  - `sys1_player_skeleton.py`, ..., `sys3_player_skeleton.py`: Incomplete player-side attack scripts for each level.
  - `RSA.py`: Simplified RSA module used in these challenges.

- `solutions/`: Full working versions of the attack code (for verification).
  - Includes files like `sys1_player.py`, ..., `sys3_player.py`.

#### `interface/`

- `ctf_player.py`: Player-facing script for flag submission.
- `ctf_server.py`: Central server that verifies flags and handles game progression.
- `RSA.py`: Used by the interface code.

#### `server/`

- Contains server-side files for each CTF level.
- `sys1_server.py`, ..., `sys3_server.py`: Corresponding to each level in the game.
- `RSA.py`: Used internally by the level servers.

---

### Other Files

- `leaked_message/`: Folder containing the `leaked_message.bin` file for Level 0 (Caesar cipher challenge).
- `README.md`: This file 😊

---

Each folder is modular and reflects a clear separation of concerns between attack logic, CTF game flow, and educational use for players.
