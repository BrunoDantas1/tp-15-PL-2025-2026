# Trabalho Prático

**Processamento de Linguagens**

Licenciatura em Engenharia de Sistemas Informáticos (*regime laboral*) 2025-26

## Sobre o projeto

Interpretador em Python para a **LFun**, uma linguagem funcional simplificada. A linguagem suporta:

- expressões aritméticas e booleanas;
- definições de variáveis (`let`) e de funções (`fun` + `let`);
- condicionais (`if / then / else`);
- seleção de casos (`when ... is ... end`);
- comentários de linha (`--`) e de bloco (`{- ... -}`).

O interpretador foi construído com a biblioteca [PLY](https://www.dabeaz.com/ply/) (Python Lex-Yacc) e segue quatro fases:

1. **Análise léxica** (`lexer.py`): transforma o texto em tokens.
2. **Análise sintática** (`grammar.py`): constrói a árvore de sintaxe abstrata (AST, definida em `ast_nodes.py`).
3. **Análise semântica** (`semantic.py`): tabela de símbolos e verificação de tipos.
4. **Interpretação** (`interpreter.py`): avalia a AST e mostra os resultados.

O ficheiro `main.py` é o ponto de entrada e liga as quatro fases.

## grupo *15*

| Nome |
|-----------------|
| Bruno Dantas |
| Gonçalo Correia |
| João Castro |
| André Ferreira |

## organização

|    |    |
| -- | -- |
|[input/](./input/)| exemplos de texto de entrada (ficheiros `.lf`) |
|[report/](./report/)  | relatório do trabalho |
|[source/](./source/)  | código com a implementação da solução desenvolvida |

## executar a aplicação

**Requisitos:** Python 3 e a biblioteca PLY.

```bash
pip install ply
```

**Executar um ficheiro `.lf`** (a partir da raiz do projeto):

```bash
python source/main.py input/01_arith.lf
```

Exemplo de saída:

```
resultado: 7 tipo: Int
resultado: 4 tipo: Int
resultado: 50 tipo: Int
resultado: true tipo: Bool
resultado: false tipo: Bool
resultado: true tipo: Bool
```

Sem argumentos, o programa mostra `Uso: python main.py <ficheiro.lf>`.

### Exemplos incluídos

| Ficheiro | O que demonstra |
| -- | -- |
| `input/01_arith.lf` | expressões aritméticas e booleanas |
| `input/02_defenicoes.lf` | definições com `let` (termina com um erro semântico **propositado**: `Int` declarado, mas valor `Bool`) |
| `input/03_funcoes.lf` | declaração e chamada de funções |
| `input/04_condicional.lf` | `if/then/else` e `when` |
| `input/05_comentarios.lf` | comentários de linha e de bloco |

### Pequeno exemplo da linguagem

```
-- declarar o tipo da função e depois defini-la
fun dobro : Int -> Int;
let dobro n = n * 2;

let r : Int = dobro(7);
```

Resultado: `resultado: 14 tipo: Int`

## referências web

- [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/)
