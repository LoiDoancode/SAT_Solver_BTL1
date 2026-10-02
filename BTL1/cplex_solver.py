import time

try:
    from docplex.mp.model import Model as MpModel
    HAS_CPLEX_MIP = True
except ImportError:
    HAS_CPLEX_MIP = False

try:
    from docplex.cp.model import CpoModel
    HAS_CPLEX_CP = True
except ImportError:
    HAS_CPLEX_CP = False


def solve_cplex_mip(n):
    """
    ILP formulation for N-Queens using IBM CPLEX (docplex.mp).
    """
    if not HAS_CPLEX_MIP:
        return {"error": "docplex.mp not installed", "is_sat": False}
        
    try:
        model = MpModel(name="nqueens_mip")
        
        # Variables: x[r, c] = 1 if queen is placed at row r, column c
        x = model.binary_var_matrix(n, n, name="x")
        
        # Exactly one queen per row
        for r in range(n):
            model.add_constraint(model.sum(x[r, c] for c in range(n)) == 1)
            
        # Exactly one queen per column
        for c in range(n):
            model.add_constraint(model.sum(x[r, c] for r in range(n)) == 1)
            
        # At most one queen per diagonal ( \ )
        for d in range(-n + 1, n):
            model.add_constraint(model.sum(x[r, r - d] for r in range(n) if 0 <= r - d < n) <= 1)
            
        # At most one queen per anti-diagonal ( / )
        for d in range(2 * n - 1):
            model.add_constraint(model.sum(x[r, d - r] for r in range(n) if 0 <= d - r < n) <= 1)
            
        # Suppress console output
        model.context.solver.log_output = False
        model.set_time_limit(60.0)
        
        start_time = time.time()
        solution_obj = model.solve()
        solve_time = time.time() - start_time
        
        if solve_time >= 60.0:
            return {'error': 'run time error', 'is_sat': False}
            
        is_sat = solution_obj is not None
        solution = []
        if is_sat:
            for r in range(n):
                for c in range(n):
                    if solution_obj.get_value(x[r, c]) > 0.5:
                        solution.append(c)
                        
        return {
            'is_sat': is_sat,
            'solution': solution,
            'solve_time': solve_time
        }
    except Exception as e:
        return {"error": str(e), "is_sat": False}


def solve_cplex_cp(n):
    """
    CP formulation for N-Queens using IBM CPLEX CP Optimizer (docplex.cp).
    """
    if not HAS_CPLEX_CP:
        return {"error": "docplex.cp not installed", "is_sat": False}
        
    try:
        model = CpoModel(name="nqueens_cp")
        
        # Variables: queens[i] = column of queen in row i
        queens = model.integer_var_list(n, 0, n - 1, "Q")
        
        # All columns must be different
        model.add(model.all_diff(queens))
        
        # All diagonals must be different
        model.add(model.all_diff([queens[i] + i for i in range(n)]))
        model.add(model.all_diff([queens[i] - i for i in range(n)]))
        
        start_time = time.time()
        # Suppress output
        sol = model.solve(TimeLimit=60, LogVerbosity="Quiet")
        solve_time = time.time() - start_time
        
        if solve_time >= 60.0:
            return {'error': 'run time error', 'is_sat': False}
            
        is_sat = sol and sol.is_solution()
        solution = []
        if is_sat:
            solution = [sol[queens[i]] for i in range(n)]
            
        return {
            'is_sat': is_sat,
            'solution': solution,
            'solve_time': solve_time
        }
    except Exception as e:
        return {"error": str(e), "is_sat": False}
