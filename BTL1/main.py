import csv
from sat_solver import NQueensSAT, HAS_PYSAT
from cp_solver import solve_ortools_cp_sat, HAS_ORTOOLS
from mip_solver import solve_gurobi_mip, HAS_GUROBI
from cplex_solver import solve_cplex_mip, solve_cplex_cp, HAS_CPLEX_MIP, HAS_CPLEX_CP
from utils import print_board

def run_benchmarks():
    sizes = [10, 20, 30, 40, 50, 60]  # Thử nghiệm với các kích thước lớn
    encodings = ["seqcounter", "binary", "pairwise"]  # Các phương pháp encoding từ PySAT
    
    csv_file = "results.csv"
    
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        # Header for the benchmark
        header = ["N", "CP_Time_ORTools", "CP_Time_CPLEX", "MIP_Time_Gurobi", "MIP_Time_CPLEX"]
        for enc in encodings:
            header.extend([f"SAT_{enc}_Total", f"SAT_{enc}_Vars", f"SAT_{enc}_Clauses"])
        writer.writerow(header)
        
        print("Bắt đầu chạy thực nghiệm Benchmarks...")
        print("=========================================")
        
        for n in sizes:
            row_data = [n]
            print(f"\\nĐang giải với N = {n}...")
            
            # 1. OR-Tools CP-SAT
            cp_time = "N/A"
            if HAS_ORTOOLS:
                res_cp = solve_ortools_cp_sat(n)
                if "error" not in res_cp and res_cp["is_sat"]:
                    cp_time = res_cp["solve_time"]
                    print(f"  [CP-SAT (OR-Tools)] Thời gian tìm nghiệm đầu tiên: {cp_time:.4f}s")
            row_data.append(cp_time)
            
            # 2. CPLEX CP
            cplex_cp_time = "N/A"
            if HAS_CPLEX_CP:
                res = solve_cplex_cp(n)
                if "error" not in res and res.get("is_sat"):
                    cplex_cp_time = res["solve_time"]
                    print(f"  [CPLEX CP] Thời gian tìm nghiệm đầu tiên: {cplex_cp_time:.4f}s")
                elif "error" in res:
                    print(f"  [CPLEX CP] Lỗi: {res['error']}")
            row_data.append(cplex_cp_time)
            
            # 3. Gurobi MIP
            mip_time = "N/A"
            if HAS_GUROBI:
                res_mip = solve_gurobi_mip(n)
                if "error" not in res_mip and res_mip.get("is_sat"):
                    mip_time = res_mip["solve_time"]
                    print(f"  [Gurobi MIP] Thời gian tìm nghiệm đầu tiên: {mip_time:.4f}s")
                elif "error" in res_mip:
                    print(f"  [Gurobi MIP] Lỗi: {res_mip['error']}")
            row_data.append(mip_time)
            
            # 4. CPLEX MIP
            cplex_mip_time = "N/A"
            if HAS_CPLEX_MIP:
                res = solve_cplex_mip(n)
                if "error" not in res and res.get("is_sat"):
                    cplex_mip_time = res["solve_time"]
                    print(f"  [CPLEX MIP] Thời gian tìm nghiệm đầu tiên: {cplex_mip_time:.4f}s")
                elif "error" in res:
                    print(f"  [CPLEX MIP] Lỗi: {res['error']}")
            row_data.append(cplex_mip_time)
            
            # 5. SAT Solver với nhiều Encoding khác nhau
            if HAS_PYSAT:
                for enc in encodings:
                    sat_solver = NQueensSAT(n, encoding_name=enc)
                    res_sat = sat_solver.solve("cadical")
                    
                    if "error" not in res_sat and res_sat["is_sat"]:
                        total_time = res_sat["total_time"]
                        vars_count = res_sat["num_vars"]
                        clauses_count = res_sat["num_clauses"]
                        
                        row_data.extend([total_time, vars_count, clauses_count])
                        print(f"  [SAT-{enc}] Tổng thời gian: {total_time:.4f}s, Biến: {vars_count}, Mệnh đề: {clauses_count}")
                    else:
                        row_data.extend(["N/A", "N/A", "N/A"])
                        print(f"  [SAT-{enc}] Thất bại hoặc lỗi.")
            else:
                for _ in encodings:
                    row_data.extend(["N/A", "N/A", "N/A"])
                    
            # Ghi kết quả N hiện tại vào CSV
            writer.writerow(row_data)
            f.flush()
            
    print(f"\\n=========================================")
    print(f"Đã hoàn thành! Kết quả được lưu tại: {csv_file}")
    
    if not HAS_PYSAT:
        print("⚠ Ghi chú: PySAT chưa được cài đặt. (pip install python-sat)")
    if not HAS_ORTOOLS:
        print("⚠ Ghi chú: OR-Tools chưa được cài đặt. (pip install ortools)")
    if not HAS_GUROBI:
        print("⚠ Ghi chú: Gurobi chưa được cài đặt. (pip install gurobipy)")
    if not HAS_CPLEX_CP or not HAS_CPLEX_MIP:
        print("⚠ Ghi chú: CPLEX chưa được cài đặt đầy đủ. (pip install docplex cplex)")

if __name__ == "__main__":
    # Nút bật/tắt (Uncomment run_benchmarks() để chạy full ghi ra CSV)
    # run_benchmarks()
    HAS_CPLEX_MIP = False
    HAS_CPLEX_CP = False
    try:
        n_size = int(input("Nhập giá trị N (số lượng quân Hậu): "))
    except ValueError:
        print("Vui lòng nhập một số nguyên hợp lệ.")
        exit(1)
        
    print("=" * 65)
    print(f"   THỬ NGHIỆM ĐỘC LẬP & SO SÁNH NHANH CÁC SOLVER - N = {n_size}")
    print("=" * 65)
    
    # 1. CONSTRAINT PROGRAMMING (CP)
    print("\n--- 1. CONSTRAINT PROGRAMMING (CP) ---")
    if HAS_ORTOOLS:
        res = solve_ortools_cp_sat(n_size)
        if "error" not in res and res.get("is_sat"):
            print(f"✅ [OR-Tools CP-SAT] Thời gian tìm nghiệm đầu tiên: {res['solve_time']:.4f}s")
        else:
            print(f"❌ [OR-Tools CP-SAT] Lỗi: {res.get('error', 'Unsat')}")
    else:
        print("⏭ [OR-Tools CP-SAT] Bỏ qua (chưa cài ortools)")
        
    if HAS_CPLEX_CP:
        res = solve_cplex_cp(n_size)
        if "error" not in res and res.get("is_sat"):
            print(f"✅ [CPLEX CP]        Thời gian tìm nghiệm đầu tiên: {res['solve_time']:.4f}s")
        else:
            print(f"❌ [CPLEX CP]        Lỗi: {res.get('error', 'Unsat')}")
    else:
        print("⏭ [CPLEX CP]        Bỏ qua (chưa cài docplex)")
        
    # 2. INTEGER LINEAR PROGRAMMING (ILP)
    print("\n--- 2. INTEGER LINEAR PROGRAMMING (ILP/MIP) ---")
    if HAS_GUROBI:
        res = solve_gurobi_mip(n_size)
        if "error" not in res and res.get("is_sat"):
            print(f"✅ [Gurobi MIP]      Thời gian tìm nghiệm đầu tiên: {res['solve_time']:.4f}s")
        else:
            print(f"❌ [Gurobi MIP]      Lỗi: {res.get('error', 'Unsat')}")
    else:
        print("⏭ [Gurobi MIP]      Bỏ qua (chưa cài gurobipy)")

    if HAS_CPLEX_MIP:
        res = solve_cplex_mip(n_size)
        if "error" not in res and res.get("is_sat"):
            print(f"✅ [CPLEX MIP]       Thời gian tìm nghiệm đầu tiên: {res['solve_time']:.4f}s")
        else:
            print(f"❌ [CPLEX MIP]       Lỗi: {res.get('error', 'Unsat')}")
    else:
        print("⏭ [CPLEX MIP]       Bỏ qua (chưa cài docplex)")

    # 3. BOOLEAN SATISFIABILITY (SAT)
    print("\n--- 3. SAT SOLVING (Cadical) ---")
    if HAS_PYSAT:
        for enc in ["seqcounter", "binary", "pairwise"]:
            solver = NQueensSAT(n_size, encoding_name=enc)
            res = solver.solve("cadical")
            if "error" not in res and res.get("is_sat"):
                print(f"✅ [SAT - {enc.upper():<10}] Tổng thời gian: {res['total_time']:.4f}s (Encode: {res['encode_time']:.4f}s, Tìm nghiệm đầu: {res['solve_time']:.4f}s)")
            else:
                print(f"❌ [SAT - {enc.upper():<10}] Lỗi: {res.get('error', 'Unsat')}")
    else:
        print("⏭ [SAT]             Bỏ qua (chưa cài python-sat)")
        
    print("\n" + "=" * 65)
