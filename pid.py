import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Настройки PID и шума
K_p = st.sidebar.slider("Пропорциональный коэффициент (Kp)", 0.0, 10.0, 1.0)
K_i = st.sidebar.slider("Интегральный коэффициент (Ki)", 0.0, 1.0, 0.1)
K_d = st.sidebar.slider("Дифференциальный коэффициент (Kd)", 0.0, 1.0, 0.01)
noise_scale = st.sidebar.slider("Уровень шума", 0.0, 1.0, 0.1, step=0.01)

set_point = st.sidebar.number_input("Заданное значение", value=50.0)
initial_value = st.sidebar.number_input("Начальное значение", value=0.0)

# Функция для моделирования PID с шумом
def simulate_pid(Kp, Ki, Kd, set_point, initial_value, n=300, noise_scale=0.5):
    dt = 0.1   # временной шаг
    values = [initial_value]
    errors = [set_point - initial_value]
    integral = 0
    time_steps = list(range(n))

    # Подготовка графика
    fig, ax = plt.subplots()
    line1, = ax.plot([], [], 'r-', label='Значение')
    line2, = ax.plot([], [], 'b-', label='Ошибка')
    ax.set_xlim(0, n*dt)
    ax.set_ylim(min(initial_value, set_point) - 10, max(initial_value, set_point) + 10)
    ax.legend()

    # Streamlit график
    plot_container = st.empty()

    for i in range(1, n):
        error = set_point - values[-1] + np.random.normal(0, noise_scale)  # добавление шума
        integral += error * dt
        derivative = (error - errors[-1]) / dt

        output = Kp * error + Ki * integral + Kd * derivative
        values.append(values[-1] + output * dt)
        errors.append(error)

        # Обновление графика
        line1.set_data(time_steps[:i], values[:i])
        line2.set_data(time_steps[:i], errors[:i])
        plot_container.pyplot(fig)
        time.sleep(0.1)

simulate_pid(K_p, K_i, K_d, set_point, initial_value, noise_scale=noise_scale)
