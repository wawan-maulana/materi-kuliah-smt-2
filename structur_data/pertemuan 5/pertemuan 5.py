senjata_dict = {
    "kapak": 10,
    "pedang": 20,
    "panah": 15,
    "keris": 25,
    "tombak": 30
}
print(senjata_dict)

print(senjata_dict["pedang"])
print(senjata_dict.get("kapak"))
print(senjata_dict.get("senapan", "tidak ada"))

senjata_dict["busur"] = 18
print(senjata_dict)

senjata_dict["kapak"] = 12
print(senjata_dict)

del senjata_dict["panah"]
print(senjata_dict)

popped = senjata_dict.pop("keris")
print(popped)
print(senjata_dict)

popped_last = senjata_dict.popitem()
print(popped_last)
print(senjata_dict)

print(len(senjata_dict))

print("pedang" in senjata_dict)
print("kapak" not in senjata_dict)

print(senjata_dict.keys())
print(senjata_dict.values())
print(senjata_dict.items())

for nama in senjata_dict:
    print(nama)

for nama, damage in senjata_dict.items():
    print(nama, "->", damage)

for damage in senjata_dict.values():
    print(damage)

senjata_dict2 = {
    "tombak": 99,
    "senapan": 50
}
senjata_dict.update(senjata_dict2)
print(senjata_dict)

senjata_copy = senjata_dict.copy()
print(senjata_copy)

senjata_dict.setdefault("perisai", 5)
print(senjata_dict)

senjata_dict.setdefault("pedang", 999)
print(senjata_dict)

keys = ["kapak", "pedang", "panah"]
default_damage = 0
dari_keys = dict.fromkeys(keys, default_damage)
print(dari_keys)

senjata_dict.clear()
print(senjata_dict)

karakter = {
    "nama": "Ksatria",
    "level": 10,
    "senjata": {
        "utama": "pedang",
        "cadangan": "keris"
    },
    "skill": ["tebas", "tusuk", "lempar"]
}
print(karakter["senjata"]["utama"])
print(karakter["skill"][1])

squares = {x: x**2 for x in range(1, 6)}
print(squares)

genap = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(genap)

nilai = {"kapak": 10, "pedang": 20, "panah": 15}
terbalik = {v: k for k, v in nilai.items()}
print(terbalik)

sorted_by_value = dict(sorted(nilai.items(), key=lambda x: x[1]))
print(sorted_by_value)

sorted_by_value_desc = dict(sorted(nilai.items(), key=lambda x: x[1], reverse=True))
print(sorted_by_value_desc)

max_damage = max(nilai, key=nilai.get)
min_damage = min(nilai, key=nilai.get)
print(max_damage)
print(min_damage)

merged = {"kapak": 10} | {"pedang": 20} | {"panah": 15}
print(merged)