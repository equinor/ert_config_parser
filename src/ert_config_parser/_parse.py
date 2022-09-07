from pathlib import Path
from warnings import warn


def tokenize(line):
    in_string = False
    tokens = []
    current_token = ""
    started_dash = False
    for index in range(len(line)):
        if line[index] == '"':
            started_dash = False
            if current_token:
                tokens.append(current_token)
                current_token = ""
            in_string = not in_string
            continue
        if in_string:
            current_token += line[index]
        else:
            if line[index] == "-":
                if started_dash:
                    current_token = current_token[:-1]
                    break
                else:
                    started_dash = True
            else:
                started_dash = False
            if line[index] == " ":
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += line[index]
    if current_token:
        tokens.append(current_token)

    if in_string:
        raise ValueError("Unmatched quote")
    return tokens


def parse(filename, keywords):
    file_contents = Path(filename).read_text().split("\n")
    results = {}
    for line in file_contents:
        tokens = tokenize(line)
        if not tokens:
            continue
        keyword = tokens[0]
        if keyword in keywords:
            results[keyword] = tokens[1:]
        else:
            warn(f"Unrecognized keyword {keyword}")
    return results
