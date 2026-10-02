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
.
├── encodings/          # Triển khai các thuật toán mã hóa SAT (Pairwise, Binary, Sequential Counter...)
├── solvers/            # Mô hình bài toán cho CP (OR-Tools, CPLEX CP) và ILP (Gurobi, CPLEX MIP)
├── experiments/        # Script chạy thực nghiệm tự động theo kích thước N = [8, 16, ..., 1000+]
├── results/            # Báo cáo kết quả: Thời gian giải (Execution Time), Bộ nhớ (Peak Memory), File log
├── main.py             # Entrypoint chính để chạy benchmark
└── README.md
