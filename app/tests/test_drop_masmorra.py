from data.masmorras import MASMORRAS


def __testar_masmorra(masmorra, item_esperado):
    tentativas = []
    for n in range(100):
        item = None
        __tentativas = 0
        masmorra.passos = 1
        while item == None or item.nome != item_esperado.nome:
            masmorra.passos = min(masmorra.total_passos, masmorra.passos+1)
            item = masmorra.item_aleatorio()
            __tentativas += 1
        tentativas.append(__tentativas)
    return sum(tentativas)/len(tentativas)


def test_drop_primeiro_item():
    medias_primeiro_item = []
    for _, masmorra in MASMORRAS.items():
        if masmorra.lista_itens:
            medias_primeiro_item.append(
                __testar_masmorra(
                    masmorra,
                    masmorra.lista_itens[0][1]
                )
            )
    assert not any([m < 10 for m in medias_primeiro_item])
    assert not any([m > 50 for m in medias_primeiro_item])


def test_drop_ultimo_item():
    medias_ultimo_item = []
    for masmorra_nome, masmorra in MASMORRAS.items():
        if masmorra.lista_itens:
            medias_ultimo_item.append(
                __testar_masmorra(
                    masmorra,
                    masmorra.lista_itens[-1][1]
                )
            )

    assert not any([m < 45 for m in medias_ultimo_item])
    assert not any([m > 320 for m in medias_ultimo_item])
