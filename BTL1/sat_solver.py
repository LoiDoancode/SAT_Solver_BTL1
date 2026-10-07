import time

try:
    from pysat.solvers import Glucose4, Cadical153
    from pysat.formula import CNF, IDPool
    from pysat.card import CardEnc, EncType
    HAS_PYSAT = True
except ImportError:
    HAS_PYSAT = False

class NQueensSAT:
    """
    N-Queens SAT Solver using PySAT's native CardEnc for At-Most-One (AMO) constraint.
    Supports various encodings like sequential counter, bitwise (binary), pairwise, etc.
    """
    def __init__(self, n, encoding_name="seqcounter"):
        self.n = n
        self.encoding_name = encoding_name.lower()
        self.cnf = CNF()
        self.vpool = IDPool()

    def var(self, r, c):
        return self.vpool.id((r, c))

    def get_enc_type(self):
        # Map requested names to PySAT's EncType
        mapping = {
            "seqcounter": EncType.seqcounter,
            "binary": EncType.bitwise,
            "bitwise": EncType.bitwise,
            "pairwise": EncType.pairwise,
            "totalizer": EncType.totalizer,
            # Commander and Product might not be natively named in PySAT's EncType, 
            # we use fallback or map to other robust encodings like totalizer if requested.
            "commander": EncType.totalizer, 
            "product": EncType.totalizer
        }
        return mapping.get(self.encoding_name, EncType.seqcounter)

    def amo_product(self, lits):
        import math
        n = len(lits)
        if n <= 1:
            return []
        if n == 2:
            return [[-lits[0], -lits[1]]]
            
        p = math.ceil(math.sqrt(n))
        q = math.ceil(n / p)
        
        group_id = self.vpool.id(("lits_group", tuple(lits)))
        rows = [self.vpool.id(("prod_r", group_id, i)) for i in range(p)]
        cols = [self.vpool.id(("prod_c", group_id, j)) for j in range(q)]
        
        clauses = []
        for idx, lit in enumerate(lits):
            r = idx // q
            c = idx % q
            clauses.append([-lit, rows[r]])
            clauses.append([-lit, cols[c]])
            
        amo_r = CardEnc.atmost(lits=rows, bound=1, encoding=EncType.seqcounter, vpool=self.vpool)
        clauses.extend(amo_r.clauses)
        
        amo_c = CardEnc.atmost(lits=cols, bound=1, encoding=EncType.seqcounter, vpool=self.vpool)
        clauses.extend(amo_c.clauses)
        
        return clauses

    def amo_commander(self, lits, group_size=3):
        n = len(lits)
        if n <= 1:
            return []
        if n <= group_size:
            # Base case: Pairwise
            clauses = []
            for i in range(n):
                for j in range(i + 1, n):
                    clauses.append([-lits[i], -lits[j]])
            return clauses
            
        groups = [lits[i:i + group_size] for i in range(0, n, group_size)]
        commanders = []
        clauses = []
        
        group_id = self.vpool.id(("cmd_group", tuple(lits)))
        
        for idx, g in enumerate(groups):
            if len(g) == 1:
                commanders.append(g[0])
            else:
                c_i = self.vpool.id(("cmd", group_id, idx))
                commanders.append(c_i)
                
                for i in range(len(g)):
                    for j in range(i + 1, len(g)):
                        clauses.append([-g[i], -g[j]])
                        
                for x in g:
                    clauses.append([-x, c_i])
                    
                clauses.append([-c_i] + g)
                
        clauses.extend(self.amo_commander(commanders, group_size))
        return clauses

    def add_amo(self, lits):
        if self.encoding_name == "product":
            clauses = self.amo_product(lits)
            self.cnf.extend(clauses)
        elif self.encoding_name == "commander":
            clauses = self.amo_commander(lits, group_size=3)
            self.cnf.extend(clauses)
        else:
            enc = self.get_enc_type()
            amo = CardEnc.atmost(lits=lits, bound=1, encoding=enc, vpool=self.vpool)
            self.cnf.extend(amo.clauses)

    def generate_clauses(self):
        n = self.n
        # 1. Exactly one queen per row
        for r in range(n):
            vars_row = [self.var(r, c) for c in range(n)]
            self.cnf.append(vars_row) # At-Least-One
            self.add_amo(vars_row)

        # 2. Exactly one queen per column
        for c in range(n):
            vars_col = [self.var(r, c) for r in range(n)]
            self.cnf.append(vars_col) # At-Least-One
            self.add_amo(vars_col)

        # 3. At most one queen per diagonal ( \ )
        for d in range(-n + 1, n):
            diag = [self.var(r, r - d) for r in range(n) if 0 <= r - d < n]
            if len(diag) > 1:
                self.add_amo(diag)

        # 4. At most one queen per anti-diagonal ( / )
        for d in range(2 * n - 1):
            diag = [self.var(r, d - r) for r in range(n) if 0 <= d - r < n]
            if len(diag) > 1:
                self.add_amo(diag)

    def solve(self, solver_name="cadical"):
        if not HAS_PYSAT:
            return {"error": "PySAT not installed", "is_sat": False}

        start_time = time.time()
        self.generate_clauses()
        encode_time = time.time() - start_time
        
        # Initialize SAT Solver
        if solver_name.lower() == "glucose":
            solver = Glucose4()
        else:
            solver = Cadical153()
            
        solver.append_formula(self.cnf)
            
        import threading
        timer = threading.Timer(60.0, solver.interrupt)
        timer.start()
        
        start_solve = time.time()
        is_sat = solver.solve()
        timer.cancel()
        solve_time = time.time() - start_solve
        
        if solve_time >= 60.0:
            solver.delete()
            return {'error': 'run time error', 'is_sat': False}
            
        solution = []
        if is_sat:
            model = solver.get_model()
            # Extract board configuration
            # In PySAT, model contains literals (positive for True, negative for False)
            for r in range(self.n):
                for c in range(self.n):
                    if model[self.var(r, c) - 1] > 0:
                        solution.append(c)
        solver.delete()
        
        return {
            'is_sat': is_sat,
            'solution': solution,
            'encode_time': encode_time,
            'solve_time': solve_time,
            'total_time': encode_time + solve_time,
            'num_vars': self.vpool.top,
            'num_clauses': len(self.cnf.clauses),
            'encoding_used': self.encoding_name
        }
