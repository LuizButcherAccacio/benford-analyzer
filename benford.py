import pandas as pd
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