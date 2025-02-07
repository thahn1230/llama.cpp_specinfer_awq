import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 준비 (Perplexity 값 수정됨)
data = {
    'Model': ['gemma2-7b'] * 14,
    'Quantization Method': [
        'full precision', 'Q8_0', 'Q6_K', 'Q5_K', 'Q4_K', 'Q3_K', 'Q2_K',
        'full precision', 'Q8_0', 'Q6_K', 'Q5_K', 'Q4_K', 'Q3_K', 'Q2_K'
    ],
    'Perplexity': [
        7.3012, 7.0365, 7.3839, 7.4259, 7.578, 8.4036, None,  # 첫 번째 데이터 블록 (Q2_K 값 수정)
        9.132, 9.162, 9.3795, 9.462, 9.7042, 10.9054, 18.517     # 두 번째 데이터 블록
    ],
    'ModelSize_MB': [
        16284.67, 8651.54, 6679.65, 5854.09, 5077.09, 4161.15, 3314.4,
        4780.29, 2539.66, 1960.84, 1748.67, 1548.98, 1313.94, 1098.52
    ],
    'Model Type': ['Gemma2-7B'] * 7 + ['Gemma2-2B'] * 7  # 데이터 블록 구분
}

df = pd.DataFrame(data)

# 시각화 설정
plt.figure(figsize=(14, 10))
sns.set(style="whitegrid")

# 산점도 그리기 (markers as dict)
scatter = sns.scatterplot(
    data=df,
    x='ModelSize_MB',
    y='Perplexity',
    hue='Quantization Method',
    style='Model Type',
    s=100,
    palette='viridis',
    markers={'Gemma2-7B': 'o', 'Gemma2-2B': 's'},
    legend='full'
)

# 그래프 제목 및 축 레이블 설정
plt.title('Tradeoff between Model Size and Perplexity with Quantization Techniques', fontsize=18)
plt.xlabel('Model Size (MB)', fontsize=14)
plt.ylabel('Perplexity (wikitext2)', fontsize=14)

# 레전드 위치 조정
plt.legend(title='Quantization & Experiment', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

# 그래프 레이아웃 조정
plt.tight_layout()

# 그래프를 PNG 파일로 저장
plt.savefig('scatter_plot.png', dpi=300, format='png', bbox_inches='tight')

# 그래프 표시
plt.show()
