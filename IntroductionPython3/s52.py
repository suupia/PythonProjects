
questions = [
    "We don't ...",
    "What is said ...",
    "What makes ..."
]

answers = [
    "An exploding sheep.",
    "No, I'm a frayed knot.",
    "'Pop! goes the weasel.'"
]

q_a = ((0,1),(1,2),(2,0)) #タプル

for (q,a) in q_a:
    print("Q:", questions[q])
    print("A:", answers[a])
    print()
