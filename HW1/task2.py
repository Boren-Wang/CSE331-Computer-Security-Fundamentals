# Part 2
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

def decrypt(ciphertext, key):
    if len(key) == 0:
        return ciphertext

    # 1. generate keystream
    keystr = keystream(ciphertext, key)

    plaintext = ""
    # 2. generate plaintext
    for i in range(len(ciphertext)):
        if not ciphertext[i].isalpha():
            plaintext += ciphertext[i]
            continue
        a = 'A' if ciphertext[i].isupper() else 'a'
        char = keystr[i]
        shift = ord(char) - ord('A')
        plain_char = chr(ord(a) + (ord(ciphertext[i]) - ord(a) - shift) % 26)
        plaintext += plain_char
    return plaintext

# main program
ciphertext = input()
key = input()
plaintext = decrypt(ciphertext, key)
print(plaintext)
