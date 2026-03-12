#!/usr/bin/env python3
import random
import json
from datetime import datetime
from collections import Counter

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

FORWARD_WORDS = {
    "A": ["ASH", "ARC", "AXIS"],
    "B": ["BAND", "BONE", "BURDEN"],
    "C": ["COLD", "CHAIN", "CHAMBER"],
    "D": ["DRIFT", "DUST", "DOMAIN"],
    "E": ["ECHO", "ENTRY", "ENGINE"],
    "F": ["FIELD", "FRAME", "FAULT"],
    "G": ["GATE", "GLASS", "GRACE"],
    "H": ["HUSH", "HALL", "HOLLOW"],
    "I": ["INDEX", "IMAGE", "ISOLATE"],
    "J": ["JUNCTION", "JOURNAL", "JAW"],
    "K": ["KEEP", "KERNEL", "KEY"],
    "L": ["LIGHT", "LAYER", "LOGIC"],
    "M": ["MACHINE", "MEMORY", "MOTION"],
}
FORWARD_WORDS.update({
    "N": ["NODE", "NOISE", "NULL"],
    "O": ["ORDER", "OBJECT", "ORBIT"],
    "P": ["PROCESS", "PULSE", "PANEL"],
    "Q": ["QUERY", "QUIET", "QUARTER"],
    "R": ["RECORD", "ROOM", "RETURN"],
    "S": ["SEAM", "SIGNAL", "STATION"],
    "T": ["TERMINAL", "THRESHOLD", "TRACE"],
    "U": ["UNIT", "UNDER", "UPLINK"],
    "V": ["VECTOR", "VAULT", "VOICE"],
    "W": ["WALL", "WINTER", "WIRE"],
    "X": ["XENON", "XYLEM", "X-ARRAY"],
    "Y": ["YARD", "YIELD", "YOKE"],
    "Z": ["ZONE", "ZERO", "ZAP"],
})

INVERSE_WORDS = {
    "A": ["ARCHIVE", "ALONE", "ACCESS"],
    "B": ["BARRIER", "BENEATH", "BEACON"],
    "C": ["CONTROL", "CIPHER", "CLOSURE"],
    "D": ["DENIAL", "DELAY", "DESCENT"],
    "E": ["EVENT", "ERROR", "EVIDENCE"],
    "F": ["FAILURE", "FORM", "FRACTURE"],
    "G": ["GRANT", "GUARD", "GRID"],
    "H": ["HOLD", "HOST", "HARMONIC"],
    "I": ["INTAKE", "INNER", "INTERVAL"],
    "J": ["JAM", "JET", "JUDGMENT"],
    "K": ["KNOWN", "KEPT", "KINETIC"],
    "L": ["LOCK", "LIMIT", "LIST"],
    "M": ["MARK", "MANUAL", "MIRROR"],
}
INVERSE_WORDS.update({
    "N": ["NOTICE", "NUMBER", "NEXUS"],
    "O": ["OFFSET", "OPERATOR", "OUTPUT"],
    "P": ["PATTERN", "PROTOCOL", "PRESSURE"],
    "Q": ["QUEUE", "QUORUM", "QUIVER"],
    "R": ["REVIEW", "REDACTION", "RANGE"],
    "S": ["SECTOR", "STATIC", "SUMMARY"],
    "T": ["TRANSFER", "TENSION", "TOKEN"],
    "U": ["UNION", "UPDATE", "UNDERLAY"],
    "V": ["VERIFY", "VENT", "VOLUME"],
    "W": ["WATCH", "WITHIN", "WEIGHT"],
    "X": ["X-LOCK", "XENIAL", "XENIALITY"],
    "Y": ["YIELD", "YOKE", "YESTER"],
    "Z": ["ZONE", "ZERO", "ZAP"],
})

SENTENCE_TEMPLATES = [
    "{w1} remains active while {w2} is under review.",
    "{w1} passed beneath the {w2} without notice.",
    "No alarm followed when {w1} approached the {w2}.",
    "{w1} persists, but the {w2} no longer explains itself.",
    "The {w1} recorded movement near the {w2}.",
]

DISCOURSE_TEMPLATES = [
    "{s1} {s2}",
    "{s1} However, {s2}",
    "{s1} Meanwhile, {s2}",
]

def box(title):
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)
class TempleBuilderPlusRuntime:
    def __init__(self, mode="seeded", seed=None):
        self.mode = mode
        self.seed = seed
        self.history = []
        self.trends = Counter()

        if mode == "seeded":
            if seed is None:
                seed = 777
            self.rng = random.Random(seed)
            self.seed = seed
        else:
            self.rng = random.Random()

    def O1(self):
        return {
            "runtime_active": True,
            "state": "constant_state_of_being",
            "range": "infinite_potential"
        }

    def O2(self):
        if self.mode == "chaos":
            return self.rng.randint(1, 9999)
        return self.rng.randint(1, 26)

    def O3(self, value):
        if 1 <= value <= 26:
            return ALPHABET[value - 1]
        return None

    def O4(self, letter):
        if not letter:
            return None
        pool = FORWARD_WORDS.get(letter, [letter])
        if self.mode == "chaos":
            return self._chaos_word(letter, pool)
        return self.rng.choice(pool)

    def O5(self, value):
        if 1 <= value <= 26:
            return 27 - value
        return None

    def O6(self, inverse_value):
        if inverse_value is None:
            return None
        letter = self.O3(inverse_value)
        if not letter:
            return None
        pool = INVERSE_WORDS.get(letter, [letter])
        if self.mode == "chaos":
            return self._chaos_word(letter, pool)
        return self.rng.choice(pool)
    def O7(self, word1, word2):
        if self.mode == "chaos":
            return self._chaos_sentence(word1, word2)
        template = self.rng.choice(SENTENCE_TEMPLATES)
        return template.format(w1=word1.lower(), w2=word2.lower())

    def O8(self, sentence1, sentence2):
        if self.mode == "chaos":
            return self._chaos_discourse(sentence1, sentence2)
        template = self.rng.choice(DISCOURSE_TEMPLATES)
        return template.format(s1=sentence1, s2=sentence2)

    def O9(self, output):
        words = output.replace(".", "").replace(",", "").replace("|", "").replace("/", "").split()
        length = len(words)
        has_repeat = len(words) != len(set(words))
        if self.mode == "chaos":
            verdict = "unstable"
        elif length >= 8:
            verdict = "coherent"
        else:
            verdict = "minimal"
        return {
            "word_count": length,
            "repetition_detected": has_repeat,
            "verdict": verdict
        }

    def O10(self, record):
        self.history.append(record)
        self.trends[record["o3_letter"] or "NONE"] += 1
        self.trends[record["o9"]["verdict"]] += 1
        return dict(self.trends)

    def _fallback_fragment(self):
        parts = [
            "signal without source",
            "unindexed remainder",
            "cold recursion",
            "manual review pending",
            "residual process"
        ]
        return self.rng.choice(parts)
    def _chaos_word(self, letter, pool):
        base = self.rng.choice(pool)
        fragments = [
            base,
            letter,
            base[: max(1, len(base)//2)],
            base[::-1],
            "NULL",
            "VOID",
            "ECHO",
        ]
        count = self.rng.randint(2, 4)
        return "-".join(self.rng.choice(fragments) for _ in range(count))

    def _chaos_sentence(self, word1, word2):
        patterns = [
            f"{word1}. {word2}. no witness remained.",
            f"{word1} approached {word2} and returned incomplete.",
            f"{word1} // {word2} // repeat until review.",
            f"not {word1}, not {word2}, still active.",
        ]
        return self.rng.choice(patterns)

    def _chaos_discourse(self, sentence1, sentence2):
        joiners = [" ", " // ", " ... ", " | "]
        return sentence1 + self.rng.choice(joiners) + sentence2

    def generate(self):
        state = self.O1()
        discrete = self.O2()
        letter = self.O3(discrete)
        inverse_value = self.O5(discrete)

        if letter:
            word1 = self.O4(letter)
            word2 = self.O6(inverse_value)
        else:
            word1 = self._fallback_fragment()
            word2 = self._fallback_fragment()

        sentence1 = self.O7(word1, word2)
        discrete2 = self.O2()
        letter2 = self.O3(discrete2)
        inverse_value2 = self.O5(discrete2)

        if letter2:
            word3 = self.O4(letter2)
            word4 = self.O6(inverse_value2)
        else:
            word3 = self._fallback_fragment()
            word4 = self._fallback_fragment()

        sentence2 = self.O7(word3, word4)
        discourse = self.O8(sentence1, sentence2)
        evaluation = self.O9(discourse)

        record = {
            "timestamp": int(datetime.utcnow().timestamp()),
            "module": "TempleBuilderPlus",
            "mode": self.mode,
            "seed": self.seed,
            "o1": state,
            "o2_value": discrete,
            "o3_letter": letter,
            "o4_word": word1,
            "o5_inverse_value": inverse_value,
            "o6_word": word2,
            "o7_sentence_1": sentence1,
            "o7_sentence_2": sentence2,
            "o8_discourse": discourse,
            "o9": evaluation
        }
        record["o10_trends"] = self.O10(record)
        return record
def print_record(record):
    box("TEMPLEBUILDERPLUS OUTPUT")
    print("mode:", record["mode"])
    print("seed:", record["seed"])
    print("O2:", record["o2_value"])
    print("O3:", record["o3_letter"])
    print("O4:", record["o4_word"])
    print("O5:", record["o5_inverse_value"])
    print("O6:", record["o6_word"])
    print()
    print("O7 sentence 1:")
    print(record["o7_sentence_1"])
    print()
    print("O7 sentence 2:")
    print(record["o7_sentence_2"])
    print()
    print("O8 discourse:")
    print(record["o8_discourse"])
    print()
    print("O9 evaluation:")
    print(json.dumps(record["o9"], indent=2))
    print()
    print("O10 trends:")
    print(json.dumps(record["o10_trends"], indent=2))
    print()
def save_record(record):
    ts = int(datetime.utcnow().timestamp())
    out = f"/root/lucentghost/saves/templebuilderplus_{ts}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    print("saved:", out)
    print()

def main():
    box("TEMPLEBUILDERPLUS")
    print("[1] seeded")
    print("[2] guided")
    print("[3] chaos")
    mode_choice = input("Select mode: ").strip()

    if mode_choice == "1":
        mode = "seeded"
        seed_text = input("Enter seed integer: ").strip()
        seed = int(seed_text) if seed_text else 777
    elif mode_choice == "2":
        mode = "guided"
        seed = None
    else:
        mode = "chaos"
        seed = None

    runtime = TempleBuilderPlusRuntime(mode=mode, seed=seed)

    while True:
        record = runtime.generate()
        print_record(record)
        cmd = input("[Enter] again | [s] save | [q] quit: ").strip().lower()
        if cmd == "q":
            break
        if cmd == "s":
            save_record(record)

if __name__ == "__main__":
    main()
