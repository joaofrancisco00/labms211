import math
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import raizes

# Diretório onde este script está localizado (pasta tema2)
DIRETORIO_LOCAL = os.path.dirname(os.path.abspath(__file__))

f1 = lambda x: x**3 - 3*x + 1
df1 = lambda x: 3*x**2 - 3
alpha = 2 * math.cos(2 * math.pi / 9)


def calcular_raizes():
    res_newton = raizes.calc_newton(f1, df1, 2)
    res_secante = raizes.calc_secante(f1, 1, 2)
    res_bissecao = raizes.calc_bisection(f1, 1, 2)

    return res_newton, res_secante, res_bissecao


def gerar_grafico(res_bis, res_sec, res_newt):

    def obter_k_dk(history):
        k_lista = []
        dk_lista = []
        for k, x in enumerate(history):
            erro = abs(x - alpha)
            if erro > 0:
                k_lista.append(k)
                dk_lista.append(-math.log10(erro))
        return k_lista, dk_lista

    k_bis, dk_bis = obter_k_dk(res_bis["history"])
    k_sec, dk_sec = obter_k_dk(res_sec["history"])
    k_newt, dk_newt = obter_k_dk(res_newt["history"])

    plt.figure(figsize=(9, 5))

    plt.plot(k_bis, dk_bis, marker='o', label='Bissecção', color='tab:blue', markersize=4)
    plt.plot(k_sec, dk_sec, marker='s', label='Secante', color='tab:red', markersize=4)
    plt.plot(k_newt, dk_newt, marker='^', label='Newton', color='tab:green', markersize=4)

    plt.axhline(y=10, color='gray', linestyle='--', linewidth=0.7, label=r"Tolerância ($10^{-10}$)")

    plt.xlabel("Iteração ($k$)", fontsize=11)
    plt.ylabel(r"$d_k = -\log_{10}|x_k - \alpha|$ (dígitos corretos)", fontsize=11)
    plt.title("Evolução dos Dígitos Corretos ($d_k$) — Caso 1", fontsize=12)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(fontsize=10)

    caminho_grafico = os.path.join(DIRETORIO_LOCAL, "grafico_dk_caso1.png")
    plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo como '{caminho_grafico}'")

    plt.show()


def gerar_tabela(nome_metodo, resultado, salvar_latex=True):
    hist = resultado["history"]

    dados = {
        "k": list(range(len(hist))),
        "x_k": hist,
        "|f(x_k)|": [abs(f1(x)) for x in hist],
        "|x_k - alpha|": [abs(x - alpha) for x in hist],
    }
    df = pd.DataFrame(dados)

    formatadores = {
        "k": "{:d}".format,
        "x_k": "{:.10f}".format,
        "|f(x_k)|": "{:.4e}".format,
        "|x_k - alpha|": "{:.4e}".format,
    }

    print(f"\n{'='*55}\nTabela - Método: {nome_metodo}\n{'='*55}")

    print(df.to_string(index=False, formatters=formatadores))

    if salvar_latex:
        metodo_slug = nome_metodo.lower().replace("ç", "c").replace("ã", "a")
        nome_arquivo = os.path.join(DIRETORIO_LOCAL, f"tabela_{metodo_slug}.tex")
        df.to_latex(nome_arquivo, index=False, formatters=formatadores)
        print(f"Tabela LaTeX salva em: {nome_arquivo}")

    return df


def gerar_tabela_resumo(res_bis, res_sec, res_newt):
    resumo = [
        {
            "Método": "Bissecção",
            "Iterações": res_bis["iteration"],
            "Avaliações f": res_bis["count_f"],
            "Avaliações f'": "—",
            "Erro Final": f"{abs(res_bis['history'][-1] - alpha):.4e}",
            "Resíduo Final": f"{abs(f1(res_bis['history'][-1])):.4e}"
        },
        {
            "Método": "Secante",
            "Iterações": res_sec["iteration"],
            "Avaliações f": res_sec["count_f"],
            "Avaliações f'": "—",
            "Erro Final": f"{abs(res_sec['history'][-1] - alpha):.4e}",
            "Resíduo Final": f"{abs(f1(res_sec['history'][-1])):.4e}"
        },
        {
            "Método": "Newton",
            "Iterações": res_newt["iteration"],
            "Avaliações f": res_newt["count_f"],
            "Avaliações f'": res_newt["count_df"],
            "Erro Final": f"{abs(res_newt['history'][-1] - alpha):.4e}",
            "Resíduo Final": f"{abs(f1(res_newt['history'][-1])):.4e}"
        }
    ]
    df_resumo = pd.DataFrame(resumo)
    print(f"\n{'='*65}\nResumo Comparativo dos Métodos\n{'='*65}")
    print(df_resumo.to_string(index=False, line_width=1000))
    caminho_resumo = os.path.join(DIRETORIO_LOCAL, "tabela_resumo.tex")
    df_resumo.to_latex(caminho_resumo, index=False)
    print(f"Tabela Resumo LaTeX salva em: {caminho_resumo}")


def calcular_ordem_assintotica(nome_metodo, resultado, teoria):
    hist = resultado["history"]

    erros = [abs(x - alpha) for x in hist]

    print(f"\n{'='*50}")
    print(f"Ordem Assintótica Estimada (p_k) — {nome_metodo}")
    print(f"Valor Teórico: {teoria}")
    print(f"{'='*50}")
    print(f"{'k':<4} | {'e_k':<12} | {'p_k estimado':<15}")
    print(f"{'-'*50}")

    for k in range(1, len(erros) - 1):
        e_k = erros[k]
        e_k_menos_1 = erros[k - 1]
        e_k_mais_1 = erros[k + 1]

        if e_k_menos_1 > 1e-14 and e_k_mais_1 > 1e-14 and e_k > 1e-14:
            numerador = math.log(e_k_mais_1 / e_k)
            denominador = math.log(e_k / e_k_menos_1)
            p_k_estimado = numerador / denominador if denominador != 0 else float('inf')
            print(f"{k:<4d} | {e_k:<12.4e} | {p_k_estimado:<15.4f}")
    
    print(f"{'-'*50}\n")


res_newton, res_secante, res_bissecao = calcular_raizes()

gerar_tabela("Newton", res_newton) 
gerar_tabela("Secante", res_secante)
gerar_tabela("Bissecção", res_bissecao)

gerar_tabela_resumo(res_bissecao, res_secante, res_newton)

calcular_ordem_assintotica("Newton", res_newton, "2.0000 (Quadrática)")
calcular_ordem_assintotica("Secante", res_secante, "1.6180 (Razão Áurea)")

gerar_grafico(res_bissecao, res_secante, res_newton)

gerar_grafico(res_bissecao, res_secante, res_newton)