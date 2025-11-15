# ⚡ NightShift — Nuclear Power Plant Horror (Pygame)
Gra powstałą na khackathon HackTheTopo
Niepubliczne Liceum Ogólnokształcące
Autorzy:
Amelia Polna
Paweł Rzodkiewicz
Alan Flis
Maek Kaniewski

**NightShift** to top–down survival–horror tworzony na hackathon.  
Akcja gry odbywa się w opuszczonej elektrowni jądrowej, którą gracz eksploruje, naprawia i zasila… zanim stanie się coś bardzo złego.

Gra powstaje w **Pythonie + Pygame**, z autorską grafiką pixel–art, systemem sprite’ów oraz własnym systemem logiki połączeń energetycznych.

---

## 🎮 Funkcje gry

### ✔️ Top–down movement
- sterowanie **WASD / strzałki**
- animowany sprite gracza (4 kierunki, 3 klatki animacji)
- płynne poruszanie z dt (delta–time)

### ✔️ Budowanie i łączenie obiektów
Gracz może stawiać elementy infrastruktury:
– kabel (można rotować)
- automatyczne wykrywanie połączeń między elementami  
- system obliczania, które elementy otrzymują **zasilanie**

### ✔️ „Ghost mode” – podgląd stawiania obiektu
- obiekt przed postawieniem wyświetlany jest jako zielona/czerwona obwódka  
- kolizje z graczem i innymi obiektami  
- snapowanie kabli do końcówek kabli (magnetyczne łączenie)

### ✔️ Generowane pokoje elektrowni
- losowa generacja layoutu pomieszczeń  
- system ścian (`wall`) budowany z `rooms_assets.py`
- korytarze, pokoje centralne, narożne i skrzyżowania

### ✔️ Uranek — inteligentny narrator
W prawym dolnym rogu ekranu pojawia się **Uranek** – pomocnicza maskotka U-235.  
- podpowiada graczowi (dymki z tekstem)  
- reaguje na akcje (stawianie obiektów, podłączenie prądu, wejście do nowego pokoju itp.)
  

### ✔️ Pixel–art i animacje
- własny sprite gracza (`chodzenie_256.png`)
- pixel-arty obiektów: kable, generatory, elektrownia
- neonowy klimat elektrowni

- Project/
│
├── assets/ # grafiki i pixel–arty
│ ├── chodzenie_256.png
│ ├── triangle.png
│ ├── tall_rect.png
│ ├── long_rect.png
│ └── uranek.png
│
├── main.py # główny plik gry
├── player.py # sprite gracza + animacje
├── objects.py # logika obiektów, prądu, rysowanie
├── ghost.py # logika podglądu i łączenia kabli
├── rooms_assets.py # generowanie pomieszczeń elektrowni
├── walls.py # dodatkowe narzędzia ścian/pokoi
├── menu.py # ekran startowy
├── uranek.py # narrator + dymek z tekstem
└── README.md

