# Autorstwo i zakres licencji

Kod integracji i dokumentacja: Copyright (c) 2026 Jan Iłowski.
Licencja: GNU Affero General Public License, wyłącznie wersja 3
(`AGPL-3.0-only`); pełny tekst w [LICENSE](LICENSE).

## Model i biblioteki

Detekcję oraz segmentację wykonuje gotowy **YOLO11n-seg autorstwa Ultralytics**.
Ten projekt nie jest autorem modelu ani jego wag. Nie prowadzono treningu
ani dostrajania; własny kod łączy wyniki modelu z głębią i regułą alarmu.

- Źródło biblioteki: https://github.com/ultralytics/ultralytics
- Wagi: https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n-seg.pt
- Warunki Ultralytics: https://www.ultralytics.com/license

Ultralytics udostępnia bibliotekę i gotowe modele w wariancie AGPL-3.0
oraz oferuje odrębne licencjonowanie Enterprise. Projekt korzysta z wariantu
AGPL. Wagi nie są wersjonowane; biblioteka pobiera je przy pierwszym uruchomieniu,
jeżeli nie ma lokalnej kopii. SHA-256 użytej kopii `yolo11n-seg.pt`:

```text
55ed65c56c91713d23e8402371c6c49a6fd84f257f7dce452e8d70e41dcbe152
```

Zależności instalowane osobno zachowują własne licencje, zawarte w ich
dystrybucjach. Licencja tego repozytorium nie zastępuje ich warunków.

## Dane od prowadzącego i film

Archiwum `gow_bottom_part.tar.gz` zostało przekazane przez prowadzącego
do ćwiczenia. Nie otrzymano z nim informacji o autorstwie ani warunkach
dalszego rozpowszechniania. Samo przekazanie danych nie oznacza udzielenia
licencji na ich publikację.

Archiwum, katalog `out_/`, obrazy i filmy wynikowe, w tym `demo.mp4`,
pozostają poza Gitem. Licencja projektu nie nadaje praw do tych materiałów.
Przed ich dalszym udostępnieniem należy ustalić uprawnienia z posiadaczami
praw. Udostępnienie przez prowadzącego wskazuje źródło otrzymanej kopii,
nie przesądza o tym, kto jest właścicielem praw.

Dane wykorzystano wyłącznie jako wejście do inferencji i demonstracji,
bez trenowania modelu. SHA-256 otrzymanego archiwum:

```text
e6609a0220f4c3e3e8fd8728f6e5dd2be1e4346bca99cef50e96db1b6af997c3
```
