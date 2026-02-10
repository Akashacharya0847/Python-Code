from typing import List, Tuple
from functools import lru_cache


def find_dna_motifs(dna: str, motif: str, max_mismatches: int = 2) -> List[Tuple[int, int]]:
    """
    Find all occurrences of motif in DNA allowing up to max_mismatches.
    Returns list of (start_index, mismatch_count) tuples.
    """
    n, m = len(dna), len(motif)
    results = []

    @lru_cache(maxsize=None)
    def min_mismatches(i: int, j: int) -> int:
        """
        Recursive DP: minimum mismatches needed to match dna[i:] with motif[j:].
        Memoized to avoid recomputing repetitive DNA segments.
        """
        # Base cases
        if j == m:  # Finished motif
            return 0
        if i + m - j > n:  # Not enough DNA left
            return float('inf')

        # Current position match/mismatch
        mismatch = 0 if dna[i] == motif[j] else 1

        # Two choices: match current chars OR skip this DNA position (backtrack)
        match_here = mismatch + min_mismatches(i + 1, j + 1)
        skip_dna = min_mismatches(i + 1, j)

        return min(match_here, skip_dna)

    # Scan DNA for valid motif positions
    for start in range(n - m + 1):
        mismatches = min_mismatches(start, 0)
        if mismatches <= max_mismatches:
            results.append((start, mismatches))

    return results


# Test cases
dna = "AGCTTAGCTTAGCTTAGCTTA"
motif = "GATTACA"
max_mismatches = 2

matches = find_dna_motifs(dna, motif, max_mismatches)
print(f"Found {len(matches)} matches for '{motif}' allowing ≤{max_mismatches} mismatches:")
for start, dist in matches:
    snippet = dna[start:start + len(motif)]
    print(f"  Pos {start}: '{snippet}' (distance={dist})")
