l = ['assassin', 'captain']
cards = ['Assassin']
deadCards = ['Captain']
print l

print tuple(l)

print"hello there {!s}, {!s}".format(*l)
print ', '.join(l)
print ":flower_playing_cards:: {!s}, {!s}[DEAD]".format(*l)