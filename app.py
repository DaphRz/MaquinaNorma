import os

class MaquinaNorma:
    
    def __init__(self):
        self.registradores = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "E": 0,
            "F": 0,
            "G": 0,
            "H": 0,
            "I": 0,
            "K": 0,
            "M": 0,
            "T": 0,
        }
        self.macros = []
        # Carregando as macros dos arquivos
        for i in range(1, 12):
            
            with open(f"macros/macro{i}.txt", "r") as arq:
                print(f"Carregando macro {i}...")
                macrotemp = []
                for line in arq:
                    print(f"Processando linha: {line.strip()}")
                    macrotemp.append(line.split())
                print(f"Macro {i} carregada: {macrotemp}")
                self.macros.append(macrotemp)
            
    
    def _add(self, reg):
        self.registradores[reg] += 1
    
    def _sub(self, reg):
        if self.registradores[reg] > 0:
            self.registradores[reg] -= 1
    
    def _zero(self, reg):
        return self.registradores[reg] == 0
    
    def realizar_operacao(self, macro, a, b=0):
        for reg in self.registradores:
            self.registradores[reg] = 0
        self.registradores["A"] = a
        self.registradores["B"] = b

        linha_atual = 1
        print(f"({self.registradores['A']}, {self.registradores['B']}, {self.registradores['C']}, {self.registradores['D']}), M) -> Entrada de DaDOS")
        while linha_atual != 0:
            instrucao = macro[linha_atual - 1]
            reg = instrucao[2]
            linha_anterior = linha_atual
            intrucao_str = ""

            if instrucao[1] == "ADD":
                self._add(reg)
                linha_atual = int(instrucao[3])
                intrucao_str = f"FACA ADD ({reg}) E VA_PARA {linha_atual}"
            elif instrucao[1] == "SUB":
                self._sub(reg)
                linha_atual = int(instrucao[3])
                intrucao_str = f"FACA SUB ({reg}) E VA_PARA {linha_atual}"
            elif instrucao[1] == "ZER":
                if self._zero(reg):
                    linha_atual = int(instrucao[3])
                else:
                    linha_atual = int(instrucao[4])
                intrucao_str = f"SE ZERO ({reg}) ENTAO VA_PARA {instrucao[3]} SENAO VA_PARA {instrucao[4]}"
            print(f"({self.registradores['A']}, {self.registradores['B']}, {self.registradores['C']}, {self.registradores['D']}), {linha_anterior}) -> {intrucao_str})")
            
        
        return self.registradores


def menu():
    maq = MaquinaNorma()
    
    # Dicionário organizando as opções de macros: nome, (descrição, qtd_parametros)
    # DPS ADICINAR DESCRICAO MELHOR EM TEXTO NA TUPLA IGUAL AO MATERIAL DELE
    # ex: A := A + B usando C, onde o registrador C armazena a soma, A e B ficam zerados.
    operacoes = {
        "1":  ("SOMA", "C := A + B", 2),                       # Brenno
        "2":  ("MULTIPLICAÇÃO", "A := A * B", 2),              # Daphne
        "3":  ("FATORIAL", "A := A!", 1),                      # Gabriel
        "4":  ("MENOR QUE", "A < B", 2),                       # Isabel
        "5":  ("DIV. INTEIRA É ZERO", "A // B == 0", 2),       # Maria  
        "6":  ("NÚMERO PRIMO", "A é primo", 1),                # Brenno
        "7":  ("POTÊNCIA", "C := A^B", 2),                     # Daphne
        "8":  ("FIBONACCI", "A := fib(A)", 1),                 # Gabriel
        "9":  ("DIV. COM RESTO", "C := A//B, D := A%B", 2),    # Isabel       
        "10": ("MDC", "C := mdc(A, B)", 2),                    # Maria
        "11": ("COEF. BINOMIAL", "C := binomial(A, B)", 2),    # Brenno
        "0":  ("SAIR", "Encerrar a máquina", 0)
    }

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        # Imprimindo Menu Formatado
        print("╔═══════════════════════════════════════════════════════╗")
        print("║                    MÁQUINA NORMA                      ║")
        print("╠═══════════════════════════════════════════════════════╣")
        print("║ OPERAÇÕES DISPONÍVEIS:                                ║")
        print("║                                                       ║")
        
        
        for key, (nome, desc, _) in operacoes.items():
            if key != "0":
                print(f"║  [{key.rjust(2)}] {nome.ljust(22)}  ➜  {desc.ljust(21)}║")
        
        print("║                                                       ║")
        print(f"║  [ 0] {operacoes['0'][0].ljust(22)}  ➜  {operacoes['0'][1].ljust(21)}║")
        print("╚═══════════════════════════════════════════════════════╝")
        
        # Solicitando operação
        op = input("\n> Digite a operação desejada: ").strip()

        if op == "0":
            print("\n...Encerrando a Máquina Norma.\n")
            break
            
        if op not in operacoes:
            input("\nOperação inválida! Pressione Enter para tentar novamente...")
            continue

        # Solicitando os parâmetros necessários
        nome_op, desc_op, qtd_params = operacoes[op]
        print(f"\n--- {nome_op} - {desc_op} ---")
        
        try:
            a = int(input("> Digite o valor de A: "))
            b = 0
            if qtd_params == 2:
                b = int(input("> Digite o valor de B: "))
            
            if a < 0 or (qtd_params == 2 and b < 0):
                input("\nOs valores devem ser não negativos. Pressione Enter para voltar...")
                continue
        except ValueError:
            input("\nEntrada inválida. Digite apenas números inteiros. Pressione Enter...")
            continue
            
        # Realizando Macro
        regs = maq.realizar_operacao(maq.macros[int(op) - 1], a, b)
        
        # Resultado dos registradores
        print("\n" + "═" * 56)
        print(" " * 10 + "RESULTADOS DE {desc_op} com A={a}, B={b}".format(desc_op=desc_op, a=a, b=b))
        print("═" * 56)
        print(f"  [A] = {str(regs['A']).ljust(8)} [B] = {str(regs['B']).ljust(8)} [C] = {str(regs['C']).ljust(8)} [D] = {str(regs['D']).ljust(8)}")
        print(f"  [E] = {str(regs['E']).ljust(8)} [F] = {str(regs['F']).ljust(8)} [G] = {str(regs['G']).ljust(8)} [H] = {str(regs['H']).ljust(8)}")
        print(f"  [I] = {str(regs['I']).ljust(8)} [K] = {str(regs['K']).ljust(8)} [M] = {str(regs['M']).ljust(8)} [T] = {str(regs['T']).ljust(8)}")
        print("═" * 56)

        input("\nPressione Enter para continuar...")



if __name__ == "__main__":
    menu()
