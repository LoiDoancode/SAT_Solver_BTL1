# Doãn Duy Lợi - MSV: 24021549
# N-Queens Benchmark: SAT Encodings vs. CP/ILP Solvers

Nghiên cứu và đánh giá thực nghiệm hiệu năng giải bài toán N-Queens quy mô lớn ($N \ge 1000$) bằng các kỹ thuật mã hóa SAT (PySAT) so với các bộ giải Lập trình ràng buộc (CP) và Quy hoạch tuyến tính nguyên (ILP)[cite: 2].

## Các phương pháp triển khai

- **SAT Encodings (PySAT):** Pairwise, Binary, Commander, Product, Sequential Counter (AMO/ALO) sử dụng backend *CaDiCaL* & *Glucose*[cite: 2, 4].
- **Constraint Programming (CP):** Google OR-Tools CP-SAT (ràng buộc toàn cục `AllDifferent`), CPLEX CP[cite: 2, 4, 5].
- **Integer Linear Programming (ILP):** Gurobi, CPLEX MIP[cite: 2, 4, 5].

---

## 📁 Cấu trúc dự án
```text
BTL1/
├── __pycache__/        # Thư mục cache của Python
├── .gitignore          # Cấu hình bỏ qua các file tạm/không cần thiết trong Git
├── cp_solver.py        # Bộ giải sử dụng Lập trình ràng buộc (Constraint Programming)
├── cplex_solver.py     # Bộ giải sử dụng IBM ILOG CPLEX Optimization Studio
├── main.py             # File chạy chính của chương trình
├── mip_solver.py       # Bộ giải Quy hoạch tuyến tính số nguyên hỗn hợp (MIP)
├── plan.txt            # Kế hoạch / Mô tả bài toán / Lộ trình thực hiện
├── results.csv         # File lưu kết quả thực nghiệm và so sánh hiệu năng
├── sat_solver.py       # Bộ giải SAT (Boolean Satisfiability)
└── utils.py            # Các hàm bổ trợ (đọc/ghi file, xử lý dữ liệu, vẽ biểu đồ...)
