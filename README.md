# Matrix Windows Commander

<div style="display: flex; gap: 10px; justify-content: center;">
  <a href="#opis-po-polsku"><img src="https://upload.wikimedia.org/wikipedia/en/thumb/c/c3/Flag_of_Poland.svg/45px-Flag_of_Poland.svg.png" alt="Polska" title="Polski"></a>
  <a href="#english-description"><img src="https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/45px-Flag_of_the_United_States.svg.png" alt="English" title="English"></a>
</div>

---

## Opis po polsku

**Matrix Windows Commander** to zaawansowane narzędzie napisane w Pythonie z wykorzystaniem PyQt5, które umożliwia przeglądanie i wykonywanie licznych poleceń systemowych Windows w stylu „Matrixa” – zielony tekst na czarnym tle. Program organizuje polecenia w kategorie, prezentuje ich opisy, przykłady użycia oraz informacje o wymaganiach (takich jak uprawnienia administratora). Dodatkowo umożliwia wyświetlanie wyników poleceń w przewijalnych oknach, co ułatwia ich analizę.

### Co program robi:
- **Kategoryzacja poleceń:** Polecenia są pogrupowane według funkcji, takich jak Naprawa systemu, Sieć, Zarządzanie procesami itp.
- **Szczegółowe opisy:** Dla każdej komendy dostępne są opis, przykładowe użycie oraz informacja o wymaganych uprawnieniach.
- **Interakcyjny interfejs:** Program oferuje stylizowany wizerunek „Matrixa” z zielonym tekstem na czarnym tle.
- **Przewijalne okna wyników:** Wyniki wykonania poleceń otwierają się w osobnych oknach z możliwością przewijania.
- **Obsługa błędów:** Program analizuje komunikaty o błędach i sugeruje możliwe rozwiązania, np. uruchomienie programu jako administrator lub bezpośrednie wykonanie polecenia w CMD.

### Wymagania:
- **System operacyjny:** Windows 10/11
- **Python 3.x**
- **PyQt5** – instalacja:
  ```bash
  pip install PyQt5
