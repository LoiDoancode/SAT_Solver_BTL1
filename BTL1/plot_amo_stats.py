import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_plots(output_dir):
    data = {
        'N': ['16', '16', '16', '16', '16', '64', '64', '64', '64', '64', '256', '256', '256', '256', '256', '1000', '1000', '1000', '1000', '1000'],
        'AMO': ['Pairwise', 'Binary', 'Commander', 'Product', 'Sequential Counter'] * 4,
        'Ctotal': [3520, 3072, 2112, 2304, 1856, 
                   1064832, 122880, 40512, 45056, 32128,
                   260000000, 3670016, 668160, 737280, 520704,
                   np.nan, 64000000, 10480000, 11520000, 8120000],
        'Tenc': [0.002, 0.003, 0.002, 0.002, 0.002,
                 0.185, 0.042, 0.015, 0.018, 0.012,
                 42.500, 1.250, 0.210, 0.240, 0.180,
                 np.nan, 22.400, 3.500, 3.900, 2.800],
        'Tsolve': [0.003, 0.004, 0.003, 0.003, 0.002,
                   0.120, 0.085, 0.045, 0.051, 0.032,
                   np.nan, 3.120, 0.850, 0.920, 0.540,
                   np.nan, 112.500, 28.300, 31.100, 18.600],
        'Ttotal': [0.005, 0.007, 0.005, 0.005, 0.004,
                   0.305, 0.127, 0.060, 0.069, 0.044,
                   np.nan, 4.370, 1.060, 1.160, 0.720,
                   np.nan, 134.900, 31.800, 35.000, 21.400]
    }
    
    df = pd.DataFrame(data)
    
    metrics = {
        'Ctotal': 'Số câu mệnh đề CNF (Ctotal)',
        'Tenc': 'Thời gian sinh CNF Tenc (s)',
        'Tsolve': 'Thời gian giải Tsolve (s)',
        'Ttotal': 'Tổng thời gian Ttotal (s)'
    }
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    amo_techniques = ['Pairwise', 'Binary', 'Commander', 'Product', 'Sequential Counter']
    n_values = ['16', '64', '256', '1000']
    
    for metric, title in metrics.items():
        plt.figure(figsize=(10, 6))
        
        # Prepare data for plotting
        bar_width = 0.15
        index = np.arange(len(n_values))
        
        for i, amo in enumerate(amo_techniques):
            amo_data = df[df['AMO'] == amo][metric].values
            # using a very small value instead of 0 for log scale if necessary, but we can just leave nans
            plt.bar(index + i * bar_width, amo_data, bar_width, label=amo, color=colors[i])
            
        plt.xlabel('Kích thước N')
        plt.ylabel(title)
        plt.title(f'Biểu đồ {title} theo từng phương pháp AMO và kích thước N')
        plt.xticks(index + bar_width * 2, n_values)
        plt.legend(title="Kỹ thuật AMO")
        
        # Use log scale since the values vary exponentially
        if metric == 'Ctotal':
            plt.yscale('log')
            plt.ylabel(title + ' (Log Scale)')
        else:
            plt.yscale('log')
            plt.ylabel(title + ' (Log Scale)')
            
        plt.grid(True, which="both", ls="--", alpha=0.5, axis='y')
        
        output_file = os.path.join(output_dir, f'plot_{metric.lower()}.png')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.close()
        print(f"Saved {output_file}")

if __name__ == '__main__':
    output_dir = r"C:\game\HK1_Nam3_2026\CVDHDKHMT\SAT_Solver_BTL1\BTL1\graph"
    os.makedirs(output_dir, exist_ok=True)
    generate_plots(output_dir)
