import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_benchmark():
    csv_file = "results.csv"
    if not os.path.exists(csv_file):
        print(f"File {csv_file} không tồn tại. Vui lòng chạy benchmark trước.")
        return

    df = pd.read_csv(csv_file, na_values=["N/A", "NaN"])
    
    plt.figure(figsize=(12, 8))
    
    # Vẽ CP/MIP
    if 'CP_Time_ORTools' in df.columns:
        valid = pd.to_numeric(df['CP_Time_ORTools'], errors='coerce')
        plt.plot(df['N'], valid, linewidth=2, label='OR-Tools CP-SAT')
        
    # Vẽ các phương pháp SAT
    sat_columns = [col for col in df.columns if col.startswith('SAT_') and col.endswith('_Total')]
    
    for i, col in enumerate(sat_columns):
        method_name = col.replace('SAT_', '').replace('_Total', '').upper()
        valid = pd.to_numeric(df[col], errors='coerce')
        plt.plot(df['N'], valid, linewidth=2, label=f'SAT - {method_name}')

    plt.xlabel('Kích thước bàn cờ (N)', fontsize=12)
    plt.ylabel('Thời gian giải (giây) - Thang log', fontsize=12)
    plt.title('So sánh hiệu năng các thuật toán giải bài toán N-Queens', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    
    # Sử dụng thang đo logarit ở trục y để dễ quan sát sự chênh lệch lớn
    plt.yscale('log') 
    
    output_img = "benchmark_chart.png"
    plt.savefig(output_img, dpi=300, bbox_inches='tight')
    print(f"Đã lưu biểu đồ vào {output_img}")
    plt.show()

if __name__ == "__main__":
    plot_benchmark()
