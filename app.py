import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. 앱 제목 설정
st.title("🚀 K-PROTOCOL: Mass Convergence Test")
st.write("표준 SI 상수(c)와 K-PROTOCOL(ck)의 질량 산출 결과 비교")

# 2. 물리 상수 및 설정
g0 = 9.80665
pi_sq = np.pi**2
s_earth = pi_sq / g0

g_locs = {
    'Hanford (H1)': 9.8073527,
    'Livingston (L1)': 9.7936814,
    'Virgo (V1)': 9.8053340
}

# 3. 표준 과학 측정값 (입력 예시)
standard_masses = {
    'Hanford (H1)': 53.21,
    'Livingston (L1)': 53.15,
    'Virgo (V1)': 53.25
}

# 4. K-PROTOCOL 보정 계산
k_masses = {}
for site, m_std in standard_masses.items():
    s_loc = pi_sq / g_locs[site]
    # 질량-에너지 기하학적 보정 (마스터 공식)
    k_masses[site] = m_std * (s_loc / s_earth)

# 5. 화면 출력용 그래프 생성
fig, ax = plt.subplots(figsize=(10, 5))

sites = list(g_locs.keys())
std_vals = [standard_masses[s] for s in sites]
k_vals = [k_masses[s] for s in sites]

# 그래프 그리기
ax.scatter(sites, std_vals, color='red', label='Standard SI (Dispersed)', s=150, alpha=0.6)
ax.scatter(sites, k_vals, color='blue', label='K-PROTOCOL (Converged)', s=150, marker='D')
ax.axhline(y=np.mean(k_vals), color='blue', linestyle='--', alpha=0.3)

ax.set_ylabel("Solar Masses (M☉)")
ax.set_title("Mass Data Convergence Analysis")
ax.legend()
ax.grid(True, axis='y', linestyle=':', alpha=0.5)

# 🌟 핵심: 스트림릿 전용 출력 명령어
st.pyplot(fig)

# 6. 결과 표 출력
st.subheader("📊 Detailed Results")
col1, col2 = st.columns(2)

with col1:
    st.write("**Standard (SI)**")
    for s, v in standard_masses.items():
        st.write(f"{s}: {v:.4f}")

with col2:
    st.write("**K-PROTOCOL (Corrected)**")
    for s, v in k_masses.items():
        st.write(f"{s}: {v:.4f}")

st.success(f"Convergence Standard Deviation: {np.std(k_vals):.8f}")
