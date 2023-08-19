def expand_json(json: dict):
    expanded = {}

    def expand_json_rec(json: dict, parent_key: str):
        for key, value in json.items():
            newkey = parent_key + ';' + key if parent_key else key
            if isinstance(value, dict):
                expand_json_rec(value, newkey)
            else:
                expanded[newkey] = value
    
    expand_json_rec(json, '')
    return expanded

def clean_label(s: str):
    sci = s.rfind(';')
    cleaned = s if sci == -1 else s[sci + 1:]
    cleaned = cleaned.replace('_', ' ').capitalize().replace(' id ', ' ID ')
    if cleaned.endswith(' id'): cleaned = cleaned[:-3] + ' ID'
    return cleaned