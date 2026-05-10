# Lexer (PLY): define tokens e regras léxicas;

import ply.lex as lex

#palavras reservadas
reserved = {
    'let'   : 'LET',
    'fun'   : 'FUN',
    'if'    : 'IF',
    'then'  : 'THEN',
    'else'  : 'ELSE',
    'when'  : 'WHEN',
    'is'    : 'IS',
    'end'   : 'END',
    'true'  : 'TRUE',
    'false' : 'FALSE',
    'Int'   : 'TINT',
    'Bool'  : 'TBOOL',
}

#tokens
tokens = (
    'NUM',
    'ID',
    'ARROW',
    'EQ',
    'NEQ',
    'LEQ',
    'GEQ',
    'AND',
    'OR',
    'NOT',
    'ASSIGN',
    'SEMICOLON',
    'COLON',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'UNDERSCORE',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LT',
    'GT',
) + tuple(reserved.values())

#expressões regulares
t_ignore     = ' \t'
t_ARROW      = r'->'
t_EQ         = r'=='
t_NEQ        = r'!='
t_LEQ        = r'<='
t_GEQ        = r'>='
t_AND        = r'&&'
t_OR         = r'\|\|'
t_NOT        = r'!'
t_ASSIGN     = r'='
t_SEMICOLON  = r';'
t_COLON      = r':'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_COMMA      = r','
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_LT         = r'<'
t_GT         = r'>'
t_UNDERSCORE = r'_'

#faz com que o leer reconheca comentarios
def t_COMMENT_LINE(t):
    r'--[^\n]*'
    pass

#faz com que o leer reconheca comentarios de bloco
def t_COMMENT_BLOCK(t):
    r'\{-(.|\n)*?-\}'
    t.lexer.lineno += t.value.count('\n') #atualiza o numero de linhas o lexer 
    pass

#serve para reconhecer numeros, pois reconhece inicialmente como sdtring e passa para numero, ex: "123" -> 123
def t_NUM(t):
    r'\d+' # um digito seguido de zero ou mais dígitos
    t.value = int(t.value)
    return t

#serve para reconhecer nomes de variaveis, funcoes, etc
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*' #primeiro uma letra seguido de letras, numeros ou underscores, zero ou mais vezes
    t.type = reserved.get(t.value, 'ID') #verifica se esta no reserved, se estiver devolve o valor correspondente, se nao estover fica como 'ID'
    return t

#encontra mudanças de linha e atualiza o numero de linhas do lexer
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Quando aparece um caractere não reconhecido pelo lexer, esta função mostra o erro e manda o lexer continuyar a analisar o resto do codigo
def t_error(t):
    print(f"[Léxico] Caracter ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1) #avança um caractere

#prepara o lexer
def build():
    return lex.lex()
    #return build()