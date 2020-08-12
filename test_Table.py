from Table import Table

"""
1) Testing constructor & assigning the attributes !!!
2) !!! __get__  method !!! don't know what's that but might be usefull
3) __str__ to print state of the game
4) before each print of state the window must be cleared 
5) ... Rest later

"""

table_one = Table()
print(table_one)
table_one.bets_declaration()
table_one.deal_cards()
table_one.run_game()
table_one.end_game()

print(table_one)
