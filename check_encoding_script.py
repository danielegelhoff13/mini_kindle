with open("fellowship_paged.txt", "rb") as f:
    data = f.read()

data.decode("ascii")   # should NOT raise an exception
