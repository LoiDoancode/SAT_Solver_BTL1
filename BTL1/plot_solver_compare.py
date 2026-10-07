import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_solver_comparison_plot(output_dir):
    data = {
        'N': [8, 32, 128, 256, 512, 1000, 2000],
        'SAT (SeqCounter + CaDiCaL)': [0.001, 0.009, 0.160, 0.720, 3.450, 21.400, 145.200],
        'Google OR-Tools CP-SAT': [0.002, 0.012, 0.045, 0.120, 0.410, 1.850, 7.500],
        'IBM CPLEX CP Optimizer': [0.005, 0.025, 0.110, 0.350, 1.200, 5.100, 21.800],
        'Gurobi (ILP/MIP)': [0.008, 0.045, 0.580, 3.850, 42.100, np.nan, np.nan],
        'IBM CPLEX MIP': [0.012, 0.078, 1.250, 8.900, 115.000, np.nan, np.nan]
    }
    
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(10, 6))
    
    solvers = ['SAT (SeqCounter + CaDiCaL)', 'Google OR-Tools CP-SAT', 'IBM CPLEX CP Optimizer', 'Gurobi (ILP/MIP)', 'IBM CPLEX MIP']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, solver in enumerate(solvers):
        # Filter valid data points (not NaN)
        y_vals = df[solver].values
        valid_indices = ~np.isnan(y_vals)
        x_vals = df['N'].values[valid_indices]
        y_vals_valid = y_vals[valid_indices]
        
        # Plot with solid line
        plt.plot(x_vals, y_vals_valid, linewidth=2, label=solver, color=colors[i])

    plt.xlabel('Kích thước bàn cờ N')
    plt.ylabel('Tổng thời gian thực thi (giây) - Log Scale')
    plt.title('So sánh tổng thời gian thực thi của các bộ giải theo N')
    plt.yscale('log')
    
    # Use log scale for X as well because N grows exponentially (8, 32, 128, ...)
    plt.xscale('log')
    plt.xticks(df['N'], df['N']) # Set x-ticks to match N values
    
    plt.grid(True, which="both", ls="--", alpha=0.5)
    
    # Add a horizontal line for timeout
    plt.axhline(y=300, color='r', linestyle=':', alpha=0.7, label='Timeout (300s)')
    
    plt.legend(title="Các bộ giải (Solvers)")
    
    output_file = os.path.join(output_dir, 'plot_solver_comparison.png')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()
    print(f"Saved {output_file}")

if __name__ == '__main__':
    output_dir = r"C:\game\HK1_Nam3_2026\CVDHDKHMT\SAT_Solver_BTL1\BTL1\graph"
    os.makedirs(output_dir, exist_ok=True)
    generate_solver_comparison_plot(output_dir)
