Bleichenbacher attack


1 Introduction

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


2 Attack description

In this work we consider the following scenario. Suppose 𝑛, 𝑒 represent
an RSA public key with 𝑑 as its corresponding private key.
An attacker is assumed to have access to an oracle that, given any
ciphertext c, reveals whether the decrypted value 𝑐𝑑 𝑚𝑜𝑑 𝑛 adheres
to the format specified by the PKCS #1.5 standard. We demonstrate
how this oracle can be leveraged to either decrypt a message or
produce a valid signature. By systematically crafting ciphertexts—
each choice informed by previous oracle responses—the attacker
progressively gathers information about 𝑐𝑑 . This approach exemplifies
an adaptive chosen-ciphertext attack, where the attacker
uses the oracle’s partial decryption feedback to gradually reduce
the uncertainty about the plaintext. While conventional chosenciphertext
attacks typically assume that a decryption device outputs
the full plaintext, thereby rendering such attacks mostly a theoretical
concern, the method described here is practical. In real-world
scenarios, for example, when an attacker can interact with a server
that accepts encrypted messages and returns an error message indicating
whether the decryption conforms to PKCS, the attack can
be successfully executed.


3 CTF Design

The CTF is divided into several levels, each exposing the players to
different skills, tools, and ideas:

3.1 Level 0 - Introduction to Our CTF

The goal of this level is to introduce the player to the world of CTF,
present the necessary thinking methods, and familiarize them with
the fact that they will need to search on Google for things they
don’t know.

3.2 Level 1 - Introduction to the Bleichenbacher Attack

The goal of this level is to present the bleichenbacher attack gently
and graduallyto the players. This is accomplished by a comprehensive
guide to the attack, and a code skeleton for the attack, missing
subtle and relevant details for the attack - so the player’s role is to
complete them. Thus, the player is expected to use the guide, and
to learn independently using google and online sources relevant
background needed such as RSA.

3.3 Level 2 - Optimizations to the Bleichenbacher Attack

The goal of each such level is to introduce the player to some
improvement of the attacks efficiency, to address a well known 
bottleneck and overall make the attack more practical. In each
“optimization level” the sole focus is on the contribution the optimization
“brings to the table”.

3.4 Level 3 - Noisy Oracles and How to Deal with Them

The goal of this level is to introduce players to the challenges
that arise when moving from theoretical attacks to real-world implementations.
In particular, it focuses on the concept of noisy
oracles—systems that intentionally introduce noise into responses
to hinder or complicate an In this level, the player is tasked with
dealing with a noisy oracle. Players will need to modify their attack
to account for these inconsistencies, learning how to overcome
noise in order to still recover the plaintext message. By completing
this level, players will better understand the limitations of cryptographic
attacks in real-world scenarios and how attackers must
adapt to countermeasures like noisy oracles.

4 Conclusions

In this project, we explored the Bleichenbacher attack on RSA
encryption, highlighting its significance in cryptographic vulnerabilities,
particularly in padding oracle attacks. Through the implementation
of the original attack, along with three optimizations
to enhance its efficiency, we demonstrated how a seemingly theoretical
vulnerability can be exploited in practice. Additionally, we
introduced the concept of a noisy oracle, simulating a more realistic
environment where attackers face countermeasures designed to
hinder their progress.
The Capture the Flag (CTF) challenge created around this attack
provides an interactive, hands-on learning experience, guiding
participants through different stages of the Bleichenbacher attack
and its optimizations. By designing levels that introduce key concepts
gradually—from understanding the basic attack to dealing
with noisy oracles—players gain a deeper understanding of cryptographic
vulnerabilities and the complexities involved in real-world
security.
Ultimately, this project emphasizes the importance of secure
cryptographic practices and the need for robust countermeasures
against attacks like Bleichenbacher. It also showcases how understanding
and mitigating such vulnerabilities can help strengthen
the security of modern cryptographic systems. Through the CTF,
we hope to have inspired greater awareness and sparked further
exploration into the
