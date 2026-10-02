import time

try:
    import gurobipy as gp
    from gurobipy import GRB
    HAS_GUROBI = True
except ImportError:
    HAS_GUROBI = False

def solve_gurobi_mip(n):
    """
    ILP formulation for N-Queens using Gurobi.
    This provides an alternative exact method for comparison as requested (Cplex/Gurobi).
    """
    if not HAS_GUROBI:
        return {"error": "Gurobi not installed", "is_sat": False}
        
    try:
        # Create a new model, suppressing console output for cleaner benchmark
        env = gp.Env(empty=True)
        env.setParam("OutputFlag", 0)
        env.start()
        model = gp.Model("nqueens", env=env)
        
        # Variables: x[r, c] = 1 if queen is placed at row r, column c
        x = model.addVars(n, n, vtype=GRB.BINARY, name="x")
        
        # Exactly one queen per row
        model.addConstrs((x.sum(r, '*') == 1 for r in range(n)), name="row")
        
        # Exactly one queen per column
        model.addConstrs((x.sum('*', c) == 1 for c in range(n)), name="col")
        
        # At most one queen per diagonal ( \ )
        for d in range(-n + 1, n):
            model.addConstr(
                gp.quicksum(x[r, r - d] for r in range(n) if 0 <= r - d < n) <= 1,
                name=f"diag1_{d}"
            )
            
        # At most one queen per anti-diagonal ( / )
        for d in range(2 * n - 1):
            model.addConstr(
                gp.quicksum(x[r, d - r] for r in range(n) if 0 <= d - r < n) <= 1,
                name=f"diag2_{d}"
            )
            
        # We don't have an objective function, just finding a feasible solution
        
        start_time = time.time()
        model.optimize()
        solve_time = time.time() - start_time
        
        solution = []
        is_sat = False
        if model.status == GRB.OPTIMAL or model.status == GRB.SOLUTION_LIMIT:
            is_sat = True
            for r in range(n):
                for c in range(n):
                    if x[r, c].X > 0.5:
                        solution.append(c)
                        
        return {
            'is_sat': is_sat,
            'solution': solution,
            'solve_time': solve_time
        }
    except Exception as e:
        return {"error": str(e), "is_sat": False}
