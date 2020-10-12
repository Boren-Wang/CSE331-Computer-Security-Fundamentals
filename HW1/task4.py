from collections import Counter
from scipy.stats import chisquare
import math

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

# Part 4
def kasiski(ciphertext):
    ciphertext = ''.join([i for i in ciphertext if i.isalpha()]).upper()
    # for all 3-gram
    divisor_count = {}
    searched = []
    for i in range(0, len(ciphertext)):
        str1 = ciphertext[i:i+3]
        if str1 in searched:
            continue
        else:
            searched.append(str1)
        indexes = [i]

        # get the indexes of identical 3-grams
        for j in range(i+1, len(ciphertext), 1):
            str2 = ciphertext[j:j+3]
            # if find an identical 3-gram
            if str1==str2:
                indexes.append(j)

        for j in range(len(indexes)):
            for k in range(j+1, len(indexes)):
                # calculate the distance between two identical 3-grams
                distance = indexes[k] - indexes[j]
                divisors = get_divisors(distance)
                update_count(divisors, divisor_count)
    key_length = 0
    key_length_friedman = friedman(ciphertext)
    if key_length_friedman>2:
        divisor_count[1] = 0
    if key_length_friedman>4:
        divisor_count[2] = 0
    most_common_divisors = dict(Counter(divisor_count).most_common(5))
    indexes_of_coincidence = get_indexes_of_coincidence(ciphertext)

    for divisor in most_common_divisors:
        ic = indexes_of_coincidence[divisor]

    for d in most_common_divisors:
        if indexes_of_coincidence[d]>0.0734 or indexes_of_coincidence[d]<0.06:
            most_common_divisors[d] = 0

    if most_common_divisors=={}:
        return 0

    key_length = max(most_common_divisors, key=most_common_divisors.get)

    return key_length

def get_divisors(num):
    divisors = []
    for i in range(1, int(math.sqrt(num)) + 1):
        if num % i == 0:
            divisors.append(i)
            if num // i != i:
                divisors.append(num // i)
    return divisors

def update_count(divisors, divisor_count):
    for divisor in divisors:
        if divisor<=100:
            if divisor in divisor_count:
                divisor_count[divisor] += 1
            else:
                divisor_count[divisor] = 1

def find_most_common_divisor(divisor_count, start, end): # find the most common divisor from start to end
    most_common_divisor = 0
    max = 0
    for i in range(start, end):
        if divisor_count[i] > max:
            most_common_divisor = i
            max = max
    return most_common_divisor

def friedman(ciphertext):
    ciphertext = ''.join([i for i in ciphertext if i.isalpha()]).upper()
    alpha_table = {}
    for char in ciphertext:
        if char not in alpha_table:
            alpha_table[char] = 1
        else:
            alpha_table[char] += 1

    numerator = 0
    denominator = 0
    total = 0
    for alpha in alpha_table:
        numerator += alpha_table[alpha] * (alpha_table[alpha]-1)
        total += alpha_table[alpha]
    denominator = total * (total-1) # n*(n-1)
    if denominator == 0:
        return 0
    index_of_coincidence = numerator / denominator
    length = (0.027 * total) / ((total - 1) * index_of_coincidence - 0.038 * total + 0.065)
    return length

def get_index_of_coincidence(ciphertext):
    ciphertext = ''.join([i for i in ciphertext if i.isalpha()]).upper()
    alpha_table = {}
    for char in ciphertext:
        if char not in alpha_table:
            alpha_table[char] = 1
        else:
            alpha_table[char] += 1

    numerator = 0
    denominator = 0
    total = 0
    for alpha in alpha_table:
        numerator += alpha_table[alpha] * (alpha_table[alpha] - 1)
        total += alpha_table[alpha]
    denominator = total * (total - 1)  # n*(n-1)
    if denominator == 0:
        return 0
    index_of_coincidence = numerator / denominator
    return index_of_coincidence

def get_indexes_of_coincidence(ciphertext):
    indexes_of_coincidence = {}
    ciphertext = ''.join([i for i in ciphertext if i.isalpha()]).upper()
    upper_bound = min(101, len(ciphertext)+1)
    for i in range(1, upper_bound):
        total = 0
        cosets = get_groups(ciphertext, i)
        for string in cosets:
            ic = get_index_of_coincidence(string)
            total += ic
        avg_ic = total / len(cosets)
        indexes_of_coincidence[i] = avg_ic
    return indexes_of_coincidence

# main program
ciphertext = input()
length = kasiski(ciphertext)
key = part3(ciphertext, length)
print(key)
plaintext = decrypt(ciphertext, key)
print(plaintext)
