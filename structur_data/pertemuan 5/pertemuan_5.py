teks = """
Ksatria itu menghunus pedang dengan gagah.
Pedang itu berkilau di bawah sinar matahari.
Ksatria melangkah maju dengan penuh keberanian.
Keberanian ksatria itu membuat musuh gentar.
Musuh pun mundur karena takut menghadapi ksatria.
"""

teks_bersih = teks.lower().strip()
print(teks_bersih)

kata_kata = teks_bersih.split()
print(kata_kata)

jumlah_kata = len(kata_kata)
print("Jumlah kata:", jumlah_kata)

jumlah_karakter = len(teks)
print("Jumlah karakter (dengan spasi):", jumlah_karakter)

jumlah_karakter_tanpa_spasi = len(teks.replace(" ", "").replace("\n", ""))
print("Jumlah karakter (tanpa spasi):", jumlah_karakter_tanpa_spasi)

jumlah_baris = len([b for b in teks.strip().split("\n") if b.strip()])
print("Jumlah baris:", jumlah_baris)

wordcount = {}
for kata in kata_kata:
    kata = kata.strip(".,!?;:")
    if kata in wordcount:
        wordcount[kata] += 1
    else:
        wordcount[kata] = 1
print(wordcount)

from collections import Counter
wordcount_counter = Counter(kata.strip(".,!?;:") for kata in kata_kata)
print(wordcount_counter)

kata_terbanyak = wordcount_counter.most_common(3)
print("3 kata terbanyak:", kata_terbanyak)

kata_paling_sering = max(wordcount, key=wordcount.get)
print("Kata paling sering:", kata_paling_sering, "->", wordcount[kata_paling_sering])

kata_paling_jarang = min(wordcount, key=wordcount.get)
print("Kata paling jarang:", kata_paling_jarang, "->", wordcount[kata_paling_jarang])

sorted_wordcount = dict(sorted(wordcount.items(), key=lambda x: x[1], reverse=True))
print("Wordcount terurut:", sorted_wordcount)

stopwords = {"itu", "di", "dengan", "pun", "karena", "dan", "yang", "ke", "dari"}
wordcount_filtered = {k: v for k, v in wordcount.items() if k not in stopwords}
print("Wordcount tanpa stopwords:", wordcount_filtered)

kata_unik = set(wordcount.keys())
print("Kata unik:", kata_unik)
print("Jumlah kata unik:", len(kata_unik))

kata_lebih_dari_sekali = {k: v for k, v in wordcount.items() if v > 1}
print("Kata yang muncul lebih dari sekali:", kata_lebih_dari_sekali)

kata_muncul_sekali = {k: v for k, v in wordcount.items() if v == 1}
print("Kata yang hanya muncul sekali:", kata_muncul_sekali)

frekuensi = {}
for kata, jumlah in wordcount.items():
    persen = round((jumlah / jumlah_kata) * 100, 2)
    frekuensi[kata] = str(persen) + "%"
print("Frekuensi kata:", frekuensi)

print("\n===== LAPORAN WORDCOUNT =====")
print(f"Total kata       : {jumlah_kata}")
print(f"Kata unik        : {len(kata_unik)}")
print(f"Total karakter   : {jumlah_karakter_tanpa_spasi}")
print(f"Total baris      : {jumlah_baris}")
print(f"Kata terbanyak   : {kata_paling_sering} ({wordcount[kata_paling_sering]}x)")
print(f"Kata paling jarang: {kata_paling_jarang} ({wordcount[kata_paling_jarang]}x)")
print("=============================")