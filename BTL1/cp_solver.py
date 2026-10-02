import time

try:
    from ortools.sat.python import cp_model
    HAS_ORTOOLS = True
except ImportError:
    HAS_ORTOOLS = False

def solve_ortools_cp_sat(n):
    """
    CP-SAT formulation for comparison.
    """
    if not HAS_ORTOOLS:
        return {"error": "OR-Tools not installed", "is_sat": False}
        
    model = cp_model.CpModel()
    queens = [model.NewIntVar(0, n - 1, f'q_{i}') for i in range(n)]
    
    # All rows must have different columns
    model.AddAllDifferent(queens)
    
    # All diagonals must be different
    model.AddAllDifferent([queens[i] + i for i in range(n)])
    model.AddAllDifferent([queens[i] - i for i in range(n)])
    
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0
    
    start_time = time.time()
    status = solver.Solve(model)
    solve_time = time.time() - start_time
    
    if solve_time >= 60.0 or status == cp_model.UNKNOWN:
        return {'error': 'run time error', 'is_sat': False}
        
    solution = []
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = [solver.Value(queens[i]) for i in range(n)]
        
    return {
        'is_sat': status in (cp_model.OPTIMAL, cp_model.FEASIBLE),
        'solution': solution,
        'solve_time': solve_time
    }
