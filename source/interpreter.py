from ast import (
    Num, BoolLit, Var, BinOp, UnaryOp,
    IfExpr, WhenExpr, FunCall,
    LetVal, FunSig, LetFun, Program
)

class RuntimeError_(Exception):
    pass

#cria um interpretador e um ambiente vazio para guardar variaveis, funções e a execução
class Interpreter:
    def __init__(self):
        self.env = {}

    #region Ponto de entrada
    # Percorre todos os statements do programa e executa-os
    def run(self, node):
        if isinstance(node, Program):
            for stmt in node.stmts:
                self.exec_stmt(stmt)
    #endregion

    #region Statements
    def exec_stmt(self, node):

        # ex: fun inc : Int -> Int;
        # Só é uma assinatura, não há nada para executar
        if isinstance(node, FunSig):
            return None

        # ex: let base : Int = 10;
        # Avalia a expressão e guarda o resultado no ambiente
        if isinstance(node, LetVal):
            value = self.eval(node.expr)
            self.env[node.name] = value
            print(f"resultado: {self._fmt(value)} tipo: {node.typ}")
            return value

        # ex: let inc x = x + 1; fica "inc": ('closure','x',BinOp('+', Var('x'), Num(1)),{})
        #closure indica que é uma função
        if isinstance(node, LetFun):
            self.env[node.name] = ('closure', node.param, node.expr, dict(self.env))
            return None
    #endregion

    #region Avaliação de expressões
    def eval(self, node):

        # verifica se é um numero literal e devolve o valor
        if isinstance(node, Num):
            return node.value

        # verifica se é bool e devolve o valor
        if isinstance(node, BoolLit):
            return node.value

        # Variável: vai buscar o valor ao ambiente
        if isinstance(node, Var):
            if node.name not in self.env: #verifica se a variavel existe 
                raise RuntimeError_(f"Variável '{node.name}' não definida") #se nao existir mostra o erro
            val = self.env[node.name] #senão busca a variavel no ambiente
            if isinstance(val, tuple) and val[0] == 'closure': #verifica se é função
                raise RuntimeError_(f"'{node.name}' é uma função, não um valor") #se for motra o erro
            return val #devolve o valor da variavel

        # Operação unária
        if isinstance(node, UnaryOp): #verifica se é valor unitario
            v = self.eval(node.operand) #avalia o operador e guarda em v
            if node.op == '-':
                return -v
            if node.op == '!':
                return not v

        # Operação binária
        if isinstance(node, BinOp): #recebe o operador e operandos
            #guarda o lado esquerrdo e o direito
            l = self.eval(node.left)
            r = self.eval(node.right)
            ops = { #cria o dicionário e vai verificando qual o operador
                '+' : lambda a, b: a + b,
                '-' : lambda a, b: a - b,
                '*' : lambda a, b: a * b,
                '/' : lambda a, b: a // b,
                '==': lambda a, b: a == b,
                '!=': lambda a, b: a != b,
                '<' : lambda a, b: a < b,
                '>' : lambda a, b: a > b,
                '<=': lambda a, b: a <= b,
                '>=': lambda a, b: a >= b,
                '&&': lambda a, b: a and b,
                '||': lambda a, b: a or b,
            }
            return ops[node.op](l, r) #devolve o resultado da operação

        # avalia a condição e escolhe o ramo (then ou else)
        if isinstance(node, IfExpr):
            cond = self.eval(node.cond)
            if cond:
                return self.eval(node.then_expr)
            else:
                return self.eval(node.else_expr)

        # avalia a expressão e encontra o primeiro padrão que case
        if isinstance(node, WhenExpr):
            val = self.eval(node.expr) #calcula o valor da expressão
            for pattern, result in node.cases:
                #compara os valores
                if pattern == '_':              
                    return self.eval(result)
                pval = self.eval(pattern)
                if val == pval:
                    return self.eval(result)
            #prevenção, encaixa sempre num dos casos
            raise RuntimeError_(f"'when' sem padrão que case com {val}")

        #
        if isinstance(node, FunCall):
            if node.name not in self.env: #existe? senao existir mostra erro
                raise RuntimeError_(f"Função '{node.name}' não definida")
            fn = self.env[node.name] #busca a função se existir
            if not (isinstance(fn, tuple) and fn[0] == 'closure'): #é mesmo funcao? se nao for mostra erro
                raise RuntimeError_(f"'{node.name}' não é uma função") 
            _, param, body, closure_env = fn # se for separa por partes

            # carrega o argumento
            arg_val = self.eval(node.arg)

            # guarda o ambiente atual, dps carrega o ambiente guardadado pela closure e coloca o argumento no ambiente
            #por fim calcula/executa o corpo da função
            saved = self.env
            self.env = dict(closure_env)
            self.env[param] = arg_val
            result = self.eval(body)
            self.env = saved
            return result

        raise RuntimeError_(f"Nó desconhecido: {type(node)}")
    #endregion

    #region Auxiliar
    # Formata o valor para apresentar ao utilizador true e falso em minusculas
    def _fmt(self, value):
        if isinstance(value, bool):
            return 'true' if value else 'false'
        return str(value)
    #endregion