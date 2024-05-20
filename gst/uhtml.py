import contextlib


def format_attrs(attrs):
    if not attrs:
        return ""
    return " " + " ".join(f'{k}="{v}"' for k, v in attrs.items())


@contextlib.contextmanager
def write_tag(tag, attrs=None, *, stream):
    print(f"<{tag}{format_attrs(attrs)}>", file=stream)
    yield
    print(f"</{tag}>", file=stream)
