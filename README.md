# Projeto 1 - MS211

Este repositorio consta com a resolucao para os temas:
- "1. Sistema de ponto flutuante e aritmética de máquina";
- "2. Zeros de funções de uma variável";

## Como Replicar os Experimentos

Dado que voce encontra-se no root do repositorio, para criar o ambiente virtual, rode:

```bash
python3 -m venv venv
```

Para ativar o venv:

```bash
source venv/bin/activate
```

Para instalar as bibliotecas necessarias que valem tanto para `tema1` quanto `tema2`:

```bash
pip install -r requirements.txt
```

### Tema 1

Para o Primeiro tema, basta acessar o diretorio `tema1` com:

```bash
cd tema1/
```

Ja dentro do diretorio principal, a estrutura subdivide-se em:
- Arquivos `.py` que se dividem em, `f.py` para a classe F e seus metodos e `tester.py` para os unittest para o sistema dado;
- Imagens do grafico de crescimento do espacamento entre blocos em `espacamento_F10_2_-1_2.png` e tambem a visualizacao da reta tracada, que simula o espaco de `F` sobre a reta real, em `reta_F10_2_-1_2.png` basta:

```bash
cd graphs/
```

De modo a executar e ver os outputs verbais e/ou gerar os graficos dos testes, basta acessar `tema1/` novamente com:

```bash
cd ..
```

Para executar o tester execute: 

```bash
python3 -m unittest -v tester
```

o output verbal estara disponivel em `resultados.txt` que ja encontra-se no repositorio para facilitar o acesso.

### Tema 2

Para o segundo e ultimo tema, basta acessar a pasta referente a ele:

```bash
cd tema2/
```

Dentro desse repositorio, constam:
- Dois arquivos executaveis `.py` com cada um dos casos para rodar os testes, basta rodar `python3 caso1.py` ou `python3 caso2.py`;
- Arquivo `raizes.py` com os metodos para achar os zeros da funcao (newton, secante e bissecao);
- Tabelas em `.tex`, dentro de `tables/`, que sao os resultados a cada iteracao;
- Graficos em `.png`, dentro de `graphs/`, que expoe a evolucao dos modelos a cada iteracao (k).
