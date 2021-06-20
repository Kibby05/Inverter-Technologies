import numpy as np
from scipy.integrate import *
import matplotlib as mpl
import matplotlib.pyplot as plt


class Inverter:
    """docstring for Inverter"""
    InitVoltage = 1.0			   # Assume that all inverters are operating at nominal steady state voltage
    def __init__(self, ni, mi, tao, Prated, wn, Ei, init_Phase):
        # Droop Gain Set points
        self.ni = ni 				# Rad/s/VAR 
        self.mi = mi 				# V/Watt
        # Nominal Operation Set points
        self.wn = wn 				# rad/s
        self.Ei = Ei 				# V p.u.
        self.tao = tao 			   	# Inverter delay time constants
        # Inverter rated power
        self.Pi = Prated		   	# Rated active power injection
        self.Pnom = 0.8 * Prated      # Nominal active power injection set point
        self.Qimax = Prated * -0.44	 # Max Reactive power injection
        self.Qimin = Prated * 0.44  # Max Reactive power absorption
        # Initial Phase
        self.InitPhase = init_Phase
        # self.InitPhase = 2*np.pi()*np.random.random()

def Init_Inverters(Inverters):
    print("Running Init_Inverters")
    # Define Init_vars as global for use in other functions...
    global Phase_state_mat
    global Phase_Next_state
    global Voltage_state_mat
    global Voltage_Next_state
    global Phase_influence_mat
    global Init_Phase
    global Init_Voltage
    global Init_states

    # Initialize matrices needed for simulation...
    Phase_state_mat = np.zeros((len(Inverters), len(Inverters))) # [0] * len(Inverters)
    Voltage_state_mat = [0] * len(Inverters)
    Phase_Next_state = [0] * len(Inverters)
    Voltage_Next_state = [0] * len(Inverters)
    Phase_influence_mat = np.zeros((len(Inverters), len(Inverters)))
    Coupling_Gain_mat = np.zeros((len(Inverters), len(Inverters)))

    # Initialize Network Voltages and phases at each bus...
    Init_Phase = []
    Init_Voltage = []
    for i in range(len(Inverters)):
        Init_Voltage.append(Inverter.InitVoltage)
        Init_Phase.append(Inverters[i].InitPhase)
    Init_states = Init_Phase + Init_Voltage

    print("Inverters Initialized!")
    pass

def Init_Network(L1, L2, L3, L4):
    print("Running Init_Network")
    # Define Init_vars as global for use in other functions...
    global scale

    scale = np.array([[1, -1, -1, -1], [-1, 1, -1, -1], [-1, -1, 1, -1], [-1, -1, -1, 1]]) # This is NOT expandable needs to be fixed later
    Network_Coupling(L1, L2, L3, L4)

    print("Network Initialized!")

    pass

def Network_Coupling(L1, L2, L3, L4):
    global Y_mag
    global Y_ang
    global Y_angT

    # Transfer Admittances (Phlox)
    Yb12 = Yb21 = np.complex(33333, 27824.15)
    Yb14 = Yb41 = np.complex(33333, 27824.15)
    Yb34 = Yb43 = np.complex(33333, 27824.15)
    Yb23 = Yb32 = np.complex(33333, 27824.15)
    Yb13 = Yb24 = Yb31 = Yb42 = 0
    # Weak Coupling Test
    # Yb12 = Yb21 = np.complex(33.333, 27.824)
    # Yb14 = Yb41 = np.complex(33.333, 27.824)
    # Yb34 = Yb43 = np.complex(33.333, 27.824)
    # Yb23 = Yb32 = np.complex(33.333, 27.824)
    # Yb13 = Yb24 = Yb31 = Yb42 = 0

    # Driving-point admittances
    Yb11, Yb22, Yb33, Yb44 = L1 + Yb12 + Yb14, L2 + Yb21 + Yb23, L3 + Yb32 + Yb34, L4 + Yb41 + Yb43

    Y = np.array(
        [[Yb11, Yb12, Yb13, Yb14], [Yb21, Yb22, Yb23, Yb24], [Yb31, Yb32, Yb33, Yb34], [Yb41, Yb42, Yb43, Yb44]])
    Y_mag = np.absolute(Y)
    # print(Y_mag)
    Y_ang = np.angle(Y)
    # print(Y_ang)
    Y_angT = Y_ang.transpose()

    pass


def Run_Simulation(ts):
    print("Running Simulation")

    # Define Init_vars as global for use in other functions...
    global Inst_Volt
    global Inst_Phase
    global Freq_Error
    global return_state

    # Initialize lists to capture values for plotting...
    Inst_Volt = []
    Inst_Phase = []
    Freq_Error = []
    states = []
    next_states = Init_states
    states.append(next_states)

    for i in range(len(ts)-1):
        # Create time interval for integration
        # print(ts[i])

        if ts[i] > 2.0 and ts[i] < 3.5:
            # print("I entered if statement")
            L1 = np.complex(0.7, 0.44)
            L2 = np.complex(0.4, 0.132)
            L3 = np.complex(0.8, 0.264)
            L4 = np.complex(0.6, 0.22)
            Network_Coupling(L1, L2, L3, L4)
        if ts[i] > 3.5:
            L1 = np.complex(0.4, 0.44)
            L2 = np.complex(0.3, 0.132)
            L3 = np.complex(0.2, 0.264)
            L4 = np.complex(0.8, 0.22)
            Network_Coupling(L1, L2, L3, L4)

        t = [ts[i], ts[i+1]]
        return_state = odeint(InvNW_Simulation, next_states, t, hmax = 0.01)
        state_buffer = return_state[-1].tolist()
        
        
        
        # Check for Voltage Droop violation
        E = [state_buffer[j] for j in range(len(Inverters), 2 * len(Inverters))]
        phase_buffer = [state_buffer[j] for j in range(0, len(Inverters))]
        phase = np.arctan2(np.sin(phase_buffer), np.cos(phase_buffer)).tolist()

        for x in range(0, len(Inverters)):
            if E[x] < (Inverters[x].Ei - Inverters[x].mi * (Inverters[x].Pi - Inverters[x].Pnom)):
                E[x] = (1 / Inverters[x].tao) * (
                            1 * (Inverters[x].Ei - E[x]) - Inverters[x].mi * (Inverters[x].Pi - Inverters[x].Pnom))
            elif E[x] > (Inverters[x].Ei - Inverters[x].mi * (Inverters[x].Pnom - Inverters[x].Pi)):
                E[x] = (1 / Inverters[x].tao) * (
                            1 * (Inverters[x].Ei - E[x]) - Inverters[x].mi * (Inverters[x].Pnom - Inverters[x].Pi))

        next_states = phase + E
        print(next_states)
        states.append(next_states)

    # print(states)
    # print(Freq_Error)
    Display_data(np.array(states), ts)

    pass


def InvNW_Simulation(state, ts):

    # Parse state list
    E = [state[j] for j in range(len(Inverters), 2*len(Inverters))]
    phase = [state[j] for j in range(0, len(Inverters))]
    Phase_state_vect = np.array([phase]).T
    Voltage_state_vect = np.array([E]).T

    # Update coupling matrix with new states
    Coupling_K_Mat = np.multiply(scale, np.multiply(Voltage_state_vect, np.matmul(Y_mag, np.diag(E))))

    # Compute next states for Inverters
    for x in range(0, len(Inverters)):
        # Calculate the Phase Error b/w Buses
        Phase_state_mat[:, x] = phase[x]
        Phase_influence_mat[:, [x]] = Phase_state_mat[:, [x]] - Phase_state_vect - Y_angT[:, [x]]

        # Calculate Next Phase State
        Phase_Next_state_ = Inverters[x].wn + Inverters[x].ni * (np.matmul(Coupling_K_Mat[[x], :], np.sin(Phase_influence_mat[:, [x]])))
        Phase_Next_state[x] = Phase_Next_state_.squeeze().tolist()

        # # Limit Reactive Power Injection to Inverter Ratings
        # if Phase_Next_state[x] < (Inverters[x].wn + Inverters[x].ni * Inverters[x].Qimax):
        #     Phase_Next_state[x] = Inverters[x].wn + Inverters[x].ni * Inverters[x].Qimax
        # elif Phase_Next_state[x] > (Inverters[x].wn + Inverters[x].ni * Inverters[x].Qimin):
        #     Phase_Next_state[x] = Inverters[x].wn + Inverters[x].ni * Inverters[x].Qimin

        # Calculate Next Voltage State
        Voltage_Next_state_ = (1 / Inverters[x].tao) * (1 * (Inverters[x].Ei - E[x]) + Inverters[x].mi * ( Inverters[x].Pnom - (np.matmul(Coupling_K_Mat[[x], :], np.cos(Phase_influence_mat[:, [x]])))))
        Voltage_Next_state[x] = Voltage_Next_state_.squeeze().tolist()

    # Update state list
    Next_state = Phase_Next_state + Voltage_Next_state
    print(Next_state)
    # Capture states for plots
    Freq_Error.append([Phase_Next_state])
    # Inst_Phase.append([phase])
    # Inst_Volt.append([E])

    return Next_state


def Display_data(return_state, ts):
    
    print("Running Display_data")
    # print(return_state)

    # # Display Voltage
    # plt.plot(ts, return_state[:, 4], color = 'dodgerblue', label = 'E_bus1')
    # plt.plot(ts, return_state[:, 5], color = 'limegreen', label = 'E_bus2')
    # plt.plot(ts, return_state[:, 6], color = 'm', label = 'E_bus3')
    # plt.plot(ts, return_state[:, 7], color = 'black', label = 'E_bus4')
    # plt.grid(color='black', linestyle='-', linewidth=1)
    # plt.ylim(0.95, 1.05)
    # plt.xlabel("Time(s)", fontsize=22, style='italic')
    # plt.ylabel('Voltage(p.u.)', fontsize=22, style='italic')
    # plt.xticks(fontsize=32, style='italic')
    # plt.yticks(fontsize=32, style='italic')
    # # plt.legend(fontsize=22)
    # plt.show()

    # # Display Bus Phase Errors
    # plt.plot(ts, np.sin(return_state[:, 0]) - np.sin(return_state[:, 1]), color = 'dodgerblue', label = r'$\theta_{12}^e $')
    # plt.plot(ts, np.sin(return_state[:, 0]) - np.sin(return_state[:, 2]), color = 'limegreen', label = r'$\theta_{14}^e $')
    # plt.plot(ts, np.sin(return_state[:, 0]) - np.sin(return_state[:, 3]), color = 'm', label = r'$\theta_{23}^e $')
    # # plt.ylim(-1.5, 1.5)
    # # plt.autoscale(False)
    # plt.xlabel("Time(s)", fontsize=18, style='italic')
    # plt.ylabel('Phase Error (rads)', fontsize=18, style='italic')
    # plt.xticks(fontsize=18,style='italic')
    # plt.yticks(fontsize=18,style='italic')
    # plt.legend(fontsize=18)
    # plt.show()

    # # Display Bus Phase
    # plt.plot(ts, np.sin(return_state[:,0]), color = 'dodgerblue', label = r'$\theta_{12}^e $')
    # plt.plot(ts, np.sin(return_state[:,1]), color = 'limegreen', label = r'$\theta_{14}^e $')
    # plt.plot(ts, np.sin(return_state[:, 2]), color = 'm', label = r'$\theta_{23}^e $')
    # plt.plot(ts, np.sin(return_state[:, 3]), color = 'b', label = r'$\theta_{43}^e $')
    # # plt.ylim(-1.5, 1.5)
    # # plt.autoscale(False)
    # plt.xlabel("Time(s)", fontsize=18, style='italic')
    # plt.ylabel('Phase Error (rads)', fontsize=18, style='italic')
    # plt.xticks(fontsize=18,style='italic')
    # plt.yticks(fontsize=18,style='italic')
    # plt.legend(fontsize=18)
    # plt.show()

    # # Display Bus Phase
    # plt.plot(ts, return_state[:, 0], color = 'dodgerblue', label = r'$\theta_{12}^e $')
    # plt.plot(ts, return_state[:, 1], color = 'limegreen', label = r'$\theta_{14}^e $')
    # plt.plot(ts, return_state[:, 2], color = 'm', label = r'$\theta_{23}^e $')
    # plt.plot(ts, return_state[:, 3], color = 'b', label = r'$\theta_{43}^e $')
    # # plt.ylim(-1.5, 1.5)
    # # plt.autoscale(False)
    # plt.xlabel("Time(s)", fontsize=18, style='italic')
    # plt.ylabel('Phase Error (rads)', fontsize=18, style='italic')
    # plt.xticks(fontsize=18,style='italic')
    # plt.yticks(fontsize=18,style='italic')
    # plt.legend(fontsize=18)
    # plt.show()

    # Display Bus Phases w.r.t a stationary phase
    plt.plot(ts, return_state[:,0] - return_state[:,1], color = 'dodgerblue', label = r'$\theta_{12}^e $')
    plt.plot(ts, return_state[:,0] - return_state[:,3], color = 'limegreen', label = r'$\theta_{14}^e $')
    plt.plot(ts, return_state[:,1] - return_state[:,2], color = 'm', label = r'$\theta_{13}^e $')
    plt.plot(ts, return_state[:,3] - return_state[:,2], color='b', label=r'$\theta_{43}^e $')
    # plt.ylim(-1.5, 1.5)
    plt.grid(color='black', linestyle='-', linewidth=1)
    plt.autoscale(False)
    plt.xlabel("Time(s)", fontsize=18, style='italic')
    plt.ylabel('Phase Error (rads)', fontsize=18, style='italic')
    plt.xticks(fontsize=28,style='italic')
    plt.yticks(fontsize=28,style='italic')
    plt.legend(fontsize=18)
    plt.show()

    pass


def main():

    # Create Inverters in an object list...
    global Inverters
    Inverters = []
    # def __(ni, mi, tao, Prated, wn, Ei, init_Phase)
    Inverters.append(Inverter(86.36, 0.5, 0.01, 0.5, 377, 1.0, -0.25))
    Inverters.append(Inverter(143.94, 0.833, 0.01, 0.3, 377, 1.0, 0.15))
    Inverters.append(Inverter(71.97, 0.4167, 0.01, 0.6, 377, 1.0, 0.0))
    Inverters.append(Inverter(43.18, 0.25, 0.01, 1.0, 377, 1.0, -0.38))
    Init_Inverters(Inverters)
    print(Inverters[0].Pnom)

    # Create Network with loads and admittances(complex_rectangular)...
    # Loads at each bus (Purely Resistive Loading)
    L1 = np.complex(0.4, 0.44)
    L2 = np.complex(0.24, 0.132)
    L3 = np.complex(0.48, 0.264)
    L4 = np.complex(0.8, 0.22)
    # Define Network size
    Y = np.zeros((len(Inverters),len(Inverters)))
    # Note: Coupling impedance is defined in network_coupling()
    Init_Network(L1, L2, L3, L4)

    # Specify time row vector for simulation
    # Run Simulation...
    t = np.linspace(0.0, 0.0001, 5000)
    # t = np.linspace(0.1, 5.0, 5000)
    Run_Simulation(t)

    print("End of Simulation!")

    pass


if __name__ == '__main__':
    main()