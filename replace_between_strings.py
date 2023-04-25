def replace_between_strings(s, start_str, end_str, replace_str):
    """
    Replace the substring between two given substrings in a string with a replacement substring.

    :param s: the input string
    :param start_str: the starting substring
    :param end_str: the ending substring
    :param replace_str: the replacement substring
    :return: the modified string
    """
    start_index = s.find(start_str)
    end_index = s.find(end_str, start_index + len(start_str))
    if start_index == -1 or end_index == -1:
        return s
    start_index -= len(start_str)
    return s[:start_index + len(start_str)] + replace_str + s[end_index:]

# Example usage:
input_string = "The quick brown fox jumps over the lazy dog."
start_substring = "quick "
end_substring = " fox"
replacement = "slow "
modified_string = replace_between_strings(input_string, start_substring, end_substring, replacement)
print(input_string)
print(modified_string)