import os
import tempfile
import unittest
from fractions import Fraction

import matplotlib
matplotlib.use("Agg")

import f

BETA, T, MIN_E, MAX_E = 10, 2, -1, 2        # F(10, 2, -1, 2)
S = f.F(BETA, T, MIN_E, MAX_E)

RELATORIO = []

def log(msg):
    RELATORIO.append(msg)
    print(msg)

def el(x):
    x = Fraction(x)

    if x == 0:
        return (0, 0)
    
    a = abs(x)
    for e in range(MIN_E, MAX_E + 1):
        if Fraction(BETA) ** (e - 1) <= a < Fraction(BETA) ** e:
            N = a / Fraction(BETA) ** (e - T)
            if N.denominator != 1:
                raise ValueError(f"{x} não pertence a F")
            return (int(N) if x > 0 else -int(N), e)
        
    raise ValueError(f"{x} fora de F")


def val(r):
    if r is None or isinstance(r, str):
        return r
    
    if isinstance(r, tuple):
        N, e = r
        return Fraction(N) * Fraction(BETA) ** (e - T)
    
    return Fraction(r).limit_denominator(10 ** 6)


def ref_round(x):
    x = Fraction(x)

    if x == 0:
        return Fraction(0)
    
    a = abs(x)
    if a < Fraction(1, 100):
        return "underflow"
    if a > 99:
        return "overflow"
    e = next(e for e in range(MIN_E, MAX_E + 1) if a < Fraction(BETA) ** e)
    p = Fraction(BETA) ** (e - T)
    q = a / p
    N = q.numerator // q.denominator
    if q - N >= Fraction(1, 2):
        N += 1
    y = N * p
    return y if x > 0 else -y


def op(name, x, y):
    return val(getattr(S, name)(el(x), el(y)))


def add(x, y): return op("sum", x, y)
def sub(x, y): return op("subtraction", x, y)
def mul(x, y): return op("product", x, y)
def div(x, y): return op("division", x, y)


def exato(name, x, y):
    x, y = Fraction(x), Fraction(y)
    r = {"sum": x + y, "subtraction": x - y, "product": x * y, "division": x / y}[name]
    return ref_round(r)


def tearDownModule():
    with open("resultados.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(RELATORIO) + "\n")


class TestF(unittest.TestCase):
    """Tests the implementation for F(10,2,-1,2)"""

    def test_parametros(self):
        self.assertAlmostEqual(S.xmin, 0.01)
        self.assertAlmostEqual(S.xmax, 99.0)
        log(f"[parâmetros] xmin = {S.xmin}, xmax = {S.xmax}")

    def test_create_element_validos(self):
        for x in [(10, -1), (99, 2), (-50, 0), (-99, -1), (10, 2)]:
            with self.subTest(x=x):
                self.assertEqual(S.create_element(x), x)

    def test_create_element_invalidos(self):
        invalidos = [
            (9, 0), (100, 0), (-9, 0), (-100, 0), (0, 0),   # N fora de J
            (50, 3), (50, -2),                              # e fora de E
            (50.0, 0), (50, 0.0), ("50", 0),                # tipos errados
            (50,), (50, 0, 1), [50, 0], None, 50, "x",      # formato errado
        ]
        for x in invalidos:
            with self.subTest(x=x):
                self.assertIsNone(S.create_element(x))

    def test_round_zero_e_elementos_exatos(self):
        self.assertEqual(S.round(0), 0.0)
        for x in [0.01, 0.5, 1.0, 9.9, 10, 42, 99, -0.01, -99]:
            with self.subTest(x=x):
                self.assertAlmostEqual(S.round(x), x)

    def test_round_underflow_overflow(self):
        for x in [0.001, 0.0099, -0.005]:
            with self.subTest(x=x):
                self.assertEqual(S.round(x), "underflow")
        for x in [99.5, 100, 150, -100, 1e6]:
            with self.subTest(x=x):
                self.assertEqual(S.round(x), "overflow")

    def test_round_empate_vai_para_maior_modulo(self):
        self.assertAlmostEqual(S.round(12.5), 13.0)
        self.assertAlmostEqual(S.round(-12.5), -13.0)
        self.assertAlmostEqual(S.round(0.375), 0.38)

    def test_round_sem_empate(self):
        casos = {50.4: 50.0, 50.6: 51.0, 3.14159: 3.1, 0.123: 0.12,
                 -3.14159: -3.1, 98.7: 99.0}
        for x, esperado in casos.items():
            with self.subTest(x=x):
                self.assertAlmostEqual(S.round(x), esperado)

    def test_round_contra_referencia(self):
        n = 0
        for k in range(10, 99000, 37):
            x = Fraction(k, 1000)
            r = ref_round(x)
            if r in ("underflow", "overflow"):
                continue
            e = next(e for e in range(MIN_E, MAX_E + 1) if x < Fraction(BETA) ** e)
            q = x / Fraction(BETA) ** (e - T)
            if q - (q.numerator // q.denominator) == Fraction(1, 2):
                continue
            with self.subTest(x=float(x)):
                self.assertAlmostEqual(S.round(float(x)), float(r), places=9)
            n += 1
        log(f"[round] {n} valores comparados com o arredondamento de referência")

    def test_to_float(self):
        casos = {(12, 2): 12.0, (10, -1): 0.01, (99, 2): 99.0, (-55, 0): -0.55,
                 (10, 1): 1.0, (99, -1): 0.099}
        for x, esperado in casos.items():
            with self.subTest(x=x):
                self.assertAlmostEqual(S.to_float(x), esperado)

    def test_get_element_form(self):
        self.assertEqual(S.get_element_form(0), (0, 0))
        casos = {12.0: (12, 2), 0.5: (50, 0), 0.01: (10, -1), 99.0: (99, 2),
                 1.0: (10, 1), 3.5: (35, 1), 0.25: (25, 0)}
        for x, esperado in casos.items():
            with self.subTest(x=x):
                self.assertEqual(S.get_element_form(x), esperado)

    def test_get_element_form_negativo(self):
        self.assertEqual(S.get_element_form(-3.5), (-35, 1))

    def test_get_element_form_fora_de_F(self):
        for x in [0.001, 100, 1e3, -100, -0.001]:
            with self.subTest(x=x):
                self.assertIsNone(S.get_element_form(x))

    def test_ida_e_volta(self):
        for x in [(10, -1), (57, 0), (99, 2), (23, 1)]:
            with self.subTest(x=x):
                self.assertEqual(S.get_element_form(S.to_float(x)), x)

    def test_compare_two(self):
        self.assertEqual(S.compare_two((10, 1), (11, 1)), -1)
        self.assertEqual(S.compare_two((99, 1), (10, 2)), -1)   
        self.assertEqual(S.compare_two((50, 0), (50, 0)), 0)
        self.assertEqual(S.compare_two((50, 1), (10, 1)), 1)
        self.assertEqual(S.compare_two((-50, 0), (10, -1)), -1)
        self.assertEqual(S.compare_two((-10, 0), (-20, 0)), 1)

    def test_get_symmetric(self):
        self.assertEqual(S.get_symmetric((50, 0)), (-50, 0))
        self.assertEqual(S.get_symmetric((-99, 2)), (99, 2))
        for x in [(10, -1), (73, 1)]:
            self.assertEqual(S.get_symmetric(S.get_symmetric(x)), x)

    def test_elements(self):
        els = S.elements()
        self.assertEqual(len(els), 90 * 4)              
        self.assertEqual(len(set(els)), len(els))
        for x in els:
            self.assertEqual(S.create_element(x), x)
        vs = [S.to_float(x) for x in els]
        self.assertEqual(vs, sorted(vs))                
        self.assertEqual(len(set(vs)), len(vs))         
        self.assertAlmostEqual(vs[0], S.xmin)
        self.assertAlmostEqual(vs[-1], S.xmax)
        log(f"[elements] {len(els)} elementos positivos, de {vs[0]} a {vs[-1]}")

    CASOS = [
        ("sum", "1.5", "2.5"), ("sum", "0.12", "3.4"), ("sum", "9.9", "0.1"),
        ("sum", "-1.5", "2.5"), ("sum", "-4", "-3"),
        ("subtraction", "5", "2"), ("subtraction", "9.9", "0.1"),
        ("subtraction", "0.5", "0.25"), ("subtraction", "2", "5"),
        ("product", "2.5", "4"), ("product", "1.1", "3"), ("product", "0.12", "0.5"),
        ("product", "-2", "3"), ("product", "-2", "-3"),
        ("division", "7", "2"), ("division", "1", "3"), ("division", "2", "3"),
        ("division", "-7", "2"), ("division", "-6", "-3"),
    ]

    def test_operacoes_corretas(self):
        for name, x, y in self.CASOS:
            with self.subTest(op=name, x=x, y=y):
                obtido, esperado = op(name, x, y), exato(name, x, y)
                self.assertEqual(obtido, esperado)
                log(f"[ok] {name}({x}, {y}) = {float(obtido):g}")

    def test_operacoes_overflow_underflow(self):
        casos = [("sum", "50", "50", "overflow"), ("product", "20", "20", "overflow"),
                 ("division", "1", "0.01", "overflow"),
                 ("product", "0.1", "0.01", "underflow"),
                 ("division", "0.01", "99", "underflow")]
        for name, x, y, esperado in casos:
            with self.subTest(op=name, x=x, y=y):
                self.assertEqual(op(name, x, y), esperado)
                log(f"[falha esperada] {name}({x}, {y}) -> {esperado}")

    def test_divisao_por_zero(self):
        self.assertIsNone(S.division((50, 0), (0, 0)))

    def test_operacoes_contra_referencia(self):
        vals = [Fraction(N, 10 ** (T - e)) for e in (0, 1, 2) for N in range(10, 100, 11)]
        n = 0
        for name in ("sum", "subtraction", "product", "division"):
            for x in vals:
                for y in vals:
                    if name == "subtraction" and x == y:
                        continue
                    esperado = exato(name, x, y)
                    bruto = {"sum": x + y, "subtraction": x - y,
                             "product": x * y, "division": x / y}[name]
                    if not isinstance(esperado, str):
                        a = abs(bruto)
                        e = next(e for e in range(MIN_E, MAX_E + 1) if a < Fraction(BETA) ** e)
                        q = a / Fraction(BETA) ** (e - T)
                        if q - (q.numerator // q.denominator) == Fraction(1, 2):
                            continue
                    with self.subTest(op=name, x=float(x), y=float(y)):
                        self.assertEqual(op(name, x, y), esperado)
                    n += 1
        log(f"[varredura] {n} operações comparadas com a referência")

    def test_comutatividade_vale(self):
        vals = ["0.13", "1.7", "9.9", "42", "0.5", "-3.3"]
        for x in vals:
            for y in vals:
                with self.subTest(x=x, y=y):
                    self.assertEqual(add(x, y), add(y, x))
                    self.assertEqual(mul(x, y), mul(y, x))

    def test_simetrico_e_identidade(self):
        for x in ["0.13", "1.7", "9.9", "42", "-3.3"]:
            with self.subTest(x=x):
                self.assertEqual(add(x, -Fraction(x)), 0)        
                self.assertEqual(mul(x, "1"), Fraction(x))       
                self.assertEqual(div(x, "1"), Fraction(x))       

    def test_absorcao(self):
        for x, y in [("50", "0.4"), ("1", "0.04"), ("9.9", "0.04"), ("10", "0.4")]:
            with self.subTest(x=x, y=y):
                r = add(x, y)
                self.assertEqual(r, Fraction(x))
                self.assertNotEqual(Fraction(y), 0)
                log(f"[absorção] {x} + {y} = {float(r):g}  (real: {float(Fraction(x)+Fraction(y)):g})")

    def test_cancelamento(self):
        x, y = "9.1", "9.0"
        real = Fraction(x) ** 2 - Fraction(y) ** 2                  
        forma1 = sub(mul(x, x), mul(y, y))                          
        forma2 = mul(sub(x, y), add(x, y))                          
        err1, err2 = abs(forma1 - real), abs(forma2 - real)
        self.assertEqual(forma1, 2)
        self.assertEqual(forma2, Fraction("1.8"))
        self.assertGreater(err1, err2)
        log(f"[cancelamento] x²−y²: real={float(real):g}, fl(x²)−fl(y²)={float(forma1):g} "
            f"(erro {float(err1):.3g}), (x−y)(x+y)={float(forma2):g} (erro {float(err2):.3g})")

    def test_cancelamento_diferenca_com_absorcao(self):
        r = sub(add("5", "0.04"), "5")
        self.assertEqual(r, 0)
        log(f"[cancelamento] (5 + 0.04) − 5 = {float(r):g}  (real: 0.04)")

    def test_associatividade_da_adicao_falha(self):
        a, b, c = "50", "0.4", "0.4"
        esq = add(add(a, b), c)       
        dir_ = add(a, add(b, c))      
        self.assertEqual(esq, 50)
        self.assertEqual(dir_, 51)
        self.assertNotEqual(esq, dir_)
        log(f"[assoc. soma] (50+0.4)+0.4 = {float(esq):g}  ≠  50+(0.4+0.4) = {float(dir_):g}")

    def test_distributividade_falha(self):
        a, b, c = "7", "2.2", "2.2"
        esq = mul(a, add(b, c))         
        dir_ = add(mul(a, b), mul(a, c)) 
        self.assertEqual(esq, 31)
        self.assertEqual(dir_, 30)
        self.assertNotEqual(esq, dir_)
        log(f"[distrib.] 7·(2.2+2.2) = {float(esq):g}  ≠  7·2.2 + 7·2.2 = {float(dir_):g}")

    def test_distributividade_busca_contraexemplos(self):
        vals = [Fraction(N, 10 ** (T - e)) for e in (0, 1) for N in range(10, 100, 3)]
        total = falhas = 0
        for a in ("3", "7", "9", "0.9"):
            for b in vals:
                for c in vals:
                    s = add(b, c)
                    if isinstance(s, str):
                        continue
                    l = mul(a, s)
                    p1, p2 = mul(a, b), mul(a, c)
                    if isinstance(p1, str) or isinstance(p2, str):
                        continue
                    r = add(p1, p2)
                    if isinstance(l, str) or isinstance(r, str):
                        continue
                    total += 1
                    falhas += (l != r)
        self.assertGreater(falhas, 0)
        log(f"[distrib.] {falhas} de {total} triplas testadas violam a·(b+c) = a·b + a·c")

    def test_associatividade_do_produto_falha(self):
        vals = [Fraction(N, 10 ** (T - e)) for e in (0, 1) for N in range(10, 100, 7)]
        achou = None
        for a in vals:
            for b in vals:
                ab = mul(a, b)
                if isinstance(ab, str):
                    continue
                for c in vals:
                    bc = mul(b, c)
                    if isinstance(bc, str):
                        continue
                    l, r = mul(ab, c), mul(a, bc)
                    if not isinstance(l, str) and not isinstance(r, str) and l != r:
                        achou = (a, b, c, l, r)
                        break
                if achou:
                    break
            if achou:
                break
        self.assertIsNotNone(achou)
        a, b, c, l, r = achou
        log(f"[assoc. produto] ({float(a):g}·{float(b):g})·{float(c):g} = {float(l):g}  ≠  "
            f"{float(a):g}·({float(b):g}·{float(c):g}) = {float(r):g}")

    def test_divisao_nao_inversa_da_multiplicacao(self):
        r = mul(div("1", "3"), "3")     
        self.assertEqual(r, Fraction("0.99"))
        self.assertNotEqual(r, 1)
        log(f"[inverso] (1/3)·3 = {float(r):g}  ≠  1")

    def test_plot_line_e_spacing(self):
        os.makedirs("figuras", exist_ok=True)
        reta = os.path.join("figuras", "reta_F10_2_-1_2.png")
        esp = os.path.join("figuras", "espacamento_F10_2_-1_2.png")
        S.plot_line(reta)
        S.plot_spacing(esp)
        for p in (reta, esp):
            self.assertTrue(os.path.exists(p) and os.path.getsize(p) > 0)
        log(f"[figuras] geradas: {reta}, {esp}")

    def test_preview_f(self):
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                S.preview_f() 
                for nome in ("reta.png", "espacamento.png"):
                    self.assertTrue(os.path.exists(nome))
            finally:
                os.chdir(cwd)


if __name__ == '__main__':
    unittest.main()