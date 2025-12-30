def assign(code_lengths: dict[int, int]) -> dict[int, tuple[int, int]]:
    sorted_chars = sorted(code_lengths, key=lambda char: (code_lengths[char], char))
    code_assignment = {}
    prev_length = 0
    curr_code = 0
    for char in sorted_chars:
        length = code_lengths[char]
        length_diff = length - prev_length
        code = curr_code << length_diff
        code_assignment[char] = (code, length)
        prev_length = length
        curr_code = code + 1
    return code_assignment
