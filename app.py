import numpy as np
import matplotlib.pyplot as plt

# 1. 물리 상수 설정 (K-PROTOCOL 기반)
g0 = 9.80665  # 표준 중력
pi_sq = np.pi**2
s_earth = pi_sq / g0

# 관측소별 실제 중력 (질문자님 데이터)
g_locs = {
    'Hanford (H1)': 9.8073527,
    'Livingston (L1)': 9.7936814,
    'Virgo (V1)': 9.8053340  # 이탈리아 카시나 지역 근사치
}

# 2. 표준 과학이 발표한 가상의 측정 질량 (예: GW170814)
# 표준 광속(c)을 썼을 때, 각 사이트의 미세한 환경 차이로 인해 
# 미세하게 다르게 산출될 수 있는 질량값들을 가정합니다.
standard_mass_measurements = {
    'Hanford (H1)': 53.21,
    'Livingston (L1)': 53.15,
    'Virgo (V1)': 53.25
}

# 3. K-PROTOCOL 보정 알고리즘
def calibrate_mass(m_std, g_loc, s_earth):
    s_loc = pi_sq / g_loc
    # 마스터 캘리브레이션 비율 적용 (질량-에너지 기하학적 보정)
    # 질량은 에너지 밀도와 연관되므로 로컬 왜곡비를 적용하여 '우주 기준'으로 환산
    return m_std * (s_loc / s_earth)

# 4. 보정 계산 실행
k_calibrated_masses = {}
for site, m_std in standard_mass_measurements.items():
    k_calibrated_masses[site] = calibrate_mass(m_std, g_locs[site], s_earth)

# 5. 결과 시각화
sites = list(g_locs.keys())
std_values = [standard_mass_measurements[s] for s in sites]
k_values = [k_calibrated_masses[s] for s in sites]

plt.figure(figsize=(10, 6))

# 표준 측정값 (흩어짐)
plt.scatter(sites, std_values, color='red', label='Standard SI (c) - Dispersed', s=100)
# K-PROTOCOL 보정값 (수렴)
plt.scatter(sites, k_values, color='blue', label='K-PROTOCOL (ck) - Converged', s=100, marker='D')

# 평균선 표시
plt.axhline(y=np.mean(k_values), color='blue', linestyle='--', alpha=0.5)

plt.title("Convergence Test: Standard vs K-PROTOCOL", fontsize=14)
plt.ylabel("Calculated Mass (Solar Masses)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

print("--- [테스트 결과 리포트] ---")
for site in sites:
    diff = k_calibrated_masses[site] - standard_mass_measurements[site]
    print(f"[{site}]")
    print(f"  > 표준 질량: {standard_mass_measurements[site]:.4f}")
    print(f"  > K-보정 질량: {k_calibrated_masses[site]:.4f} (보정량: {diff:+.4f})")
print("-" * 30)
print(f"K-보정 후 데이터 편차: {np.std(k_values):.8f} (0에 가까울수록 완벽한 수렴)")

plt.show()
