import math
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import raizes

DIRETORIO_LOCAL = os.path.dirname(os.path.abspath(__file__))

def iterar_newton_arctg(x0, max_iter=10):
    historico = [x0]
    for _ in range(max_iter):
        try:
            x = historico[-1]
            x_prox = x - (1 + x**2) * math.atan(x)
            historico.append(x_prox)
        except OverflowError:
            historico.append(float('inf'))
            break

    while len(historico) < max_iter + 1:
        historico.append(float('inf'))
    return historico

def criar_tabela(nome_metodo, salvar_latex=True):
    x0 = [0.5, 1, 1.3, 1.4, 1.5, 2]

    dados = {"k": list(range(11))}

    for valor in x0:
        historico = iterar_newton_arctg(valor, max_iter=10)
        dados[f"x0={valor}"] = historico
    
    tabela = pd.DataFrame(dados)

    formatadores = {"k": "{:d}".format}
    for valor in x0:
        formatadores[f"x0={valor}"] = "{:.4e}".format

    print(f"\n{'='*55}\nTabela - Método: {nome_metodo}\n{'='*55}")
    print(tabela.to_string(index=False, formatters=formatadores, line_width=1000))
    
    if salvar_latex:
        tabela.to_latex(os.path.join(DIRETORIO_LOCAL, f"{nome_metodo}.tex"), index=False, formatters=formatadores)
    
    return tabela


def gerar_grafico_semilog(x0_lista=[0.5, 1, 1.3, 1.4, 1.5, 2]):
    plt.figure(figsize=(9, 5))
    
    estilos = ['o-', 's-', '^-', 'v-', 'd-', 'x-']
    
    for i, x0 in enumerate(x0_lista):
        hist = iterar_newton_arctg(x0, max_iter=10)
        
        k_vals = []
        mod_x = []
        for k, x in enumerate(hist):
            val = abs(x)
            if 0 < val < float('inf'):
                k_vals.append(k)
                mod_x.append(val)
                
        plt.plot(k_vals, mod_x, estilos[i % len(estilos)], label=f"$x_0 = {x0}$")

    plt.yscale('log')

    plt.xlabel("Iteração ($k$)", fontsize=11)
    plt.ylabel(r"$|x_k|$ (escala logarítmica)", fontsize=11)
    plt.title(r"Localidade de Newton para $g(x) = \text{arctg}(x)$ — Caso 2(a)", fontsize=12)
    plt.grid(True, which="both", linestyle=":", alpha=0.6)
    plt.legend(fontsize=9, loc='center left', bbox_to_anchor=(1, 0.5))

    caminho_grafico = os.path.join(DIRETORIO_LOCAL, "grafico_caso2_semilog.png")
    plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo em: {caminho_grafico}")

    plt.show()

def calcular_limiar_x_estrela():
    h = lambda x: 2*x - (1 + x**2) * math.atan(x)
    
    res = raizes.calc_bisection(h, 1.0, 1.5, tol=1e-10)
    x_estrela = res["history"][-1]
    
    print(f"\n{'='*55}")
    print("Item (b) — Ponto Limiar de Fronteira (x*)")
    print(f"{'='*55}")
    print(f"x* encontrado: {x_estrela:.10f}")
    print(f"Iterações da Bissecção: {res['iteration']}")
    print(f"Resíduo h(x*): {h(x_estrela):.4e}")
    print(f"{'='*55}\n")
    
    return x_estrela


def testar_tres_regimes(x_estrela):
    
    casos = {
        "|x0| < x* (1.20)": 1.20,
        "|x0| < x* (1.35)": 1.35,
        "|x0| = x* (+x*)": x_estrela,
        "|x0| = x* (-x*)": -x_estrela,
        "|x0| > x* (1.45)": 1.45,
        "|x0| > x* (1.80)": 1.80,
    }
    
    max_k = 25 
    dados = {"k": list(range(max_k + 1))}
    formatadores = {"k": "{:d}".format}
    
    for rotulo, val in casos.items():
        hist = iterar_newton_arctg(val, max_iter=max_k)
        dados[rotulo] = hist
        formatadores[rotulo] = "{:.4e}".format
        
    df_regimes = pd.DataFrame(dados)
    
    print(f"\n{'='*85}\nTabela dos 3 Regimes — Item (c)\n{'='*85}")
    print(df_regimes.to_string(index=False, formatters=formatadores, line_width=1000))
    
    caminho_tex = os.path.join(DIRETORIO_LOCAL, "tabela_caso2_regimes.tex")
    df_regimes.to_latex(caminho_tex, index=False, formatters=formatadores)
    print(f"\nTabela dos regimes salva em: {caminho_tex}")
    
    return df_regimes


criar_tabela("Newton_arctg", salvar_latex=True)

x_estrela = calcular_limiar_x_estrela()
df_regimes = testar_tres_regimes(x_estrela)

gerar_grafico_semilog()