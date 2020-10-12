# Part 1
def keystream(text, key):
    res = ""
    count_non_alpha = 0
    for i in range(len(text)):
        if not text[i].isalpha():
            res += " "
            count_non_alpha += 1
        else:
            res += key[(i - count_non_alpha) % len(key)]
    return res

def encrypt(plaintext, key):
    keystr = keystream(plaintext, key)
    ciphertext = ""
    for i in range(len(plaintext)):
        if not plaintext[i].isalpha():
            ciphertext += plaintext[i]
            continue
        a = 'A' if plaintext[i].isupper() else 'a'
        char = keystr[i]
        shift = ord(char) - ord('A')
        cipher_char = chr(ord(a) + (ord(plaintext[i]) - ord(a) + shift) % 26)
        ciphertext += cipher_char
    return ciphertext

# main program
plaintext = input()
key = input()
ciphertext = encrypt(plaintext, key)
print(ciphertext)

