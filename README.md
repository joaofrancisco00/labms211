# Projeto 1 - MS211

Este repositorio consta com a resolucao para os temas "1. Sistema de ponto flutuante e aritmética de máquina" e "2. Zeros de funções de uma variável". Para Cada um deles, segue o modo de replicar os experimentos e a estrutura de organizcao do repositorio.

## Como Replicar os Experimentos

Para o Primeiro tema, basta acessar o diretorio `tema1`:

```bash
cd tema1/
```

Dentro dele sera possivel acessar as imagens do grafico de crescimento do espacamento entre blocos em `espacamento_F10_2_-1_2.png` e tambem a visualizacao da reta tracada, que simula o espaco de `F` sobre a reta real, em `reta_F10_2_-1_2.png`.

```bash
cd figuras/
```

Os arquivos `.py` se dividem em, `f.py` para a classe F e seus metodos e `tester.py` para os unittest para o sistema dado. De modo a executar e ver os outputs do testes, basta acessar `tema1/`:

```bash
python3 -m venv venv
```

Para criar o ambiente virtual;

```bash
source venv/bin/activate
```

Para ativar o venv;

```bash
pip install -r requirements.txt
```

Para instalar as bibliotecas necessarias (matplotlib)

```bash
python3 -m unittest -v tester
```

Para executar o tester, o output estara disponivel em `resultados.txt` que ja encontra-se no repositorio para facilitar o acesso.
