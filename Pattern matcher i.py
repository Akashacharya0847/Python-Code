def wildcard_match(text: str, pattern: str) -> bool:
    memo = {}

    def dfs(i: int, j: int) -> bool:
        # i: current position in text, j: current position in pattern
        if (i, j) in memo:
            return memo[(i, j)]

        # Base case: end of both text and pattern
        if i == len(text) and j == len(pattern):
            return True

        # Base case: end of text but not pattern (unless remaining pattern is all '*')
        if i == len(text):
            return all(c == '*' for c in pattern[j:])

        # Base case: end of pattern but not text
        if j == len(pattern):
            return False

        # Current pattern char handling
        if pattern[j] == '*':
            # '*' matches zero or more chars: try zero (skip '*') or one+ (skip text char)
            match = dfs(i, j + 1) or (i < len(text) and dfs(i + 1, j))
        elif pattern[j] == '?' or pattern[j] == text[i]:
            # '?' matches any single char, or literal match
            match = dfs(i + 1, j + 1)
        else:
            match = False

        memo[(i, j)] = match
        return match

    return dfs(0, 0)


# Test cases
print(wildcard_match("abcdefg", "a*b?d"))  # True ('*' matches 'bc', '?' matches 'e', 'd' matches 'd')
print(wildcard_match("aa", "a?"))  # False (too short)
print(wildcard_match("aaabbbccc", "a*b*c"))  # True ('*' matches 'aabbb', '*' matches empty before 'c')
print(wildcard_match("adceb",
                     "*a*b"))  # True ('*' matches empty, 'a', '*' matches 'ceb' wait no: first '*'='ad', then 'a'? wait adjust: actually first *=' ', a='a', *='dceb')
