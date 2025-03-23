from datetime import datetime
from dateutil.relativedelta import relativedelta
from selic_mensal import selic_mensal

# Dicionário de meses para garantir compatibilidade com qualquer locale
MESES_PT = {
    "jan": "Jan", "fev": "Feb", "mar": "Mar", "abr": "Apr", "mai": "May", "jun": "Jun",
    "jul": "Jul", "ago": "Aug", "set": "Sep", "out": "Oct", "nov": "Nov", "dez": "Dec"
}


def converter_mes_ano(mes_ano):
    """Converte uma string no formato 'mmm/aa' para um formato compatível com datetime."""
    mes, ano = mes_ano.split("/")
    mes_convertido = MESES_PT.get(mes.lower())
    if not mes_convertido:
        raise ValueError(f"Mês inválido: {mes}")
    return datetime.strptime(f"{mes_convertido}/{ano}", "%b/%y")


def adicionar_um_mes(data):
    """Adiciona um mês a uma data."""
    return data + relativedelta(months=1)


def calcular_selic_acumulada(selic_mensal, mes_inicial):
    """
    Calcula a soma das porcentagens SELIC de um determinado mês até o mês anterior ao mês atual.

    Args:
        selic_mensal (dict): Dicionário com os meses no formato "mmm/aa" como chave e as taxas SELIC como valores.
        mes_inicial (str): Mês inicial do período no formato "mmm/aa".

    Returns:
        float: Soma das taxas SELIC no período especificado.
    """
    try:
        # Converter chaves para datetime e ordenar corretamente
        meses_ordenados = sorted(selic_mensal.keys(), key=converter_mes_ano)
        selic_ordenada = {mes: selic_mensal[mes] for mes in meses_ordenados}

        # Converter o mês inicial para datetime
        data_inicial = converter_mes_ano(mes_inicial)

        # Adicionar um mês ao mês inicial
        data_inicial = adicionar_um_mes(data_inicial)
        mes_inicial = data_inicial.strftime("%b/%y").lower()

        # Calcular o mês anterior ao mês atual
        data_atual = datetime.now()
        data_final = data_atual - relativedelta(months=-1)
        mes_final = data_final.strftime("%b/%y").lower()
    except ValueError as e:
        raise ValueError(f"Erro ao converter datas: {e}")

    # if mes_inicial not in selic_ordenada:
    #     raise ValueError(f"Mês inicial inválido: {mes_inicial}")

    # Ajustar o mês final para o último mês disponível no dicionário, se necessário
    while mes_final not in selic_ordenada:
        data_final -= relativedelta(months=1)
        mes_final = data_final.strftime("%b/%y").lower()

    if data_inicial > data_final:
        raise ValueError(
            "O mês inicial deve ser anterior ou igual ao mês final.")

    # Cria uma lista com os meses do período selecionado
    meses_periodo = [mes for mes in meses_ordenados if data_inicial <= converter_mes_ano(mes) <= data_final]

    # Soma as porcentagens SELIC dos meses do período
    selic_periodo = sum(selic_ordenada[mes] for mes in meses_periodo)

    return selic_periodo


def calcular_valor_cedivel(valor_bruto, selic_periodo, percentual_honorario, rra=0.03):
    # Faz o calculo da Selic e soma com o valor bruto
    selic_valor = valor_bruto * (selic_periodo / 100)
    valor_liquido = valor_bruto + selic_valor

    # Desconta o valor do RRA e o percentual do honorário
    valor_rra = valor_liquido * rra
    valor_recebido = valor_liquido - \
        (valor_liquido * (percentual_honorario / 100)) - valor_rra

    # Retorna o valor final arredondado
    return round(valor_recebido, 2)


# Solicitar entrada do usuário
mes_inicial = input(
    "Coloque o mês inicial [Deve seguir o seguinte formato: 'out/24']: ")
valor_bruto = float(input("Coloque o valor bruto do precatório: "))
percentual_honorario = float(input("Coloque o percentual de honorário: "))

try:
    # Calcular a SELIC acumulada
    selic_periodo = calcular_selic_acumulada(selic_mensal, mes_inicial)
    print(
        f"A soma da SELIC de {mes_inicial} até o mês anterior ao mês atual é: {selic_periodo:.2f}%")

    # Calcular o valor cedível
    valor_cedivel = calcular_valor_cedivel(
        valor_bruto, selic_periodo, percentual_honorario)
    print(f"O valor cedível é: {round(valor_cedivel):.2f}")
except ValueError as e:
    print(f"Erro: {e}")
