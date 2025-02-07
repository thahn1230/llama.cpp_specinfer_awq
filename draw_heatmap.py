import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 모델 조합 정의
LTM_models = ['gemma2-7b full precision', 'gemma2-7b 8bit', 'gemma2-7b 4bit']
SSM_models = ['gemma2-2b full precision', 'gemma2-2b 8bit', 'gemma2-2b 6bit', 'gemma2-2b 4bit', 'gemma2-2b 2bit']

# 예시 데이터 (각 모델 조합에 대한 acceptance rate)
data = {
    'gemma2-2b full precision': [0.61434, 0.61145, 0.26795],
    'gemma2-2b 8bit': [0.61311, 0.61096, 0.27341],
    'gemma2-2b 6bit': [0.59057, 0.59362, 0.26714],
    'gemma2-2b 4bit': [0.40674, 0.46588, 0.24711],
    'gemma2-2b 2bit': [0.12292, 0.18653, 0.13903]
}

# DataFrame 생성
df = pd.DataFrame(data, index=LTM_models)

# 히트맵 그리기
plt.figure(figsize=(10, 6))
sns.heatmap(df, annot=True, cmap='coolwarm', fmt='.5f', cbar=True)

# 그래프 제목과 레이블 설정
plt.title('Acceptance Rates for Speculative Decoding Models', fontsize=16)
plt.xlabel('SSM Models', fontsize=14)
plt.ylabel('LTM Models', fontsize=14)

# 그래프 저장 (저장할 파일 이름과 경로 지정)
plt.savefig('acceptance_rate_heatmap.png', dpi=300, format='png', bbox_inches='tight')

# 그래프 표시
plt.tight_layout()
plt.show()
