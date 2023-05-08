import json
import random
import string


json_file_name = ""

# Example usage
with open(f"{json_file_name}.json") as f:
    json_file = json.load(f)


def anonymize_json(json_data):
    
    def gen_random_ints(max_random_int):
        random_ints = []
        for i in range(max_random_int // 4):
            random_int = random.randint(0, max_random_int - 1)
            if random_int not in random_ints: random_ints.append(random_int)
        return random_ints
    
    def replace_pii(value):
        if isinstance(value, str):
            if len(value) <= 3:
                return value
            else:
                random_ints = gen_random_ints(len(value))
                for i in random_ints:
                    try:
                        char = str((int(value[i]) + i) // 10)
                    except:
                        char = random.choice(string.ascii_lowercase) if value[i].isalpha() else value[i]
                    value = value[:i] + char + value[i+1:]
            return value
        elif isinstance(value, str) and "@" in value:
            return ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + "@example.com"
        elif isinstance(value, list):
            print("list", value)
            return [replace_pii(item) for item in value]
        elif isinstance(value, dict):
            for k, v in value.items():
                if 'date' not in k.lower() and 'time' not in k.lower() and 'kg' not in v.lower() and 'lb' not in v.lower() and '2023' not in v:
                    annon_str = ",".join(" ".join(replace_pii(sub2) for sub2 in sub1.split(" ")) for sub1 in v.split(","))
                    value[k] = annon_str
        return value
    
    return replace_pii(json_data)

# printing original json file
print(json.dumps(json_file, indent=4))


anonymized_json = anonymize_json(json_file)

# printing annonymized version
print(json.dumps(anonymized_json, indent=4))

# saving the annonymized version in json_file
with open(f"anonymized_{json_file_name}.json", "w") as f:
    json.dump(anonymized_json, f, indent=2)


