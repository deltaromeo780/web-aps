import levenshtein


def command_assistant(input_text):
    suggestions = [
       "add", "all", "names", "address", "phone", "email", "birthday", "edit", "delete", "search",
        "show", "good bye", "exit", "close", "help"
    ]
    closest_match = None
    min_distance = float('inf')

    for suggestion in suggestions:
        distance = levenshtein.distance(input_text, suggestion)
        if distance < min_distance:
            min_distance = distance
            good_command = suggestion
    print(f" Bad Command: {input_text}, Correct Command is: {good_command} ")
    return good_command
