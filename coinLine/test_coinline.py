from coinline import State, actions, succ, terminal, utility, winner, minimax

s = State(coins=(3,9,1,2))
print("actions:", actions(s))
s1 = succ(s, ('L',1))
print("after L1:", s1)
print("minimax (AI) on small board:", minimax(State(coins=(3,9)), True))