from collections import Counter
from scipy.stats import chisquare

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

# Part 3
def part3(ciphertext, key_length):
    key = ""
    ciphertext_alpha = "".join(filter(str.isalpha, ciphertext)).upper()
    groups = get_groups(ciphertext_alpha, key_length)
    for group in groups:
        # found_shift = False
        min_chisq = 100
        min_shift = 0
        for shift in range(26):
            shifted = get_shifted_string(group, shift)
            chisq = chi_square_frequency_analysis(shifted)
            if chisq<min_chisq:
                min_chisq = chisq
                min_shift = shift
        key += chr(ord("A") + min_shift)
    return key

def get_groups(ciphertext_alpha, key_length):
    groups = []
    for i in range(key_length):
        group = ""
        for j in range(i, len(ciphertext_alpha), key_length):
            group += ciphertext_alpha[j]
        groups.append(group)
    return groups

def get_shifted_string(string, shift):
    res = ""
    for s in string:
        res += chr(ord("A")+(ord(s)-ord("A")-shift) % 26)
    return res

def chi_square_frequency_analysis(shifted):
    counter = Counter(shifted)
    length = len(shifted)
    frequency_observed = []

    # Relative Frequencies of Letters in General English Plain text http://cs.wellesley.edu/~fturbak/codman/letterfreq.html
    frequency_expected = [0.0820011, 0.0106581, 0.0344391, 0.0363709, 0.124167, 0.0235145, 0.0181188, 0.0350386,
                          0.0768052, 0.0019984, 0.00393019, 0.0448308, 0.0281775, 0.0764055, 0.0714095, 0.0203171,
                          0.0009325, 0.0668132, 0.0706768, 0.0969225, 0.028777, 0.0124567, 0.0135225, 0.00219824,
                          0.0189182, 0.000599]
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        f = counter[letter] / length
        frequency_observed.append(f)
    chisq, p = chisquare(frequency_observed, f_exp=frequency_expected, ddof=25)
    return chisq

# main program
ciphertext = input()
length = int(input())
key = part3(ciphertext, length)
print(key)
plaintext = decrypt(ciphertext, key)
print(plaintext)