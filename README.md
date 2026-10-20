# Wykrywanie osób z RGB i głębi

Minimalne demo laboratoryjne: gotowy YOLO11n-seg wyznacza maski osób na RGB,
a skrypt oblicza medianę poprawnych wartości `depth16` wewnątrz każdej maski.
Osoba przecinająca centralny pas obrazu i znajdująca się poniżej progu
odległości powoduje sygnał `STOP`. Detekcje rysuje Ultralytics `Results.plot()`.
Projekt nie steruje robotem; nie zawiera treningu, śledzenia ani stanu zwalniania.

## Uruchomienie

Python 3.12 i [uv](https://docs.astral.sh/uv/). Instalacja PyTorch dla CPU:

```bash
uv venv --python 3.12
uv pip install --python .venv/bin/python torch torchvision --index-url https://download.pytorch.org/whl/cpu
uv pip install --python .venv/bin/python -r requirements.txt
```

Umieść otrzymane od prowadzącego archiwum w katalogu projektu i rozpakuj
wyłącznie obrazy RGB oraz głębię 16-bitową:

```bash
tar -xzf gow_bottom_part.tar.gz ./out_/imgs ./out_/depth16
.venv/bin/python demo.py
```

Skrypt łączy pliki po numerze, np. `0007_img.png` z `0007_depth.png`.
Nie używa stratnego katalogu `depth/`. Zapisuje `demo.mp4` i wypisuje
liczby detekcji, stany oraz mediany głębi w jednostkach surowych.
Przy pierwszym uruchomieniu pobierze wagi, jeśli nie ma ich lokalnie.

Bez potwierdzonej kalibracji wszystkie klatki mają stan `UNKNOWN`.
Komenda odtwarzająca demonstrację jawnie zakłada wyrównanie RGB–depth
oraz skalę `0.001 m/raw`; próg wynosi 1 m, a korytarz 40% szerokości obrazu:

```bash
.venv/bin/python demo.py --demo-m-per-unit 0.001 --stop-m 1
```

Film oznacza oba założenia. `--help` opisuje pozostałe parametry.
Domyślne 10 FPS to tempo odtwarzania, nie potwierdzona częstotliwość danych.

## Wynik i ograniczenia

Przetworzono 402 pary PNG 424×240. W trybie demonstracyjnym:
138 klatek `STOP`, 216 `NO STOP`, 48 `UNKNOWN`.
Bez założeń: 402 klatki `UNKNOWN`. To liczby stanów, nie pomiar dokładności.

Model wykrywa wiele ujęć od pasa w dół, np. `0160` i `0250`, ale pomija
skrajnie przycięte nogi, np. `0298` i `0312`. Brak etykiet uniemożliwia
podanie accuracy. `NO STOP` dotyczy tylko wykrytych masek i nie potwierdza
wolnego przejazdu; brak detekcji daje `UNKNOWN`.

Nie potwierdzono skali głębi; na nakładkach widać przesunięcia konturów
RGB–depth. Wyniki w metrach i sygnały `STOP` opierają się więc na założeniach
demonstracyjnych. Wartości `0` i `65535` są odrzucane jako konwencja demo,
nie jako potwierdzona specyfikacja czujnika. Brak poprawnej głębi osoby
w korytarzu daje `UNKNOWN`, chyba że inna wykryta osoba powoduje `STOP`.

## Licencja i dane

Własny kod i dokumentacja: [AGPL-3.0-only](LICENSE).
Autorstwo modelu, źródła wag i odrębny status danych opisuje [NOTICE.md](NOTICE.md).
Dane od prowadzącego, wagi i film są ignorowane przez Git i pozostają lokalnie.
