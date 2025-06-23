import yaml

def load_filters():
    try:
        with open("backend/filters.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {"include": [], "exclude": []}

def is_relevant_process(name, include=None, exclude=None):
    name = name.lower()
    if not name:
        return False
    if exclude and any(name == ex.lower() for ex in exclude):
        return False
    if include and not any(inc.lower() in name for inc in include):
        return False
    return True