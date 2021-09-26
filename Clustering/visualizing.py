import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="ticks")

df = sns.load_dataset('anscombe')

print(df[df['dataset']=='I'].corr())   #상관계수

#col : dataset 기준으로 따로, col_wrap : n개씩 나눠서 보기, ci : 데이터 분포에 관한 신뢰구간, scatter_kws : 점 크기, 투명도
sns.lmplot(x="x", y="y", col="dataset", hue="dataset", data=df, ci=50, palette="muted", height=4, scatter_kws={"s": 50, "alpha": 1})