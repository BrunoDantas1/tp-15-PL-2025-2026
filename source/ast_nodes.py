# AST: classes que representam nós sintáticos (Num, Var, BinOp, ...)

class Node:
    pass

#Guarda um Numero
class Num(Node):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NumLit({self.value})"

#Guarda um valor booleano (true, false, etc)
class BoolLit(Node):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"BoolLit({self.value})"

#Guarda um identificador (variável, nome de função, etc), ex: x = 10, x é a variavel(identidificador)
class Var(Node):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Var({self.name})"

#Recebe um operador (+, -, *, /) e um valor do lado esquerdo e direito, ex: 1 + 2, o operador é +, o valor do lado esquerdo é 1 e o valor do lado direito é 2
class BinOp(Node):
    def __init__(self, op, left, right):
        self.op    = op
        self.left  = left
        self.right = right
    def __repr__(self):
        return f"BinOp({self.op}, {self.left}, {self.right})"

#Recebe um operador (ex: -, !, etc) e um numero (ex:5, 6), ex: -10, o op é o '-' e o operand é  10
class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op      = op
        self.operand = operand
    def __repr__(self):
        return f"UnaryOp({self.op}, {self.operand})"

#Expressão condicional, ex: if x = 0, then 1 else 2, o cond é x = 0, o then_expr é 1 e o else_expr é 2
class IfExpr(Node):
    def __init__(self, cond, then_expr, else_expr):
        self.cond      = cond
        self.then_expr = then_expr
        self.else_expr = else_expr
    def __repr__(self):
        return f"IfExpr({self.cond}, {self.then_expr}, {self.else_expr})"

#Guarda um 'when' e os seus casos, ex: when x = 0 then 1 else 2, o expr é x = 0 e os cases são [(1, 2)]
class WhenExpr(Node):
    def __init__(self, expr, cases):
        self.expr  = expr
        self.cases = cases
    def __repr__(self):
        return f"WhenExpr({self.expr}, {self.cases})"

#Guarda nome da função e o argumento, ex: soma(5), o nome da função é soma e o argumento é 5
class FunCall(Node):
    def __init__(self, name, arg):
        self.name = name
        self.arg  = arg
    def __repr__(self):
        return f"FunCall({self.name}, {self.arg})"

#Guarda o nome da variavel, o tipo e o valor, ex: let y: int = 1, o nome da variavel é y, o tipo é int e o valor é 1
class LetVal(Node):
    def __init__(self, name, typ, expr):
        self.name = name
        self.typ  = typ
        self.expr = expr
    def __repr__(self):
        return f"LetVal({self.name}: {self.typ} = {self.expr})"

#Guarda a assinatura da função, o tipo do parâmetro e o tipo de retorno, ex: soma: int -> int, o nome da função é soma, o tipo do parâmetro é int e o tipo de retorno é int
class FunSig(Node):
    def __init__(self, name, param_type, return_type):
        self.name        = name
        self.param_type  = param_type
        self.return_type = return_type
    def __repr__(self):
        return f"FunSig({self.name}: {self.param_type} -> {self.return_type})"

#Guarda a defenição de uma funcao, nome, parametro e o que faz, ex:let some x = x +1;
class LetFun(Node):
    def __init__(self, name, param, expr):
        self.name  = name
        self.param = param
        self.expr  = expr
    def __repr__(self):
        return f"LetFun({self.name} {self.param} = {self.expr})"

#Guarda no smts todas as classes anteriormente defenidas por ordem
class Program(Node):
    def __init__(self, stmts):
        self.stmts = stmts
    def __repr__(self):
        return f"Program({self.stmts})"