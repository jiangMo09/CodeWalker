def find_keys_containing(data, search_string, case_sensitive=False):
    result = []

    for item in data:
        if "key" in item:
            key = item["key"]
            if not case_sensitive:
                key = key.lower()
                search_string = search_string.lower()

            if search_string in key:
                result.append(item)

    return result
