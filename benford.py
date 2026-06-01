"""import pandas as pd
import math
from collections import Counter

# ==========================
# Leitura do arquivo
# ==========================

arquivo = "dados.csv"

try:
    df = pd.read_csv(arquivo)
except FileNotFoundError:
    print(f"Arquivo '{arquivo}' não encontrado.")
    exit()

print(f"\nArquivo carregado: {arquivo}")

# ==========================
# Escolha da coluna
# ==========================

print("\nColunas disponíveis:")
print(df.columns.tolist())

coluna = input("\nDigite o nome da coluna a ser analisada: ")

if coluna not in df.columns:
    print("Coluna não encontrada.")
    exit()

# ==========================
# Extração dos primeiros dígitos
# ==========================

primeiros_digitos = []

for valor in df[coluna]:

    # Ignora valores nulos
    if pd.isna(valor):
        continue

    valor_str = str(abs(valor))

    for caractere in valor_str:
        if caractere.isdigit() and caractere != '0':
            primeiros_digitos.append(int(caractere))
            break

if len(primeiros_digitos) == 0:
    print("Nenhum número válido encontrado na coluna.")
    exit()

# ==========================
# Distribuição observada
# ==========================

contagem = Counter(primeiros_digitos)
total = len(primeiros_digitos)

observado = {}

for digito in range(1, 10):
    observado[digito] = contagem[digito] / total * 100

# ==========================
# Distribuição Benford
# ==========================

benford = {}

for digito in range(1, 10):
    benford[digito] = math.log10(1 + 1 / digito) * 100

# ==========================
# Exibição dos resultados
# ==========================

print("\n" + "=" * 45)
print("ANÁLISE DA LEI DE BENFORD")
print("=" * 45)

print(f"\nColuna analisada: {coluna}")
print(f"Quantidade de registros válidos: {total}")

print("\nDígito | Observado (%) | Benford (%)")
print("-" * 38)

desvio_total = 0

for digito in range(1, 10):

    obs = observado[digito]
    esp = benford[digito]

    desvio_total += abs(obs - esp)

    print(
        f"{digito:^6} | "
        f"{obs:>11.2f} | "
        f"{esp:>10.2f}"
    )

# ==========================
# Conclusão preliminar
# ==========================

print("\n" + "-" * 38)
print(f"Desvio Total: {desvio_total:.2f}")

if desvio_total < 10:
    conclusao = "Boa aderência à Lei de Benford"
elif desvio_total < 20:
    conclusao = "Aderência moderada à Lei de Benford"
else:
    conclusao = "Baixa aderência à Lei de Benford"

print(f"\nConclusão: {conclusao}")

"""

import pandas as pd
import math
from collections import Counter


def analisar_benford(df, coluna):

    if coluna not in df.columns:
        raise ValueError("Coluna não encontrada")

    primeiros_digitos = []

    for valor in df[coluna]:

        if pd.isna(valor):
            continue

        valor_str = str(abs(valor))

        for caractere in valor_str:
            if caractere.isdigit() and caractere != "0":
                primeiros_digitos.append(int(caractere))
                break

    if len(primeiros_digitos) == 0:
        raise ValueError("Nenhum número válido encontrado")

    contagem = Counter(primeiros_digitos)
    total = len(primeiros_digitos)

    observado = {}

    for digito in range(1, 10):
        observado[str(digito)] = round(
            contagem[digito] / total * 100,
            2
        )

    benford = {}

    for digito in range(1, 10):
        benford[str(digito)] = round(
            math.log10(1 + 1 / digito) * 100,
            2
        )

    desvio_total = 0

    for digito in range(1, 10):
        desvio_total += abs(
            observado[str(digito)]
            - benford[str(digito)]
        )

    if desvio_total < 10:
        conclusao = "Boa aderência à Lei de Benford"
    elif desvio_total < 20:
        conclusao = "Aderência moderada à Lei de Benford"
    else:
        conclusao = "Baixa aderência à Lei de Benford"


    # Calculo Mad
    mad = 0

    for digito in range(1, 10):
        mad += abs(
            (observado[str(digito)] / 100)
            - (benford[str(digito)] / 100)
        )

    mad = mad / 9


    #Calculo qui quadrado
    qui_quadrado = 0

    for digito in range(1, 10):
        observado_qtd = contagem[digito]

        esperado_qtd = (
                               benford[str(digito)] / 100
                       ) * total

        qui_quadrado += (
                                (observado_qtd - esperado_qtd) ** 2
                        ) / esperado_qtd

    if mad < 0.006:
        classificacao_mad = "Conformidade próxima"

    elif mad < 0.012:
        classificacao_mad = "Conformidade aceitável"

    elif mad < 0.015:
        classificacao_mad = "Conformidade marginal"

    else:
        classificacao_mad = "Não conformidade"

    return {
        "coluna": coluna,
        "registros_validos": total,
        "observado": observado,
        "benford": benford,

        "desvio_total": round(desvio_total, 2),
        "conclusao": conclusao,

        "mad": round(mad, 6),
        "classificacao_mad": classificacao_mad,

        "qui_quadrado": round(
            qui_quadrado,
            4
        ),

        "valor_critico": 15.51,

        "digitos": [1, 2, 3, 4, 5, 6, 7, 8, 9],

        "observado_lista": [
            observado[str(i)]
            for i in range(1, 10)
        ],

        "benford_lista": [
            benford[str(i)]
            for i in range(1, 10)
        ]
    } 