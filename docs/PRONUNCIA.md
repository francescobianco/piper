# Pronuncia italiana con Piper: cosa abbiamo imparato

Note raccolte a orecchio, prima nel progetto [speaker](https://github.com/francescobianco/speaker) (la voce di
Claude Code su uno speaker Bluetooth), poi al telefono con Nura
([mynura](https://github.com/francescobianco/mynura), `devices/xiaomi-dandelion`). Voce: `it_IT-paola-medium`.

## Come Piper legge

Il testo diventa fonemi con espeak-ng, poi il modello trasforma i fonemi in audio. Si può intervenire a più livelli:

1. **Impostazioni di lettura** (`config/lettura.json`): velocità (`length_scale`) e pause tra le frasi
   (`sentence_silence`). Effetto immediato.
2. **Dizionario di pronuncia** (`config/pronuncia.tsv`): una parola intera sostituita con una grafia che si
   legge meglio. Costa zero ed è il livello usato per le correzioni chieste a voce.
3. **Regole fonetiche di espeak-ng**: correzioni sistematiche, da ricompilare. Più delicate.
4. **Fine-tuning da un checkpoint**: servono registrazioni trascritte e una scheda grafica, e il checkpoint deve
   avere qualità e frequenza del modello da ottenere. Per l'italiano, a novembre 2026 erano pubblici solo i
   checkpoint di "serena" (media e alta qualità): paola non si può rifinire, si otterrebbe una voce nuova.
5. **Addestramento da zero**: dataset grande e molto calcolo. Non conviene per questi difetti.

Riferimenti: [guida all'addestramento](https://github.com/rhasspy/piper/blob/master/TRAINING.md) e
[checkpoint](https://huggingface.co/datasets/rhasspy/piper-checkpoints/tree/main).

## Velocità e pause

Con `length_scale` 1,25 e 0,35 secondi di pausa tra le frasi la voce è comoda da seguire (speaker). Al telefono
conta anche il tempo di risposta: si può abbassare la velocità per frase senza toccare il dizionario.

## Doppie

Per "coppia" i fonemi di espeak-ng sono giusti (`kˈɔpːia`), ma il modello rende la doppia troppo corta. Misure
indicative della pausa della p, su una prova singola:

| Testo | Fonemi | Pausa |
|---|---|---|
| copia | `kˈɔpia` | circa 20 ms |
| coppia | `kˈɔpːia` | circa 30 ms |
| còp-pia | `kˈɔppˈia` | circa 73 ms |
| còpp-pia | `kˈɔpːpˈia` | circa 99 ms, scelta |

Le grafie senza accento, come `cop-pia`, chiudono la "o": **l'accento serve a mantenerla aperta**.

## Domande

Piper riceve il punto interrogativo, ma la salita finale è modesta: su una domanda con premessa la voce scendeva
di circa un semitono, e sulle parole tronche o inglesi non sale. Al massimo circa due semitoni di salita con un
finale italiano piano. Funziona meglio la domanda diretta e breve, che finisce con una parola italiana piana:
«Vuoi che la pubblichi?».

## Sigle e parole straniere

Le sigle lette lettera per lettera e le parole inglesi sono il caso tipico da dizionario: si scrive come si
pronuncia in italiano (per esempio una sigla con le lettere separate e accentate). Ogni voce nuova va provata con
`bin/pronuncia` e poi ascoltata.

## Correzioni a voce, al telefono

Al telefono con Nura, nella sessione operativa (dopo la parola d'ordine), si può dire a Claude che una parola è
pronunciata male e come dovrebbe suonare. Claude aggiunge o cambia la voce in `config/pronuncia.tsv` (o le
impostazioni in `config/lettura.json`), la prova con `bin/pronuncia`, fa commit e push qui, e il ponte sul PC
copia i file sul telefono: la frase successiva usa già la correzione.
