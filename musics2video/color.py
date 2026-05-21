RESET = "\033[0m"

def _wrap(code: str, text: str):
    return f"{code}{text}{RESET}"

def red(text: str):
    return _wrap("\033[31m", text)

def yello(text: str):
    return _wrap("\033[33m", text)

def blue(text: str):
    return _wrap("\033[34m", text)

def cyan(text: str):
    return _wrap("\033[36m", text)
