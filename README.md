W GitHub README nie ma natywnej możliwości dynamicznego przełączania języków, ale można zastosować **sekcje rozwijalne** (ang. collapsible sections) za pomocą tagów HTML `<details>` i `<summary>`. Pozwoli to użytkownikowi kliknąć i rozwinąć opis w wybranym języku. Poniżej przedstawiam przykładowy plik **README.md**, który zawiera jednolity opis z możliwością rozwinięcia sekcji w języku polskim i angielskim.

---

```markdown
# Matrix Windows Commander

<div align="center">
  <strong>Wybierz język opisu:</strong>
</div>

<details>
  <summary>🇵🇱 Polski</summary>

## Opis po polsku

**Matrix Windows Commander** to zaawansowane narzędzie stworzone w Pythonie z użyciem PyQt5, które umożliwia przeglądanie i wykonywanie wielu poleceń systemowych Windows w stylu „Matrixa” – zielony tekst na czarnym tle.

### Co program robi:
- **Kategoryzacja poleceń:** Polecenia są pogrupowane według funkcjonalności (np. Naprawa systemu, Sieć, Zarządzanie procesami).
- **Szczegółowe opisy:** Każde polecenie zawiera opis, przykład użycia oraz informację, czy wymaga uprawnień administratora.
- **Interfejs Matrixa:** Estetyczny interfejs z zielonym tekstem na czarnym tle.
- **Przewijalne okna wyników:** Wyniki poleceń są wyświetlane w oddzielnych oknach z możliwością przewijania.
- **Obsługa błędów:** Program analizuje komunikaty o błędach i sugeruje rozwiązania, np. uruchomienie jako administrator lub uruchomienie polecenia w CMD.

### Wymagania:
- **System operacyjny:** Windows 10/11
- **Python 3.x**
- **PyQt5** – instalacja:  
  ```bash
  pip install PyQt5
  ```

</details>

<details>
  <summary>🇺🇸 English</summary>

## English Description

**Matrix Windows Commander** is an advanced tool built with Python and PyQt5 that allows you to browse and execute numerous Windows system commands in a "Matrix" style – green text on a black background.

### What the program does:
- **Command Categorization:** Commands are grouped by functionality (e.g., System Repair, Network, Process Management).
- **Detailed Descriptions:** Each command includes a description, usage example, and information on whether administrator privileges are required.
- **Matrix Style Interface:** A visually appealing interface with green text on a black background.
- **Scrollable Result Windows:** Command outputs are displayed in separate scrollable windows for easy viewing.
- **Error Handling:** The program analyzes error messages and suggests solutions, such as running as administrator or executing the command directly in CMD.

### Requirements:
- **Operating System:** Windows 10/11
- **Python 3.x**
- **PyQt5** – installation:  
  ```bash
  pip install PyQt5
  ```
</details>
```

---

**Instrukcje:**

1. Skopiuj powyższy kod i wklej go do pliku `README.md` w swoim repozytorium GitHub.
2. Po zapisaniu README użytkownicy zobaczą przyciski (flagowe emoji) i tekst „Wybierz język opisu:”. Kliknięcie na daną flagę (sekcję `<summary>`) rozwinie opis w wybranym języku.
3. Dzięki temu opis w języku polskim i angielskim jest w jednym pliku, a użytkownik sam decyduje, którą wersję chce przeczytać.

Ten format README jest przejrzysty, umożliwia rozwijanie sekcji według preferencji językowych i prezentuje najważniejsze informacje o projekcie.
