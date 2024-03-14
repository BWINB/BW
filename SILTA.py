def BW_draw_silta_kork(user_jv):
    import matplotlib.pyplot as plt

    def h_laattasilta(jm):
        h = 0.63 + 0.4 * (jm / 10 - 1)
        return h

    def h_palkkisilta(jm):
        h = 1.1 + 1.1 * ((jm - 10)/30)
        return h

    l_h_laattasilta = []
    l_h_palkkisilta = []

    for i in range(50):
        h_laatti = h_laattasilta(i)
        h_palkki = h_palkkisilta(i)

        l_h_laattasilta.append(h_laatti)
        l_h_palkkisilta.append(h_palkki)

        #print('JV = {}m, Laattasilta h = {:.2f}m, Palkkisilta h = {:.2f}m'.format(i, h_laatti, h_palkki))



    # Laske laattasilta ja palkkisilta korkeudet käyttäjän jännevälin kohdalla
    user_h_laattasilta = h_laattasilta(user_jv)
    user_h_palkkisilta = h_palkkisilta(user_jv)

    # Laske ja tulosta siltojen ero
    ero = user_h_laattasilta - user_h_palkkisilta
    #print('Laattasilta - Palkkisilta ero kohdassa JV = {:.2f}m: {:.2f}m'.format(user_jv, ero))

    # Luo kaavio
    plt.plot(range(50), l_h_laattasilta, label='Laattasilta', linestyle='-', marker='')
    plt.plot(range(50), l_h_palkkisilta, label='Palkkisilta', linestyle='-', marker='')
    plt.plot([user_jv,user_jv], [0,2.5],  label='Oma jänneväli ',linestyle='--', marker='')
    #plt.plot(user_jv, user_h_palkkisilta, 'go', label='Oma jänneväli (Palkkisilta)')

    plt.plot(user_jv, user_h_laattasilta, 'ro')
    plt.plot(user_jv, user_h_palkkisilta, 'go')

    plt.text(user_jv-2, user_h_palkkisilta, f'h = {user_h_palkkisilta:.2f}m', ha='right', va='bottom')

    plt.text(user_jv+10, user_h_laattasilta-0.1, f'h = {user_h_laattasilta:.2f}m', ha='right', va='bottom')


    plt.xlabel('JV (m)')
    plt.ylabel('h (m)')
    plt.title('Korkeus h vs. JV')
    #plt.grid(True)
    plt.legend()
    plt.show()
    # Näytä kaavio
    print('Laattasilta - Palkkisilta ero kohdassa JV = {:.2f}m: {:.2f}m'.format(user_jv, ero)),print('JV = {}m, Laattasilta h = {:.2f}m, Palkkisilta h = {:.2f}m'.format(user_jv, user_h_laattasilta, user_h_palkkisilta))
    print(f"""
          
        h_laattasilta  ==> h = 0.63 + 0.4 * (jm / 10 - 1)
        h_palkkisilta  ==> h = 1.1 + 1.1 * ((jm - 10)/30)
          
          """)




