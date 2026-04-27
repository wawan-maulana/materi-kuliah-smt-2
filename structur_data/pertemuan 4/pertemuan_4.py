senjata_set = {"kapak", "pedang", "panah", "keris", "tombak"}
print(senjata_set)

senjata_set.add("busur")
print(senjata_set)

senjata_set.remove("kapak")
print(senjata_set)

senjata_set.discard("senapan")
print(senjata_set)

popped = senjata_set.pop()
print(popped)
print(senjata_set)

print(len(senjata_set))

print("pedang" in senjata_set)
print("kapak" not in senjata_set)

set_a = {"kapak", "pedang", "panah"}
set_b = {"panah", "keris", "busur"}

gabungan = set_a | set_b
print(gabungan)

irisan = set_a & set_b
print(irisan)

selisih = set_a - set_b
print(selisih)

selisih_simetris = set_a ^ set_b
print(selisih_simetris)

set_a.update({"tombak", "keris"})
print(set_a)

set_a.intersection_update(set_b)
print(set_a)

set_c = {"kapak", "pedang"}
set_d = {"kapak", "pedang", "panah", "keris"}

print(set_c.issubset(set_d))
print(set_d.issuperset(set_c))
print(set_c.isdisjoint({"busur", "tombak"}))

set_e = set_d.copy()
print(set_e)

set_e.clear()
print(set_e)

dari_list = set(["kapak", "pedang", "kapak", "panah", "pedang"])
print(dari_list)

dari_tuple = set(("keris", "tombak", "keris"))
print(dari_tuple)

angka = {1, 2, 3, 4, 5, 6}
genap = {x for x in angka if x % 2 == 0}
print(genap)

frozenset_senjata = frozenset({"kapak", "pedang", "panah"})
print(frozenset_senjata)
print("kapak" in frozenset_senjata)

for senjata in {"kapak", "pedang", "panah"}:
    print(senjata)

set_f = {"kapak", "pedang"}
set_g = set_f
set_g.add("panah")
print(set_f)

set_h = set_f.copy()
set_h.add("keris")
print(set_f)
print(set_h)