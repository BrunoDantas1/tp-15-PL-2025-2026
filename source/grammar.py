#
import ply.yacc as yacc
from lexer import tokens, build
from ast_nodes import (Num, BoolLit, Var, BinOp, UnaryOp, IfExpr, WhenExpr, FunCall, LetVal, FunSig, LetFun, Program)

start = 'program'

#do menos para o mais importante
precedence = (
    ('left',  'OR'), 
    ('left',  'AND'),
    ('right', 'NOT'),
    ('left',  'EQ', 'NEQ'), #EQ = igual(==) e NEQ = nao igual/diferente de(!=)
    ('left',  'LT', 'GT', 'LEQ', 'GEQ'), #LT = menor que(<), GT = maior que(>), LEQ = menor ou igual(<=) e GEQ = maior ou igual(>=)
    ('left',  'PLUS', 'MINUS'),
    ('left',  'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'), 
)

#region Lista de Statements

#Lê a primeirsa linha e cria uma lista 
def p_stmt_list_one(p):
    """stmt_list : stmt"""
    p[0] = [p[1]]

#Le a proxima linha e junta com a linha anterior na lista
def p_stmt_list_many(p):
    """stmt_list : stmt_list stmt"""
    p[0] = p[1] + [p[2]]
 
#cria o pograma a partir da lista que foi criada
def p_program(p):
    """program : stmt_list"""
    p[0] = Program(p[1])
 
 #endregion


#region Statements

#Guarda a assinatura da função, ex: fun id : Int -> Int; ex: let soma x = x+1; let - p1, soma - p2, x - p3, = - p4, x+1 - p5, ; -p6
def p_stmt_funsig(p):
    """stmt : FUN ID COLON type ARROW type SEMICOLON"""
    p[0] = FunSig(p[2], p[4], p[6]) #pega no nome da função, no tipo do parâmetro e no tipo de retorno e guarda na classe FunSig

#Recebe o nome da variavel, o tipo e o valor, ex: let idade : int = 21, pega no 'idade', 'int' e '21' e guarda na classe LetVal
def p_stmt_letval(p):
    """stmt : LET ID COLON type ASSIGN expr SEMICOLON"""
    p[0] = LetVal(p[2], p[4], p[6])

#Guarda a definição de uma função, ex: let inc x = x + 1;
def p_stmt_letfun(p):
    """stmt : LET ID ID ASSIGN expr SEMICOLON"""
    p[0] = LetFun(p[2], p[3], p[5])#pega no nome da função (inc), no parâmetro (x) e no corpo (x + 1) e guarda na classe LetFun

 #endregion


#region Tipos

#user escreve int ou bool, o lexer reconhece como TINT ou TBOOL, e o parser guarda as strings int e bool
def p_type_int(p):
    """type : TINT"""
    p[0] = 'Int'
 
def p_type_bool(p):
    """type : TBOOL"""
    p[0] = 'Bool'

#endregion


#region Expressões

# Operações aritméticas
def p_expr_plus(p):
    """expr : expr PLUS expr"""
    p[0] = BinOp('+', p[1], p[3])
 
def p_expr_minus(p):
    """expr : expr MINUS expr"""
    p[0] = BinOp('-', p[1], p[3])
 
def p_expr_times(p):
    """expr : expr TIMES expr"""
    p[0] = BinOp('*', p[1], p[3])
 
def p_expr_divide(p):
    """expr : expr DIVIDE expr"""
    p[0] = BinOp('/', p[1], p[3])
 
# Operações de comparação
def p_expr_eq(p):
    """expr : expr EQ expr"""
    p[0] = BinOp('==', p[1], p[3])
 
def p_expr_neq(p):
    """expr : expr NEQ expr"""
    p[0] = BinOp('!=', p[1], p[3])
 
def p_expr_lt(p):
    """expr : expr LT expr"""
    p[0] = BinOp('<', p[1], p[3])
 
def p_expr_gt(p):
    """expr : expr GT expr"""
    p[0] = BinOp('>', p[1], p[3])
 
def p_expr_leq(p):
    """expr : expr LEQ expr"""
    p[0] = BinOp('<=', p[1], p[3])
 
def p_expr_geq(p):
    """expr : expr GEQ expr"""
    p[0] = BinOp('>=', p[1], p[3])
 
# Operações booleanas
def p_expr_and(p):
    """expr : expr AND expr"""
    p[0] = BinOp('&&', p[1], p[3])
 
def p_expr_or(p):
    """expr : expr OR expr"""
    p[0] = BinOp('||', p[1], p[3])
 
def p_expr_not(p):
    """expr : NOT expr"""
    p[0] = UnaryOp('!', p[2])
 
# Menos unário: -n
def p_expr_uminus(p):
    """expr : MINUS expr %prec UMINUS"""
    p[0] = UnaryOp('-', p[2])
 
# Parênteses
def p_expr_paren(p):
    """expr : LPAREN expr RPAREN"""
    p[0] = p[2]
 
# Se cond entao e1 senao e2
def p_expr_if(p):
    """expr : IF expr THEN expr ELSE expr"""
    p[0] = IfExpr(p[2], p[4], p[6])
 
# diz que um when_expr é uma expressão
def p_expr_when(p):
    """expr : when_expr"""
    p[0] = p[1]
 
# Chamada de função: inc(5), p1 - inc, p3 - 5
def p_expr_funcall(p):
    """expr : ID LPAREN expr RPAREN"""
    p[0] = FunCall(p[1], p[3])
 
# ex: "42", 42 é reconhecido como Num e é guardado como Num(42)
def p_expr_num(p):
    """expr : NUM"""
    p[0] = Num(p[1])
 
# true -> BoolLit(True), false -- BoolLit(False)
def p_expr_true(p):
    """expr : TRUE"""
    p[0] = BoolLit(True)
 
def p_expr_false(p):
    """expr : FALSE"""
    p[0] = BoolLit(False)
 

# ex: x -> Var('x')
def p_expr_var(p):
    """expr : ID"""
    p[0] = Var(p[1])

#endregion


#region Seleção de Casos

#ex: when (x) is 0 -> true; 1 -> false; _ -> true; end
#o "_" funciona como senão (then)
def p_when_expr(p):
    """when_expr : WHEN LPAREN expr RPAREN IS case_list END"""
    p[0] = WhenExpr(p[3], p[6])
 
def p_case_list_many(p):
    """case_list : case_list case"""
    p[0] = p[1] + [p[2]]
 
def p_case_list_one(p):
    """case_list : case"""
    p[0] = [p[1]]
 

# ex: 5 -> exp;
def p_case_num(p):
    """case : NUM ARROW expr SEMICOLON"""
    p[0] = (Num(p[1]), p[3])
 
# ex: -5 ->exp;
def p_case_neg(p):
    """case : MINUS NUM ARROW expr SEMICOLON"""
    p[0] = (Num(-p[2]), p[4])
 
# ex: true -> exp;
def p_case_true(p):
    """case : TRUE ARROW expr SEMICOLON"""
    p[0] = (BoolLit(True), p[3])
 
# ex: false -> exp;
def p_case_false(p):
    """case : FALSE ARROW expr SEMICOLON"""
    p[0] = (BoolLit(False), p[3])
 
# _ -> exp;
def p_case_wildcard(p):
    """case : UNDERSCORE ARROW expr SEMICOLON"""
    p[0] = ('_', p[3])

#endregion


#region Erros

#Apresenta que o erro foi de sintaxe, valor (ex: ;), tipo (ex: SEMICOLON) e linha
def p_error(p):
    if p:
        print(f"[Sintático] Erro inesperado '{p.value}' (tipo {p.type}) na linha {p.lineno}")
    else:
        print("[Sintático] Erro: fim de ficheiro inesperado")

#endregion


parser = yacc.yacc()

def parse(text):
    lexer = build()
    return parser.parse(text, lexer=lexer)