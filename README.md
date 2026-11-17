# piper

Pronuncia italiana per [Piper](https://github.com/rhasspy/piper): dizionario di correzioni, impostazioni di
lettura e le regole trovate a orecchio con la voce `it_IT-paola-medium`.

Lo usano:
- [speaker](https://github.com/francescobianco/speaker), la voce di Claude Code su uno speaker Bluetooth;
- [mynura](https://github.com/francescobianco/mynura), la voce di Claude al telefono con Nura
  (`devices/xiaomi-dandelion/modem/convo.py`), che rilegge questi file a ogni frase.

## File

```
config/pronuncia.tsv   dizionario: parola<TAB>grafia da leggere
config/lettura.json    velocità (length_scale) e pause tra le frasi (sentence_silence)
pronuncia.py           modulo Python: applica il dizionario e rilegge i file quando cambiano
bin/pronuncia          prova: testo dopo il dizionario e fonemi di espeak-ng
docs/PRONUNCIA.md      cosa abbiamo imparato su doppie, accenti, domande e livelli di intervento
```

## Aggiungere una correzione

1. Una riga in `config/pronuncia.tsv`: `parola<TAB>grafia`, per esempio `coppia	còpp-pia`.
2. Prova: `bin/pronuncia "una coppia di prove"`.
3. Commit e push. Al telefono la correzione vale dalla frase successiva.

```python
from pronuncia import Pronuncia
p = Pronuncia()
p.correggi("una coppia di prove")   # 'una còpp-pia di prove'
```
