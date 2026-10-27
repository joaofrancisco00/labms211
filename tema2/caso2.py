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

criar_tabela("Newton_arctg", salvar_latex=True)

gerar_grafico_semilog()