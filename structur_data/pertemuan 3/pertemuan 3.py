import sys

senjata = ("kapak", "pedang", "panah")
print(senjata)
print(senjata[1])

senjata2 = []
senjata2.append("tombak")
print(senjata2)
print(senjata2[0])

print(sys.getsizeof(senjata))
print(sys.getsizeof(senjata2))

senjatabackup = senjata
print(senjatabackup)

print(len(senjata))
print(senjata[0])
print(senjata[-1])
print(senjata[0:2])

print("pedang" in senjata)
print("tombak" not in senjata)

print(senjata.count("kapak"))
print(senjata.index("panah"))

print(max(senjata))
print(min(senjata))
print(sorted(senjata))

senjata3 = ("busur", "keris")
gabungan = senjata + senjata3
print(gabungan)

diulang = senjata3 * 2
print(diulang)

for s in senjata:
    print(s)

for index, s in enumerate(senjata):
    print(index, s)

kapak, pedang, panah = senjata
print(kapak)
print(pedang)
print(panah)

pertama, *sisanya = senjata
print(pertama)
print(sisanya)

senjata_list = list(senjata)
senjata_list.append("keris")
senjata_baru = tuple(senjata_list)
print(senjata_baru)

nested = (("kapak", 10), ("pedang", 20), ("panah", 15))
for nama, damage in nested:
    print(nama, damage)

print(senjata == senjatabackup)
print(senjata is senjatabackup)