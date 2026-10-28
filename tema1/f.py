import matplotlib.pyplot as plt
import math

# Fazer um verificador de entradas como de create element para todas as funcoes

class F :
    def __init__(self, beta, t, m, M):
        self.beta = beta
        self.t = t
        self.m = m
        self.M = M
        self.xmin = beta**(m-1)
        self.xmax = (1 - beta**(-t))*beta**M

    def create_element(self, x: tuple[int, int]) -> tuple[int,int] | None:
        '''cria um elemento a partir de um par (N, e), rejeitando 
        parâmetros inválidos e pares que não pertençam a J × E'''

        if not isinstance(x, tuple) or len(x) != 2:
            return None

        N, e = x

        if type(N) is not int or type(e) is not int:
            return None

        if not ((self.beta**(self.t - 1)) <= abs(N) <= (self.beta**self.t - 1)):
            return None
        
        if (e > self.M or e < self.m):
            return None

        return (N,e)

    def round(self, x:float) -> float | str:
        """fl(x) ∈ F, onde fl : G −→ F é a função de arredondamento 
        com a regra de desempate adotada nas notas de aula (escolhe-se
        o vizinho de maior modulo, mais longe do zero, ou seja, y2)"""

        if (x == 0):
            return 0.0

        if (0 < abs(x) < self.xmin):
            return "underflow"

        if (abs(x) > self.xmax):
            return "overflow"

        s = True
        if (x < 0):
            s = False

        a = abs(x)
        e = math.floor(math.log(abs(x), self.beta)) + 1
        p = self.beta**(e - self.t)
        N = math.floor(a/p)

        y = x
        y1 = N*p
        y2 = (N + 1)*p

        if ((a - y1) < (y2 - a)):
            y = y1
        else:
            y = y2 # empate retorna y2

        if (s):
            return y
        else:
            return -y

    def to_float(self, x: tuple[int,int]) -> float:
        """Dado um numero representado por tupla, retorna
        o mesmo numero em formato de float"""

        N, e = x
        return N * float(self.beta) ** (e - self.t)

    def get_element_form(self, num:float) -> tuple[int,int] | None:
        """obter a representação (N, e) de um elemento.
        Retorna: N: int, e: int"""

        if num == 0:
            return (0,0)

        normalized = abs(num)

        if ((normalized < self.xmin) or (normalized > self.xmax)):
            return None

        e = 0
        while (normalized >= 1):
            normalized /= self.beta
            e += 1

        while (normalized < 1 / self.beta):
            normalized *= self.beta
            e -= 1

        No = self.beta**self.t * normalized
        N = math.floor(No)
        if (abs(N - No)) >= 0.5:
            N += 1

        if N == self.beta**self.t:
            N = self.beta**(self.t - 1)
            e += 1
            if e > self.M:
                return None 

        if num < 0:
            N = -N

        return (N, e)

    def compare_two(self, x: tuple[int, int], y: tuple[int, int]) -> int:
        """comparar dois elementos do mesmo sistema (=, <, >).
        Retorna  -1 se x < y; 0 se x == y; 1 se x > y"""

        Nx, ex = x
        Ny, ey = y

        nx = Nx*self.beta**(ex - self.t)
        ny = Ny*self.beta**(ey - self.t)

        if (nx < ny):
            return -1
        elif (nx == ny):
            return 0
        else:
            return 1

    def get_symmetric(self, x: tuple[int, int]) -> tuple[int,int]:
            """Retorna o simétrico −x de um elemento x"""
            
            N, e = x
            return (-N,e)

    def sum(self, x: tuple[int,int], y: tuple[int,int]) -> tuple[int, int] | None:
        """Dados x,y ∈ F nao nulos com x + y ∈ G, retorna a soma"""

        if (x[0] == 0 or y[0] == 0):
            return None

        Nx, ex = x
        Ny, ey = y

        if (ex < ey):
            x, y = y, x
            Nx, ex = x
            Ny, ey = y

        d = ex - ey
        u = Nx + Ny*self.beta**(-d)
        e = ex - self.t

        if (u == 0):
            return (0,0)

        while (abs(u) >= 1):
            u /= self.beta
            e += 1

        while (abs(u) < 1):
            u *= self.beta
            e -= 1

        return self.round(u*self.beta**e)

    def subtraction(self, x: tuple[int,int], y: tuple[int,int]) -> tuple[int, int] | None:
        """Dados x,y ∈ F nao nulos com x - y ∈ G, retorna a subtracao"""

        return self.sum(x, self.get_symmetric(y))        

    def product(self, x: tuple[int, int], y: tuple[int,int]):
        """Dados x,y ∈ F nao nulos com xy ∈ G, retorna o produto xy"""

        if (x[0] == 0 or y[0] == 0):
            return None

        Nx, ex = x
        Ny, ey = y

        s = ((Nx > 0) == (Ny > 0))
        u = abs(Nx*Ny)
        e = ex + ey - 2*self.t

        if (u < 1/self.beta):
            u *= self.beta
            e -= 1

        if (not s):
            u = -u

        return self.round(u*self.beta**e)

    def division(self, x: tuple[int,int], y: tuple[int,int]) -> float | None:
        """Dados x,y ∈ F nao nulos com x/y ∈ G, retorna o produto x/y"""

        if (x[0] == 0 or y[0] == 0):
            return None

        Nx, ex = x
        Ny, ey = y

        if (Ny == 0):
            return None
        
        s = ((Nx > 0) == (Ny > 0))
        u = abs(Nx/Ny)
        e = ex - ey

        if (u >= 1):
            u /= self.beta
            e += 1

        if (not s):
            u = -u

        return self.round(u*self.beta**e)

    def elements(self) -> list[tuple[int, int]]:
        """Gera todos os elementos positivos de F como pares (N, e)."""

        return [(N, e)
            for e in range(self.m, self.M + 1)
            for N in range(self.beta**(self.t - 1), self.beta**self.t)]

    def plot_line(self, filename=None, show_negative=True):
        """Reta real com os elementos de F, colorindo por expoente."""
        fig, ax = plt.subplots(figsize=(12, 3))
        cmap = plt.get_cmap("tab10")

        for e in range(self.m, self.M + 1):
            xs = [self.to_float((N, e))
                  for N in range(self.beta**(self.t - 1), self.beta**self.t)]
            color = cmap((e - self.m) % 10)
            ax.plot(xs, [0] * len(xs), "|", color=color, markersize=18,
                    label=f"e = {e} (esp. = {self.beta**(e - self.t):g})")
            if show_negative:
                ax.plot([-x for x in xs], [0] * len(xs), "|", color=color,
                        markersize=18)

        ax.plot([0], [0], "ko", markersize=4)          # zero
        for v, name in [(self.xmin, "$x_{min}$"), (self.xmax, "$x_{max}$")]:
            ax.axvline(v, color="red", linestyle="--", linewidth=0.8)
            ax.annotate(name, (v, 0), xytext=(0, 28),
                        textcoords="offset points", ha="center", color="red")
            if show_negative:
                ax.axvline(-v, color="red", linestyle="--", linewidth=0.8)

        ax.set_yticks([])
        ax.set_xlabel("x")
        ax.set_title(f"F({self.beta}, {self.t}, {self.m}, {self.M})")
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.3),
                  ncol=4, fontsize=8)
        fig.tight_layout()
        if filename:
            fig.savefig(filename, dpi=200)
        plt.show()

    def plot_spacing(self, filename=None):
        """Espaçamento β^(e-t) em função de e (escala log)."""
        es = list(range(self.m, self.M + 1))
        sp = [float(self.beta) ** (e - self.t) for e in es]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.semilogy(es, sp, "o-")
        ax.set_xlabel("expoente e")
        ax.set_ylabel(r"espaçamento $\beta^{e-t}$")
        ax.grid(True, which="both", alpha=0.3)
        if filename:
            fig.savefig(filename, dpi=200)
        plt.show()

    def preview_f(self):
        """Visualizacao do sistema sobre a reta real"""

        sistema = F(2, 3, -1, 2)
        sistema.plot_line("reta.png")
        sistema.plot_spacing("espacamento.png")
