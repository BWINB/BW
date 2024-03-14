from handcalcs.decorator import handcalc


@handcalc(jupyter_display=True)
def ld (g_k,q_k):
    N_d_1 = 1.15*g_k + 1.5*q_k
    N_d_2 = 1.35*g_k
    N_d = max(N_d_1,N_d_2)
    return N_d