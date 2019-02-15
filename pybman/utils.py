import json

# write given list (results) to file at path
def write_list(path, results):
    print("write list to file", path)
    if type(results[0]) == str:
        with open(path, "w+", encoding="utf8") as f:
            f.write("\n".join(results))
    if type(results[0]) == list:
        with open(path, "w+", encoding="utf8") as f:
            for res in results:
                f.write('"' + '"\n"'.join(res) + '"\n')

# read plain text file
def read_plain_clean(path):
    print("read plain text file", path)
    lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            lines.append(line.strip('\n'))
    return lines

# read json file at path
def read_json(path):
    print("read file", path)
    result = {}
    with open(path,'r',encoding='utf-8') as f:
        result = json.load(f)
    return result

# write given data to json file at path
def write_json(path, data):
    print("write to", path)
    with open(path, 'w', encoding="utf-8") as f:
        s = json.dumps(data, indent=2)
        f.write(s)
    return path
