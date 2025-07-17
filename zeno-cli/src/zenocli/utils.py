# This will be for shared functions/helpers

def format_header(title: str) -> str:
    return f"==[ {title} ]" + "=" * (50 - len(title))
