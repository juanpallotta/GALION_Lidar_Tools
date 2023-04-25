def replace_between_strings(s, start_str, end_str, replace_str):

    start_index = s.find(start_str)
    end_index   = s.find(end_str) # end_index = s.find(end_str, start_index + len(start_str))
    if start_index == -1 or end_index == -1:
        return s
    return s[:start_index] + replace_str + s[end_index:]

# Example usage:
input_string = "GALION_LALINET_CEILAPOZONE_TEMPLATE_OPERATIONAL.json"
start_substring = "TEMPLATE"
end_substring = ".json"
replacement = "20150425"
modified_string = replace_between_strings(input_string, start_substring, end_substring, replacement)
print(input_string)
print(modified_string)