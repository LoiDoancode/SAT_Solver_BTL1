def print_board(solution):
    """
    Prints the N-Queens board given a solution array,
    and lists the positions of the queens.
    """
    if not solution:
        print("No solution found or provided.")
        return
    n = len(solution)
    
    print("\n   Bàn cờ:")
    for r in range(n):
        row_str = "   "
        for c in range(n):
            if solution[r] == c:
                row_str += "Q "
            else:
                row_str += ". "
        print(row_str)
        
    print("\n   Vị trí các quân hậu (hàng, cột):")
    positions = [(r, solution[r]) for r in range(n)]
    print(f"   {positions}\n")
