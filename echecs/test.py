import screeninfo as si

for m in si.get_monitors():
    print(f"{m.width}x{m.height}")