import sys
from grammar import parse
from semantic import Semantic, SemanticError
from interpreter import Interpreter

#region Correr ficheiro
def run_file(path):
    # Lê o ficheiro .lf
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    run_source(source)
#endregion

#region Pipeline principal
def run_source(source):
    # 1. Parse -> constrói a AST
    tree = parse(source)
    if tree is None:
        print("[Erro] Falha no parsing.")
        return

    # 2. Análise semântica -> verifica os tipos
    sem = Semantic()
    try:
        sem.check(tree)
    except SemanticError as e:
        print(f"[Semântico] {e}")
        return

    # 3. Interpretação -> executa e mostra os resultados
    interp = Interpreter()
    interp.run(tree)
#endregion

#region Entry point
if __name__ == '__main__':
    if len(sys.argv) == 2:
        # Corre o ficheiro passado como argumento
        # exemplo: python main.py entrada.lf
        run_file(sys.argv[1])
    else:
        print("Uso: python main.py <ficheiro.lf>")
#endregion