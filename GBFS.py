from itertools import permutations

# Helper function to convert word to number based on a dictionary of letter to digit mapping
def word_to_number(word, mapping):
    return int(''.join(str(mapping[letter]) for letter in word))

# Greedy Search to solve cryptarithmetic problem
def cryptarithmetic_greedy(word1, word2, operation, result):
    letters = set(word1 + word2 + result)
    if len(letters) > 10:
        return None  # Too many letters for unique digits (only 10 digits available)

    # Generate all possible permutations of digits for the letters
    for perm in permutations(range(10), len(letters)):
        mapping = dict(zip(letters, perm))

        # Check if the first letters of each word don't map to 0
        if mapping[word1[0]] == 0 or mapping[word2[0]] == 0 or mapping[result[0]] == 0:
            continue  # Words cannot have leading zeros

        # Calculate values of the words
        num1 = word_to_number(word1, mapping)
        num2 = word_to_number(word2, mapping)
        num_result = word_to_number(result, mapping)

        # Check if the equation holds
        if operation == '+' and num1 + num2 == num_result:
            return mapping
        elif operation == '-' and num1 - num2 == num_result:
            return mapping
        elif operation == '*' and num1 * num2 == num_result:
            return mapping
        elif operation == '/' and num2 != 0 and num1 / num2 == num_result:
            return mapping

    return None

# Input
word1 = "HOW"
word2 = "MUCH"
operation = "+"
result = "POWER"

# Greedy search solution
solution = cryptarithmetic_greedy(word1, word2, operation, result)
print("Solution using Greedy Search:", solution)
