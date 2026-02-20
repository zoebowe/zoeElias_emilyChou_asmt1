# ============================================================
# 3 Jugs problem (or n jugs) definition
# Authors: S. El Alaoui and ChatGPT 5
# ============================================================

class SearchProblem:
    def start_state(self):
        raise NotImplementedError()

    def actions(self, state):
        raise NotImplementedError()

    def cost(self, state, action):
        raise NotImplementedError()

    def succ(self, state, action):
        raise NotImplementedError()

    def is_end(self, state):
        raise NotImplementedError()


# Action = of type Tuple[str, int, Optional[int]]  # ('fill', i, None) | ('empty', i, None) | ('pour', i, j)
# State = of type Tuple[int, ...] 


class NJugsProblem(SearchProblem):
    """
    N-jugs problem with the standard operations:
      - fill(i): fill jug i to its capacity from an infinite source
      - empty(i): empty jug i to drain
      - pour(i, j): pour from jug i into jug j until i is empty or j is full

    State is an N-tuple of amounts (non-negative ints).
    Cost per action defaults to 1 (can be changed with cost_per_move).
    """

    def __init__(self, capacities, goal):
        caps = tuple(int(c) for c in capacities)
        if any(c <= 0 for c in caps):
            raise ValueError("All capacities must be positive integers.")


        if not goal:
            raise ValueError("Goal must be provided.")

        goal = tuple(int(x) for x in goal)
        if len(goal) != len(capacities):
            raise ValueError("Goal length must match number of capacities (", len(capacities), ").")

        self.capacities = caps
        self.n = len(caps)
        self._goal = tuple(goal)

    # ---- SearchProblem API ----
    def start_state(self):
        return tuple(0 for _ in range(self.n))

    def is_end(self, state):
        return state == self._goal

    def cost(self, state, action) -> int:
        # Unit cost per move by default 1.
        return 1

    """
    Returns the set of all possible actions available on the current state of the jugs.

    The actions function should return a list of all the possible actions that can be taken given a state.

    Each action should be represented as a tuple (action_kind, i, j) 
    action_kind is one of: "fill", "empty" and "pour"
    i corresponds to the jug affected by the action
    j is a valid number only if the action is "pour" (i.e. pour from jug i into jug j). Otherwise it should be set to None
    """
    def actions(self, state):
        actions = []

        for i in range(self.n):
            # Fill action (only if jug not already full)
            if state[i] < self.capacities[i]:
                actions.append(("fill", i, None))

            # Empty action (only if jug not already empty)
            if state[i] > 0:
                actions.append(("empty", i, None))

            # Pour actions
            if state[i] > 0:  # can only pour if source has water
                for j in range(self.n):
                    if i != j and state[j] < self.capacities[j]:
                        actions.append(("pour", i, j))

        return actions
    """
    Returns the state of the jugs after taking action (kind, i, j), without modifying the original state.

    If `action` is not a valid action for the current state, you  should raise an exception.

    The returned state should be: tuple([j1, j2, j3]) 
    where j1, j2 and j3 represent the amount of water in each jug, respectively. 

    Importantly, the original state should be left unmodified. This 
    means that simply updating the input state itself is not a correct 
    implementation of this function. You’ll likely want to make a 
    copy of the state first before making any changes.
    """
    def succ(self, state, action):
        kind, i, j = action

        if i < 0 or i >= self.n:
            raise ValueError("Invalid jug index.")

        # Make a copy of state (important: do NOT modify original)
        new_state = list(state)

        if kind == "fill":
            if new_state[i] == self.capacities[i]:
                raise ValueError("Jug already full.")
            new_state[i] = self.capacities[i]

        elif kind == "empty":
            if new_state[i] == 0:
                raise ValueError("Jug already empty.")
            new_state[i] = 0

        elif kind == "pour":
            if j is None or j < 0 or j >= self.n or i == j:
                raise ValueError("Invalid pour action.")

            if new_state[i] == 0:
                raise ValueError("Source jug is empty.")

            if new_state[j] == self.capacities[j]:
                raise ValueError("Destination jug is full.")

            # Amount we can pour
            amount = min(new_state[i],
                         self.capacities[j] - new_state[j])

            new_state[i] -= amount
            new_state[j] += amount

        else:
            raise ValueError("Unknown action type.")

        return tuple(new_state)


    # ---- Helpers ----

    @property
    def goal(self):
        return self._goal

    @property
    def capacities_tuple(self):
        return self.capacities

