import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

def calculate():
    try:
        # 获取用户输入的变量
        D = float(D_entry.get())
        E = float(E_entry.get())
        L = float(L_entry.get())
        G = float(G_entry.get())
        P1 = float(P1_entry.get())
        P2 = float(P2_entry.get())
        P3 = float(P3_entry.get())
        Ppv = float(Ppv_entry.get())
        Pload = float(Pload_entry.get())
        Pbess = float(Pbess_entry.get())
        Pdiesel = float(Pdiesel_entry.get())
        Pupper_grid_limit = float(Pupper_grid_limit_entry.get())
        t1 = float(t1_entry.get())
        t2 = float(t2_entry.get())
        t3 = float(t3_entry.get())
        t = float(t_entry.get())
        A1 = float(A1_entry.get())
        T = float(T_entry.get())
        C = float(C_entry.get())
        I = float(I_entry.get())
        K = float(K_entry.get())
        upper_grid_status = int(upper_grid_status_var.get())

        # 计算耗电量和工作量
        W1 = P1 * t1  # 电动汽车耗电量
        W2 = P2 * t2  # 慢充充电桩工作量
        W3 = P3 * t3  # 快充充电桩工作量

        # 判断充电桩系统运行模式
        if W1 <= W2:
            if W1 == 0:
                charging_mode = '第一种运行模式'
                F = W2 * (D - G) + W3 * (D - G) + W3 * (D - L)
            else:
                charging_mode = '第二种运行模式'
                F = (W2 - W1) * (D - G) + W3 * (D - G) + W3 * (D - L)
        else:
            W4 = W1 - W2  # 剩余电动汽车耗电量
            if W4 <= W3:
                charging_mode = '第三种运行模式'
                F = (W4 - W3) * (D - L) + W3 * (D - G)
            else:
                W5 = W3 - (W4 - W3)  # 剩余电动汽车耗电量
                charging_mode = '第四种运行模式'
                F = (W3 - W5) * (D - G)

        # 光伏发电和负荷功率
        Wpv = Ppv * t
        Wload = Pload * t
        Wbess = Pbess * t
        Wdiesel = Pdiesel * t
        upper_grid_limit = Pupper_grid_limit * t

        # 整体设备购买成本和年平均成本
        A = (A1 + A1 * 0.03 * T) / (T * 365)

        # 判断光伏发电系统运行模式
        if Wload >= 0 and Wload <= 8:
            if Wpv >= 0 and Wpv <= 12:
                if 8 <= Wpv and Wpv <= 12:
                    if Wpv - Wload <= 4:
                        system_mode = '第三种运行模式'
                        X = A
                        Y = (Wpv - Wload) * D + F
                        SCR = 100
                        SSR = (Wpv / Wload) * 100
                        Emission = 0
                        Gas = 0
                    else:
                        Wbess = 4
                        if upper_grid_status == 1:
                            if Wpv - Wload - Wbess <= upper_grid_limit:
                                system_mode = '第四种运行模式'
                                X = A
                                Y = Wbess * D + (Wpv - Wload - Wbess) * E + F
                                SCR = 100
                                SSR = (Wpv / Wload) * 100
                                Emission = 0
                                Gas = 0
                            else:
                                system_mode = '第五种运行模式'
                                X = A
                                Y = Wbess * D + upper_grid_limit * E + F
                                SCR = ((Wload + Wbess + upper_grid_limit) / Wpv) * 100
                                SSR = ((Wload + Wbess + upper_grid_limit) / Wload) * 100
                                Emission = 0
                                Gas = 0
                        else:
                            system_mode = '第六种运行模式'
                            X = A
                            Y = Wbess * D + F
                            SCR = ((Wload + Wbess) / Wpv) * 100
                            SSR = ((Wload + Wbess) / Wload) * 100
                            Emission = 0
                            Gas = 0
                else:
                    if Wpv < 5:
                        if upper_grid_status == 1:
                            system_mode = '第七种运行模式'
                            X = A + (Wload - Wpv) * E
                            Y = F
                            SCR = 100
                            SSR = (Wpv / Wload) * 100
                            Emission = (Wload - Wpv) * I
                            Gas = 0
                        else:
                            if Wdiesel > 0 and Wdiesel <= 5:
                                system_mode = '第八种运行模式'
                                X = A + (Wload - Wpv) * 1000 * 0.2 * C
                                Y = F
                                SCR = 100
                                SSR = (Wpv / Wload) * 100
                                Emission = 0
                                Gas = (Wload - Wpv) * 1000 * 0.2 * K
                            else:
                                system_mode = '第九种运行模式'
                    elif Wpv >= 5 and Wpv < 8:
                        if Wpv >= Wload:
                            system_mode = '第十种运行模式'
                            X = A
                            Y = (Wpv - Wload) * D + F
                            SCR = 100
                            SSR = (Wpv / Wload) * 100
                            Emission = 0
                            Gas = 0
                        else:
                            if upper_grid_status == 1:
                                system_mode = '第十一种运行模式'
                                X = A + (Wload - Wpv) * E
                                Y = F
                                SCR = 100
                                SSR = (Wpv / Wload) * 100
                                Emission = (Wload - Wpv) * I
                                Gas = 0
                            else:
                                if Wdiesel > 0 and Wdiesel <= 5:
                                    system_mode = '第十二种运行模式'
                                    X = A + (Wload - Wpv) * 1000 * 0.2 * C
                                    Y = F
                                    SCR = 100
                                    SSR = (Wpv / Wload) * 100
                                    Emission = 0
                                    Gas = (Wload - Wpv) * 1000 * 0.2 * K
                                else:
                                    system_mode = '第十三种运行模式'
            else:
                system_mode = '第二种运行模式'
        else:
            system_mode = '第一种运行模式'

        # 输出结果
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f'1充电桩系统的运行模式: {charging_mode}\n')
        result_text.insert(tk.END, f'2充电桩系统的收益: {F:.2f}\n')
        result_text.insert(tk.END, f'3光储联合系统的运行模式: {system_mode}\n')
        result_text.insert(tk.END, f'4园区微电网系统的经济性(成本，收益): {X:.2f}, {Y:.2f}\n')
        result_text.insert(tk.END, f'5园区微电网系统的节能性(SCR，SSR): {SCR:.2f}%, {SSR:.2f}%\n')
        result_text.insert(tk.END, f'6园区微电网系统的环保性(碳排量，烟气量): {Emission:.2f}, {Gas:.2f}\n')

    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

# 创建主窗口
window = tk.Tk()
window.title("园区微电网系统模拟")

# 加载背景图片
background_image = Image.open("园区微电网系统模拟.png")
background_image = background_image.resize((1000, int(background_image.height * 1000 / background_image.width)))
background_image = ImageTk.PhotoImage(background_image)

# 创建一个标签用来显示背景图片
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# 创建标签和输入框
D_label = tk.Label(window, text="峰时电价(D):")
D_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
D_entry = tk.Entry(window)
D_entry.grid(row=0, column=1, padx=5, pady=5)

E_label = tk.Label(window, text="平均电价(E):")
E_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
E_entry = tk.Entry(window)
E_entry.grid(row=1, column=1, padx=5, pady=5)

L_label = tk.Label(window, text="平时电价(L):")
L_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
L_entry = tk.Entry(window)
L_entry.grid(row=2, column=1, padx=5, pady=5)

G_label = tk.Label(window, text="谷时电价(G):")
G_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
G_entry = tk.Entry(window)
G_entry.grid(row=3, column=1, padx=5, pady=5)

P1_label = tk.Label(window, text="电动汽车耗电功率(P1):")
P1_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
P1_entry = tk.Entry(window)
P1_entry.grid(row=0, column=3, padx=5, pady=5)

P2_label = tk.Label(window, text="慢充充电桩工作功率(P2):")
P2_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
P2_entry = tk.Entry(window)
P2_entry.grid(row=1, column=3, padx=5, pady=5)

P3_label = tk.Label(window, text="快充充电桩工作功率(P3):")
P3_label.grid(row=2, column=2, padx=5, pady=5, sticky="e")
P3_entry = tk.Entry(window)
P3_entry.grid(row=2, column=3, padx=5, pady=5)

Ppv_label = tk.Label(window, text="光伏发电功率(Ppv):")
Ppv_label.grid(row=3, column=2, padx=5, pady=5, sticky="e")
Ppv_entry = tk.Entry(window)
Ppv_entry.grid(row=3, column=3, padx=5, pady=5)

Pload_label = tk.Label(window, text="负荷消耗功率(Pload):")
Pload_label.grid(row=0, column=4, padx=5, pady=5, sticky="e")
Pload_entry = tk.Entry(window)
Pload_entry.grid(row=0, column=5, padx=5, pady=5)

Pbess_label = tk.Label(window, text="电池储能系统功率(Pbess):")
Pbess_label.grid(row=1, column=4, padx=5, pady=5, sticky="e")
Pbess_entry = tk.Entry(window)
Pbess_entry.grid(row=1, column=5, padx=5, pady=5)

Pdiesel_label = tk.Label(window, text="柴油机工作功率(Pdiesel):")
Pdiesel_label.grid(row=2, column=4, padx=5, pady=5, sticky="e")
Pdiesel_entry = tk.Entry(window)
Pdiesel_entry.grid(row=2, column=5, padx=5, pady=5)

Pupper_grid_limit_label = tk.Label(window, text="上级电网回收限制(Pupper_grid_limit):")
Pupper_grid_limit_label.grid(row=3, column=4, padx=5, pady=5, sticky="e")
Pupper_grid_limit_entry = tk.Entry(window)
Pupper_grid_limit_entry.grid(row=3, column=5, padx=5, pady=5)

t1_label = tk.Label(window, text="电动汽车耗电时间(t1):")
t1_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
t1_entry = tk.Entry(window)
t1_entry.grid(row=4, column=1, padx=5, pady=5)

t2_label = tk.Label(window, text="慢充充电桩工作时间(t2):")
t2_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
t2_entry = tk.Entry(window)
t2_entry.grid(row=5, column=1, padx=5, pady=5)

t3_label = tk.Label(window, text="快充充电桩工作时间(t3):")
t3_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
t3_entry = tk.Entry(window)
t3_entry.grid(row=6, column=1, padx=5, pady=5)

t_label = tk.Label(window, text="时间(t):")
t_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
t_entry = tk.Entry(window)
t_entry.grid(row=7, column=1, padx=5, pady=5)

A1_label = tk.Label(window, text="整体设备购买成本(A1):")
A1_label.grid(row=4, column=2, padx=5, pady=5, sticky="e")
A1_entry = tk.Entry(window)
A1_entry.grid(row=4, column=3, padx=5, pady=5)

T_label = tk.Label(window, text="设备平均使用年限(T):")
T_label.grid(row=5, column=2, padx=5, pady=5, sticky="e")
T_entry = tk.Entry(window)
T_entry.grid(row=5, column=3, padx=5, pady=5)

C_label = tk.Label(window, text="柴油单价(C):")
C_label.grid(row=6, column=2, padx=5, pady=5, sticky="e")
C_entry = tk.Entry(window)
C_entry.grid(row=6, column=3, padx=5, pady=5)

I_label = tk.Label(window, text="外购电的碳排放量因子(I):")
I_label.grid(row=7, column=2, padx=5, pady=5, sticky="e")
I_entry = tk.Entry(window)
I_entry.grid(row=7, column=3, padx=5, pady=5)

K_label = tk.Label(window, text="消耗单位柴油产生烟气量(K):")
K_label.grid(row=4, column=4, padx=5, pady=5, sticky="e")
K_entry = tk.Entry(window)
K_entry.grid(row=4, column=5, padx=5, pady=5)

upper_grid_status_var = tk.IntVar(value=1)
upper_grid_status_radio1 = tk.Radiobutton(window, text="上级电网状态: 正常", variable=upper_grid_status_var, value=1)
upper_grid_status_radio1.grid(row=5, column=4, padx=5, pady=5, sticky="e")
upper_grid_status_radio2 = tk.Radiobutton(window, text="上级电网状态: 故障", variable=upper_grid_status_var, value=0)
upper_grid_status_radio2.grid(row=6, column=4, padx=5, pady=5, sticky="e")

# 创建计算按钮
calculate_button = tk.Button(window, text="计算", command=calculate)
calculate_button.grid(row=8, column=0, columnspan=6, padx=5, pady=5)

# 创建结果文本框
result_text = tk.Text(window, wrap=tk.WORD, height=10, width=80)
result_text.grid(row=9, column=0, columnspan=6, padx=5, pady=5)

# 运行主循环
window.mainloop()
