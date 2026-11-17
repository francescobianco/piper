"""Correzioni di pronuncia e impostazioni di lettura per Piper, in italiano.

Il dizionario (config/pronuncia.tsv) sostituisce parole intere con una grafia che Piper legge meglio, per
esempio "coppia" con "còpp-pia". Le impostazioni (config/lettura.json) regolano velocità e pause.
Entrambi i file si rileggono da soli quando cambiano: chi usa questo modulo in un servizio sempre acceso
(la voce al telefono di Nura) prende le correzioni nuove alla frase successiva, senza riavvii.

Uso:
    from pronuncia import Pronuncia
    p = Pronuncia()              # cartella config/ accanto a questo file, oppure Pronuncia('/percorso/config')
    testo = p.correggi(testo)    # applica il dizionario
    p.lettura()                  # {'length_scale': 1.25, 'sentence_silence': 0.35}
    p.sintetizza(voice, testo, wav)   # con un PiperVoice già caricato (piper-tts >= 1.3)
"""
import json
import os
import re

QUI = os.path.dirname(os.path.abspath(__file__))
LETTURA_PREDEFINITA = {'length_scale': 1.0, 'sentence_silence': 0.2}


class Pronuncia:
    def __init__(self, config=None):
        self.config = config or os.path.join(QUI, 'config')
        self.tsv = os.path.join(self.config, 'pronuncia.tsv')
        self.json = os.path.join(self.config, 'lettura.json')
        self._mtime = {}
        self._regole, self._re = {}, None
        self._lettura = dict(LETTURA_PREDEFINITA)
        self.ricarica()

    def _cambiato(self, path):
        try:
            m = os.path.getmtime(path)
        except OSError:
            return False
        if self._mtime.get(path) != m:
            self._mtime[path] = m
            return True
        return False

    def ricarica(self):
        """Rilegge i file se sono cambiati. Restituisce True se qualcosa è cambiato."""
        cambiato = False
        if self._cambiato(self.tsv):
            regole = {}
            with open(self.tsv, encoding='utf-8') as f:
                for riga in f:
                    riga = riga.rstrip('\n')
                    if not riga.strip() or riga.lstrip().startswith('#') or '\t' not in riga:
                        continue
                    k, v = riga.split('\t', 1)
                    if k.strip():
                        regole[k.strip().lower()] = v.strip()
            self._regole = regole
            chiavi = sorted(regole, key=len, reverse=True)
            # Confini di parola anche per voci con punti o cifre (es. "Wi-Fi", "4G")
            self._re = re.compile(r'(?<!\w)(' + '|'.join(map(re.escape, chiavi)) + r')(?!\w)',
                                  re.IGNORECASE) if chiavi else None
            cambiato = True
        if self._cambiato(self.json):
            try:
                with open(self.json, encoding='utf-8') as f:
                    dati = json.load(f)
                self._lettura = {**LETTURA_PREDEFINITA,
                                 **{k: v for k, v in dati.items() if not k.startswith('_')}}
                cambiato = True
            except ValueError:
                pass  # file a metà scrittura o sbagliato: si tiene la versione precedente
        return cambiato

    def correggi(self, testo):
        self.ricarica()
        if not self._re:
            return testo
        return self._re.sub(lambda m: self._regole[m.group(1).lower()], testo)

    def lettura(self):
        self.ricarica()
        return dict(self._lettura)

    def voci(self):
        self.ricarica()
        return dict(self._regole)

    def sintetizza(self, voice, testo, wav_file):
        """Sintetizza con un PiperVoice già caricato, applicando dizionario e impostazioni."""
        from piper import SynthesisConfig
        l = self.lettura()
        cfg = SynthesisConfig(length_scale=l.get('length_scale'))
        voice.synthesize_wav(self.correggi(testo), wav_file, syn_config=cfg,
                             set_wav_format=True)
