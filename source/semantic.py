from ast import (
    Num, BoolLit, Var, BinOp, UnaryOp,
    IfExpr, WhenExpr, FunCall,
    LetVal, FunSig, LetFun, Program
)

class SemanticError(Exception):
    pass

class Semantic:
    def __init__(self):
        # Tabela de símbolos: nome -> tipo
        # Para funções guarda ('fun', tipo_param, tipo_retorno)
        self.symbols = {}

    #region Ponto de entrada
    def check(self, node):
        """Analisa o programa todo e preenche a tabela de símbolos."""
        if isinstance(node, Program):
            for stmt in node.stmts:
                self.check_stmt(stmt)
        return self.symbols
    #endregion

    #region Statements
    def check_stmt(self, node):

        # fun inc : Int -> Int;
        # Guarda na tabela de símbolos que 'inc' é uma função que recebe Int e devolve Int
        if isinstance(node, FunSig):
            self.symbols[node.name] = ('fun', node.param_type, node.return_type)

        # let base : Int = 10;
        # Verifica se o tipo declarado bate certo com o tipo da expressão
        elif isinstance(node, LetVal):
            expr_type = self.infer(node.expr)
            if expr_type != node.typ:
                raise SemanticError(
                    f"Tipo errado em '{node.name}': "
                    f"declarado '{node.typ}' mas a expressão é '{expr_type}'"
                )
            self.symbols[node.name] = node.typ

        # let inc x = x + 1;
        # Verifica se o corpo da função tem o tipo de retorno correto
        elif isinstance(node, LetFun):
            if node.name not in self.symbols:
                raise SemanticError(
                    f"Função '{node.name}' não tem assinatura declarada (falta 'fun')"
                )
            sig = self.symbols[node.name]
            param_type  = sig[1]
            return_type = sig[2]

            # Adiciona o parâmetro à tabela de símbolos temporariamente
            saved = self.symbols.copy()
            self.symbols[node.param] = param_type

            body_type = self.infer(node.expr)

            # Restaura a tabela de símbolos (remove o parâmetro)
            self.symbols = saved

            if body_type != return_type:
                raise SemanticError(
                    f"Função '{node.name}': corpo tem tipo '{body_type}' "
                    f"mas assinatura diz '{return_type}'"
                )
    #endregion

    #region Inferência de tipos
    def infer(self, node):

        # Num → sempre Int
        if isinstance(node, Num):
            return 'Int'

        # BoolLit → sempre Bool
        if isinstance(node, BoolLit):
            return 'Bool'

        # Var → vai buscar o tipo à tabela de símbolos
        if isinstance(node, Var):
            if node.name not in self.symbols:
                raise SemanticError(f"Variável '{node.name}' não declarada")
            t = self.symbols[node.name]
            if isinstance(t, tuple):
                raise SemanticError(f"'{node.name}' é uma função, não um valor")
            return t

        # UnaryOp: -n requer Int, !b requer Bool
        if isinstance(node, UnaryOp):
            t = self.infer(node.operand)
            if node.op == '-':
                if t != 'Int':
                    raise SemanticError(f"Operador '-' requer Int, recebeu {t}")
                return 'Int'
            if node.op == '!':
                if t != 'Bool':
                    raise SemanticError(f"Operador '!' requer Bool, recebeu {t}")
                return 'Bool'

        # BinOp: verifica tipos dos dois lados
        if isinstance(node, BinOp):
            lt = self.infer(node.left)
            rt = self.infer(node.right)

            # +, -, *, / → ambos Int, resultado Int
            if node.op in ('+', '-', '*', '/'):
                if lt != 'Int' or rt != 'Int':
                    raise SemanticError(
                        f"Operador '{node.op}' requer Int e Int, "
                        f"recebeu {lt} e {rt}"
                    )
                return 'Int'

            # <, >, <=, >= → ambos Int, resultado Bool
            if node.op in ('<', '>', '<=', '>='):
                if lt != 'Int' or rt != 'Int':
                    raise SemanticError(
                        f"Operador '{node.op}' requer Int e Int, "
                        f"recebeu {lt} e {rt}"
                    )
                return 'Bool'

            # ==, != → ambos do mesmo tipo, resultado Bool
            if node.op in ('==', '!='):
                if lt != rt:
                    raise SemanticError(
                        f"Operador '{node.op}': tipos incompatíveis {lt} e {rt}"
                    )
                return 'Bool'

            # &&, || → ambos Bool, resultado Bool
            if node.op in ('&&', '||'):
                if lt != 'Bool' or rt != 'Bool':
                    raise SemanticError(
                        f"Operador '{node.op}' requer Bool e Bool, "
                        f"recebeu {lt} e {rt}"
                    )
                return 'Bool'

        # if cond then e1 else e2
        # cond tem de ser Bool, e1 e e2 têm de ter o mesmo tipo
        if isinstance(node, IfExpr):
            cond_t = self.infer(node.cond)
            if cond_t != 'Bool':
                raise SemanticError(
                    f"Condição do 'if' deve ser Bool, recebeu {cond_t}"
                )
            then_t = self.infer(node.then_expr)
            else_t = self.infer(node.else_expr)
            if then_t != else_t:
                raise SemanticError(
                    f"Ramos do 'if' têm tipos diferentes: {then_t} e {else_t}"
                )
            return then_t

        # when (expr) is ... end
        # todos os casos têm de ter o mesmo tipo de resultado
        if isinstance(node, WhenExpr):
            result_type = None
            for pattern, result in node.cases:
                rt = self.infer(result)
                if result_type is None:
                    result_type = rt
                elif rt != result_type:
                    raise SemanticError(
                        f"Casos do 'when' têm tipos diferentes: "
                        f"{result_type} e {rt}"
                    )
            return result_type

        # inc(5) → verifica se 'inc' existe, se é função,
        # e se o argumento tem o tipo certo
        if isinstance(node, FunCall):
            if node.name not in self.symbols:
                raise SemanticError(f"Função '{node.name}' não declarada")
            sig = self.symbols[node.name]
            if not isinstance(sig, tuple) or sig[0] != 'fun':
                raise SemanticError(f"'{node.name}' não é uma função")
            arg_type = self.infer(node.arg)
            if arg_type != sig[1]:
                raise SemanticError(
                    f"Chamada a '{node.name}': argumento deve ser "
                    f"'{sig[1]}', recebeu '{arg_type}'"
                )
            return sig[2]

        raise SemanticError(f"Nó desconhecido: {type(node)}")
    #endregion