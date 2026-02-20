# coinline.py

from dataclasses import dataclass
from typing import List, Tuple, Optional

# ----------------------------
# Debugging helpers
# ----------------------------
DEBUG = True  # set to False when you're done debugging

def debug(*args):
    if DEBUG:
        print(*args)

# ----------------------------
# Game state
# ----------------------------
@dataclass(frozen=True)
class State:
    coins: Tuple[int, ...]
    pScore: int = 0
    aiScore: int = 0
    turn: str = 'player'  # 'player' or 'ai'


# ----------------------------
# Required functions
# ----------------------------
def player(state: State) -> str:
    return state.turn


def actions(state: State) -> List[Tuple[str, int]]:
    n = len(state.coins)
    if n == 0:
        return []

    acts: List[Tuple[str, int]] = [('L', 1), ('R', 1)]
    if n >= 2:
        acts.extend([('L', 2), ('R', 2)])
    return acts


def succ(state: State, action: Tuple[str, int]) -> State:
    side, k = action

    debug("\n--- MOVE START ---")
    debug("Current turn:", state.turn)
    debug("Coins before:", state.coins)
    debug("Action taken:", action)

    if side not in ('L', 'R') or k not in (1, 2):
        raise ValueError("Invalid action")
    n = len(state.coins)
    if k > n:
        raise ValueError("Not enough coins to take")

    coins_list = list(state.coins)

    if side == 'L':
        taken = coins_list[:k]
        new_coins = tuple(coins_list[k:])
    else:
        taken = coins_list[-k:]
        new_coins = tuple(coins_list[:-k])

    gained = sum(taken)

    if state.turn == 'player':
        new_p = state.pScore + gained
        new_ai = state.aiScore
        next_turn = 'ai'
    else:
        new_ai = state.aiScore + gained
        new_p = state.pScore
        next_turn = 'player'

    new_state = State(coins=new_coins, pScore=new_p, aiScore=new_ai, turn=next_turn)

    debug("Coins removed:", tuple(taken))
    debug("Gained:", gained)
    debug("Coins after:", new_state.coins)
    debug("Scores -> Player:", new_state.pScore, "AI:", new_state.aiScore)
    debug("Next turn:", new_state.turn)
    debug("--- MOVE END ---")

    return new_state


def terminal(state: State) -> bool:
    return len(state.coins) == 0


def utility(state: State) -> Tuple[int, int]:
    # You may assume utility is only called when terminal(state) is True
    return (state.pScore, state.aiScore)


def winner(state: State) -> Optional[str]:
    if not terminal(state):
        return None
    if state.pScore > state.aiScore:
        return 'player'
    if state.aiScore > state.pScore:
        return 'ai'
    return None


# ----------------------------
# Minimax (memoized)
# ----------------------------
_cache = {}

def _state_key(state: State, is_maximizing: bool):
    return (state.coins, state.pScore, state.aiScore, state.turn, is_maximizing)


def minimax(state: State, is_maximizing: bool):
    # Safe top-level AI logging (prevents recursion spam)
    if DEBUG and is_maximizing and state.turn == 'ai':
        print("\n=== AI THINKING ===")
        print("Current coins:", state.coins)
        print("Current scores -> Player:", state.pScore, "AI:", state.aiScore)

    key = _state_key(state, is_maximizing)
    if key in _cache:
        return _cache[key]

    if terminal(state):
        val = state.aiScore - state.pScore
        _cache[key] = (val, None)
        return _cache[key]

    possible = actions(state)
    best_action = None

    if is_maximizing:
        best_val = float('-inf')
        for a in possible:
            ns = succ(state, a)
            val, _ = minimax(ns, False)
            if val > best_val:
                best_val = val
                best_action = a

        if DEBUG and state.turn == 'ai':
            print("AI chose action:", best_action, "with evaluation:", best_val)

        _cache[key] = (best_val, best_action)
        return _cache[key]

    else:
        best_val = float('inf')
        for a in possible:
            ns = succ(state, a)
            val, _ = minimax(ns, True)
            if val < best_val:
                best_val = val
                best_action = a

        _cache[key] = (best_val, best_action)
        return _cache[key]