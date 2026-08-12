with open("candide.txt", encoding="utf-8") as f:
    text = f.read()

def get_pair_counts(ids: list[int]) -> dict[tuple[int, int], int]:
    counts = {}
    for i in range(len(ids) - 1):
        counts[(ids[i], ids[i+1])] = counts.get((ids[i], ids[i+1]), 0) + 1
    return counts

def merge(ids: list[int], pair: tuple[int, int], new_id: int) -> list[int]:
    new_ids = []
    i = 0
    while i < len(ids) :
        if i < len(ids) - 1 and (ids[i], ids[i+1]) == pair :
            new_ids.append(new_id)
            i += 2
        else:
            new_ids.append(ids[i])
            i += 1
    return new_ids

def train_bpe(ids: list[int], num_merges: int):
    ids = list(ids) 
    merges = {}  

    for i in range(num_merges):
        counts = get_pair_counts(ids)
        if not counts:
            break  

        best_pair = max(counts, key=counts.get)
        new_id = 256 + i
        ids = merge(ids, best_pair, new_id)
        merges[best_pair] = new_id

        print(f"merge {i+1}/{num_merges}: {best_pair} -> {new_id} (freq={counts[best_pair]})")

    return ids, merges

def build_vocab(merges: dict[tuple[int, int], int]) -> dict[int, bytes]:
    vocab = {idx: bytes([idx]) for idx in range(256)}
    for pair, new_id in merges.items():
        vocab[new_id] = vocab[pair[0]] + vocab[pair[1]]
    return vocab

def decode(ids: list[int], vocab: dict[int, bytes]) -> str:
    result = b""
    for token_id in ids:
        result += vocab[token_id]
    return result.decode('utf8')

ids = list(text.encode("utf-8"))
final_ids, merges = train_bpe(ids, num_merges=50)

vocab = build_vocab(merges)
print(decode(final_ids[:50], vocab))