from re import U
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# # remove axes ticks globally parameters
plt.rcParams["xtick.bottom"] = False
plt.rcParams["xtick.labelbottom"] = False
plt.rcParams["xtick.top"] = False
plt.rcParams["xtick.labeltop"] = False
plt.rcParams["ytick.left"] = False
plt.rcParams["ytick.labelleft"] = False
plt.rcParams["ytick.right"] = False
plt.rcParams["ytick.labelright"] = False

# reserve more memort to matplotlib for faster animation
plt.rcParams["animation.embed_limit"] = 2**512

# Given complex number F(u,v) = Mx + iMy
t = np.arange(0, 1, 0.01)
complex_nums = np.exp(1j * 2 * np.pi * t)
A = np.abs(complex_nums)
phi = np.arctan2(np.imag(complex_nums), np.real(complex_nums))

# k-space coordinates (u, v)
u, v = np.arange(-50, 50, 1), np.arange(-50, 50, 1)


# Create a grid of x and y values
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
x, y = np.meshgrid(x, y)

# 2D sinusoid
kxy = A[0] * np.exp(1j * (2 * np.pi * (u[0] * x + v[0] * y) + phi[0]))
# Calculate the real and imaginary parts of the 2D sinusoid
# real_part = A * np.cos(2 * np.pi * (u * x + v * y) + phi)
# imag_part = A * np.sin(2 * np.pi * (u * x + v * y) + phi)
fig = plt.figure(figsize=(20, 10))
ax4 = fig.add_subplot(141)
ax4.set_title("K-Space")

ax1 = fig.add_subplot(142, projection="3d")
ax1.set_title("Real Part")
ax1.view_init(azim=0, elev=90)
ax1.set_zlim(0, 1)
# ax1.plot_surface(x, y, np.real(kxy), cmap='viridis')
# ax1.set_title('Real Part')

ax2 = fig.add_subplot(143, projection="3d")
ax2.set_title("Imaginary Part")
ax2.view_init(azim=0, elev=90)
ax1.set_zlim(0, 1)

ax3 = fig.add_subplot(144)
ax3.set_title("Complex phasor")
ax3.set_xlim(-1, 1)
ax3.set_ylim(-1, 1)
ax3.set_aspect("equal")
ax3.grid(False)
ax3.set_xlabel("Real")
ax3.set_ylabel("Imaginary")


phase_slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
Amplitude_slider_ax = plt.axes([0.25, 0.05, 0.65, 0.03])
phase_slider = Slider(
    ax=phase_slider_ax,
    label="Phase",
    valmin=0,
    valmax=2 * np.pi,
    valinit=0,
    valstep=np.pi / 10,
)

Amplitude_slider = Slider(
    ax=Amplitude_slider_ax,
    label="Amplitude",
    valmin=0,
    valmax=1,
    valinit=0.5,
    valstep=0.1,
)

U_slider_ax = plt.axes([0.25, 0.15, 0.65, 0.03])
U_slider = Slider(
    ax=U_slider_ax,
    label="U",
    valmin=-32,
    valmax=32,
    valstep=1,
    valinit=2,
)

V_slider_ax = plt.axes([0.25, 0.2, 0.65, 0.03])
V_slider = Slider(
    ax=V_slider_ax,
    label="V",
    valmin=-32,
    valmax=32,
    valstep=1,
    valinit=2,
)


initial_U = 2  # Replace with the actual initial value of U
initial_V = 2  # Replace with the actual initial value of V


def update_frame(frame, total_frames):
    # Divide the total frames into four equal parts for phase, amplitude, U, and V
    segment_length = total_frames // 4
    segment_index = frame // segment_length
    frame_in_segment = frame % segment_length

    # Update phase
    if segment_index == 0:
        # Change phase from -2pi to 2pi
        new_phase = -2 * np.pi + 4 * np.pi * (frame_in_segment / segment_length)
        phase_slider.set_val(new_phase)

    # Update amplitude
    elif segment_index == 1:
        # Change amplitude from 0.5 to 0 and back to 0.5
        if frame_in_segment < segment_length / 2:
            new_amplitude = 0.5 - (frame_in_segment / (segment_length / 2)) * 0.5
        else:
            new_amplitude = (
                (frame_in_segment - segment_length / 2) / (segment_length / 2)
            ) * 0.5
        Amplitude_slider.set_val(new_amplitude)

    # Update U
    elif segment_index == 2:
        # Change U from initial value to 10 and back
        if frame_in_segment < segment_length / 2:
            new_U = initial_U + (frame_in_segment / (segment_length / 2)) * (
                10 - initial_U
            )
        else:
            new_U = 10 - (
                (frame_in_segment - segment_length / 2) / (segment_length / 2)
            ) * (10 - initial_U)
        U_slider.set_val(new_U)

    # Update V
    elif segment_index == 3:
        # Change V from initial value to -10 and back
        if frame_in_segment < segment_length / 2:
            new_V = initial_V + (frame_in_segment / (segment_length / 2)) * (
                -10 - initial_V
            )
        else:
            new_V = -10 - (
                (frame_in_segment - segment_length / 2) / (segment_length / 2)
            ) * (-10 - initial_V)
        V_slider.set_val(new_V)

    # Update the plot
    update_plot(None)


def update_plot(val):
    kxy = Amplitude_slider.val * np.exp(
        1j * (2 * np.pi * (U_slider.val * x + V_slider.val * y) + phase_slider.val)
    )
    phasor = Amplitude_slider.val * np.exp(1j * phase_slider.val)
    ax4.clear()
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # Draw horizontal line segment from x_min to V_slider.val at U_slider.val
    ax4.plot(
        [0, V_slider.val],
        [U_slider.val, U_slider.val],
        color="k",
        linestyle="--",
        linewidth=1,
    )

    # Draw vertical line segment from y_min to U_slider.val at V_slider.val
    ax4.plot(
        [V_slider.val, V_slider.val],
        [0, U_slider.val],
        color="k",
        linestyle="--",
        linewidth=1,
    )

    ax4.set_xlim(-32, 32)
    ax4.set_ylim(-32, 32)
    ax4.set_aspect("equal")
    ax4.grid("major", linewidth=0.5)
    ax4.set_xlabel("Kx")
    ax4.set_ylabel("Ky")

    ax1.plot_surface(x, y, np.real(kxy), cmap="viridis")
    ax1.set_title("Real Part")
    ax1.view_init(azim=0, elev=80)
    ax1.set_zlim(-1, 1)
    ax2.plot_surface(x, y, np.imag(kxy), cmap="inferno")
    ax2.set_title("Imag Part")
    ax2.view_init(azim=0, elev=80)
    ax2.set_zlim(-1, 1)
    ax2.set_aspect("equal")
    ax2.set_aspect("equal")

    ax3.set_title("Complex phasor")
    ax3.set_xlim(-1, 1)
    ax3.set_ylim(-1, 1)
    ax3.set_aspect("equal")
    ax3.grid(False)
    ax2.grid(False)
    ax1.grid(False)
    ax3.set_xlabel("Real")
    ax3.set_ylabel("Imaginary")
    ax3.arrow(
        0,
        0,
        np.real(phasor),
        np.imag(phasor),
        head_width=0.05,
        head_length=0.1,
        fc="k",
        ec="k",
    )

    fig.canvas.draw_idle()


phase_slider.on_changed(update_plot)
Amplitude_slider.on_changed(update_plot)
U_slider.on_changed(update_plot)
V_slider.on_changed(update_plot)
## ===================================== Uncomment this section to run the animation =====================================

# total_frames = 400  # Example total frames
# ani = FuncAnimation(
#     fig,
#     lambda frame: update_frame(frame, total_frames),
#     frames=total_frames,
#     blit=False,
# )
# ani.save("FT_2D.mp4", writer="ffmpeg", fps=30)


# =======================================================================================================================
plt.show()

# Plotting
