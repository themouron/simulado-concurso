#!/usr/bin/env python3
"""Gera um simulado inédito, em PDF, inspirado no padrão visual de cadernos AOCP."""
from __future__ import annotations

from dataclasses import dataclass
from textwrap import wrap

PDF_FILE = "simulado_aocp_policia_penal_sp_prof_mourao.pdf"

INTRO = [
    "Prezado(a) candidato(a), prepare-se adequadamente para este treinamento: escolha um local silencioso, deixe sobre a mesa apenas o material permitido e evite qualquer distração durante a resolução.",
    "Marque o tempo de prova desde o início. Considere a duração total de 3 horas e procure administrar a leitura, os cálculos e a conferência do gabarito como faria em uma situação real.",
    "Simule o ambiente de prova: não consulte materiais, desligue notificações e mantenha concentração constante. O objetivo é medir desempenho com fidelidade e transformar o resultado em plano de estudo.",
    "Professor Mourão\n@mouraoprofessor",
]

@dataclass(frozen=True)
class Question:
    n: int
    area: str
    stem: str
    options: tuple[str, str, str, str]
    answer: str

TEXT = """No pátio interno da unidade, antes que os portões se abrissem para a rotina do dia, a equipe conferiu registros, revisou procedimentos e ajustou pequenas falhas de comunicação. Havia, naquele gesto aparentemente simples, uma compreensão decisiva: segurança pública não se sustenta apenas pela força visível, mas pela regularidade de condutas, pela clareza das informações e pela responsabilidade de cada agente. Quando a organização institucional funciona, o improviso perde espaço e a confiança social encontra fundamento concreto."""

QUESTIONS: list[Question] = [
    Question(1, "LÍNGUA PORTUGUESA", f"Leia o texto a seguir.\n\n{TEXT}\n\nDe acordo com o texto, a segurança pública é apresentada principalmente como resultado", ("da atuação isolada de agentes experientes em situações emergenciais.", "da combinação entre força visível, procedimentos regulares e responsabilidade institucional.", "da substituição de registros formais por decisões rápidas e improvisadas.", "do aumento de portões, barreiras físicas e recursos tecnológicos."), "B"),
    Question(2, "LÍNGUA PORTUGUESA", "No trecho 'Havia, naquele gesto aparentemente simples, uma compreensão decisiva', as vírgulas foram empregadas para", ("separar termos coordenados com a mesma função sintática.", "isolar adjunto adverbial intercalado.", "marcar a supressão de um verbo anteriormente expresso.", "separar sujeito e predicado."), "B"),
    Question(3, "LÍNGUA PORTUGUESA", "Em 'segurança pública não se sustenta apenas pela força visível', o termo 'apenas' estabelece ideia de", ("exclusão absoluta.", "retificação temporal.", "restrição argumentativa.", "causa inevitável."), "C"),
    Question(4, "LÍNGUA PORTUGUESA", "Assinale a alternativa em que todas as palavras estão corretamente acentuadas.", ("juíz, ítem, júri, também.", "saúde, caráter, hífen, possível.", "ideia, papéis, gratuíto, órfão.", "assembléia, bônus, rúbrica, polícia."), "B"),
    Question(5, "LÍNGUA PORTUGUESA", "Assinale a alternativa em que o uso do acento indicativo de crase está correto.", ("O servidor entregou o relatório à chefia imediata.", "A equipe retornou à pé para o setor administrativo.", "O documento foi anexado à este processo eletrônico.", "As orientações foram dadas à todos os presentes."), "A"),
    Question(6, "LÍNGUA PORTUGUESA", "Quanto à ortografia, assinale a alternativa correta.", ("A paralisação exigiu discrição e análise minuciosa dos fatos.", "A paralização exigiu discrissão e análise minuciosa dos fatos.", "A paralisação exigiu discrissão e análize minuciosa dos fatos.", "A paralização exigiu descrição e análise minunciosa dos fatos."), "A"),
    Question(7, "LÍNGUA PORTUGUESA", "Na frase 'A responsabilidade de cada agente fortalece a instituição', o núcleo do sujeito é", ("responsabilidade.", "cada.", "agente.", "instituição."), "A"),
    Question(8, "LÍNGUA PORTUGUESA", "Assinale a alternativa em que há oração subordinada adverbial concessiva.", ("Quando a equipe chegou, os documentos já estavam separados.", "Embora houvesse pressão, o procedimento foi seguido integralmente.", "O servidor registrou a ocorrência porque observou irregularidade.", "Caso surja nova informação, o relatório será atualizado."), "B"),
    Question(9, "LÍNGUA PORTUGUESA", "A expressão 'a confiança social encontra fundamento concreto' apresenta linguagem em sentido", ("denotativo, pois descreve ato físico de localizar objeto.", "figurado, pois atribui a 'confiança' uma ação própria de ser animado.", "metalinguístico, pois explica o significado de 'fundamento'.", "fático, pois testa o canal de comunicação."), "B"),
    Question(10, "LÍNGUA PORTUGUESA", "Predomina no texto a função da linguagem", ("emotiva, centrada na exteriorização íntima do emissor.", "conativa, voltada exclusivamente a ordenar o leitor.", "referencial, com exposição de ideia sobre organização institucional.", "poética, pela valorização exclusiva da sonoridade."), "C"),
    Question(11, "LÍNGUA PORTUGUESA", "Assinale a alternativa correta quanto à concordância verbal.", ("Fazem três anos que o setor revisa seus protocolos.", "Haviam registros pendentes no sistema.", "Existiam divergências entre os relatórios apresentados.", "A maioria dos servidores compareceram obrigatoriamente, sem variação possível."), "C"),
    Question(12, "LÍNGUA PORTUGUESA", "Assinale a alternativa correta quanto à concordância nominal.", ("Seguem anexo as cópias solicitadas.", "É proibida entrada de pessoas não autorizadas.", "As planilhas foram bastante revisadas e conferidas.", "Os documentos permaneceram incluso no processo."), "C"),
    Question(13, "LÍNGUA PORTUGUESA", "A regência está de acordo com a norma-padrão em", ("O servidor assistiu o treinamento obrigatório.", "O chefe informou os agentes de que haveria reunião.", "A comissão visou à melhoria dos procedimentos internos.", "O relatório implicou em nova diligência."), "C"),
    Question(14, "LÍNGUA PORTUGUESA", "Assinale a alternativa em que a colocação pronominal está correta segundo a norma-padrão.", ("Não comunicaram-se os responsáveis a tempo.", "Sempre se observam os protocolos de segurança.", "Me entregaram o memorando sem assinatura.", "Far-se-á uma revisão, se necessário for, somente em linguagem coloquial."), "B"),
    Question(15, "LÍNGUA PORTUGUESA", "Em 'o improviso perde espaço', a palavra 'improviso' pode ser substituída, sem prejuízo de sentido, por", ("planejamento.", "previsibilidade.", "casualidade não planejada.", "formalidade excessiva."), "C"),
    Question(16, "LÍNGUA PORTUGUESA", "Assinale a reescrita que preserva o sentido e a correção: 'Quando a organização institucional funciona, o improviso perde espaço.'", ("Funcionando a organização institucional, o improviso perde espaço.", "A organização institucional funciona, embora o improviso perde espaço.", "O improviso perde espaço, por que a organização institucional funcionaria.", "Se a organização institucional funcionou, o improviso perdera espaço necessariamente no passado."), "A"),
    Question(17, "LÍNGUA PORTUGUESA", "Em 'revisou procedimentos e ajustou pequenas falhas', os termos destacados exercem, respectivamente, a função de", ("predicativo do sujeito e aposto.", "objeto direto e objeto direto.", "objeto indireto e complemento nominal.", "adjunto adverbial e objeto indireto."), "B"),
    Question(18, "LÍNGUA PORTUGUESA", "Assinale a alternativa em que a pontuação está correta.", ("Os agentes, após a conferência dos registros, iniciaram a rotina.", "Os agentes após a conferência, dos registros iniciaram a rotina.", "Os agentes após, a conferência dos registros, iniciaram a rotina.", "Os agentes, após a conferência dos registros iniciaram, a rotina."), "A"),
    Question(19, "LÍNGUA PORTUGUESA", "A relação de coesão entre 'registros', 'procedimentos' e 'informações' no texto contribui para", ("mudança brusca de tema sem retomada.", "campo semântico ligado à organização administrativa.", "contradição entre linguagem formal e informal.", "ambiguidade necessária à interpretação."), "B"),
    Question(20, "LÍNGUA PORTUGUESA", "Assinale a alternativa em que a palavra destacada pertence à classe dos advérbios: 'gesto aparentemente simples'.", ("gesto.", "aparentemente.", "simples.", "da."), "B"),
    Question(21, "MATEMÁTICA", "Em uma operação administrativa, foram conferidos 180 documentos. O conjunto A contém os 95 documentos digitalizados, e o conjunto B contém os 120 documentos assinados. Sabendo que 50 documentos pertencem simultaneamente aos conjuntos A e B, o número de documentos que não pertencem a nenhum desses conjuntos é", ("5.", "10.", "15.", "20."), "C"),
    Question(22, "MATEMÁTICA", "A soma das raízes da equação x² - 7x + 10 = 0 é", ("-10.", "-7.", "5.", "7."), "D"),
    Question(23, "MATEMÁTICA", "A função f(x)=3x-5 satisfaz f(k)=16. O valor de k é", ("5.", "6.", "7.", "8."), "C"),
    Question(24, "MATEMÁTICA", "Quatro servidores produzem 96 relatórios em 6 dias, mantendo o mesmo ritmo. O número de relatórios produzidos por 6 servidores em 5 dias é", ("100.", "110.", "120.", "144."), "C"),
    Question(25, "MATEMÁTICA", "Um equipamento custava R$ 2.400,00 e teve aumento de 12%, seguido de desconto de 10% sobre o novo preço. O preço final é", ("R$ 2.376,00.", "R$ 2.400,00.", "R$ 2.419,20.", "R$ 2.688,00."), "C"),
    Question(26, "MATEMÁTICA", "Um capital de R$ 5.000,00 aplicado a juros simples de 2% ao mês, durante 8 meses, rende juros de", ("R$ 600,00.", "R$ 700,00.", "R$ 800,00.", "R$ 900,00."), "C"),
    Question(27, "MATEMÁTICA", "Um capital aplicado a juros compostos de 10% ao ano passa de R$ 1.000,00 para, após 2 anos,", ("R$ 1.100,00.", "R$ 1.200,00.", "R$ 1.210,00.", "R$ 1.220,00."), "C"),
    Question(28, "MATEMÁTICA", "Um retângulo possui perímetro 50 cm e largura 10 cm. Sua área é", ("100 cm².", "120 cm².", "150 cm².", "200 cm²."), "C"),
    Question(29, "MATEMÁTICA", "Em um triângulo retângulo, os catetos medem 9 cm e 12 cm. A hipotenusa mede", ("13 cm.", "14 cm.", "15 cm.", "16 cm."), "C"),
    Question(30, "MATEMÁTICA", "Se sen(theta)=3/5, com theta agudo, então cos(theta) é", ("2/5.", "3/4.", "4/5.", "5/4."), "C"),
    Question(31, "MATEMÁTICA", "As idades de cinco candidatos são 24, 28, 31, 31 e 36 anos. A mediana dessas idades é", ("28.", "30.", "31.", "32."), "C"),
    Question(32, "MATEMÁTICA", "Uma urna contém 5 bolas azuis, 3 vermelhas e 2 brancas. Retirando-se uma bola ao acaso, a probabilidade de ela não ser vermelha é", ("3/10.", "1/2.", "7/10.", "4/5."), "C"),
    Question(33, "MATEMÁTICA", "De quantas maneiras distintas 4 agentes podem ocupar 4 postos diferentes, um em cada posto?", ("12.", "16.", "20.", "24."), "D"),
    Question(34, "MATEMÁTICA", "Em uma progressão aritmética, a1=6 e a razão é 4. O décimo termo é", ("38.", "40.", "42.", "46."), "C"),
    Question(35, "MATEMÁTICA", "A distância entre os pontos A(2,3) e B(8,11) no plano cartesiano é", ("8.", "10.", "12.", "14."), "B"),
    Question(36, "CONHECIMENTOS ESPECÍFICOS", "No Windows 10/11, o atalho geralmente utilizado para bloquear a sessão do usuário é", ("Ctrl + C.", "Alt + Tab.", "Windows + L.", "Ctrl + P."), "C"),
    Question(37, "CONHECIMENTOS ESPECÍFICOS", "No Microsoft Word, o recurso mais adequado para padronizar títulos e subtítulos, facilitando a criação de sumário automático, é", ("Pincel de Animação.", "Estilos.", "Solver.", "Congelar Painéis."), "B"),
    Question(38, "CONHECIMENTOS ESPECÍFICOS", "No Excel, a fórmula =SOMA(A1:A5) realiza", ("a contagem apenas das células vazias entre A1 e A5.", "a soma dos valores contidos no intervalo de A1 até A5.", "a ordenação alfabética do intervalo indicado.", "a criação automática de gráfico dinâmico."), "B"),
    Question(39, "CONHECIMENTOS ESPECÍFICOS", "Em correio eletrônico, o campo Cco é utilizado para", ("enviar cópia oculta a destinatário, sem exibir seu endereço aos demais.", "criptografar obrigatoriamente todo anexo enviado.", "indicar o assunto principal da mensagem.", "bloquear respostas de todos os destinatários."), "A"),
    Question(40, "CONHECIMENTOS ESPECÍFICOS", "A prática de induzir usuário a fornecer senha por meio de mensagem fraudulenta caracteriza, em regra,", ("backup incremental.", "phishing.", "fragmentação de disco.", "compactação sem perdas."), "B"),
    Question(41, "CONHECIMENTOS ESPECÍFICOS", "O princípio administrativo que exige atuação conforme padrões de honestidade, boa-fé e lealdade institucional é o da", ("publicidade.", "moralidade.", "impessoalidade.", "autotutela."), "B"),
    Question(42, "CONHECIMENTOS ESPECÍFICOS", "A presunção de legitimidade dos atos administrativos significa que tais atos", ("são considerados válidos até prova em contrário.", "não podem ser anulados pela própria Administração.", "dispensam motivação em todos os casos.", "sempre produzem efeitos penais automáticos."), "A"),
    Question(43, "CONHECIMENTOS ESPECÍFICOS", "Nos termos constitucionais, a segurança pública é dever do Estado, direito e responsabilidade de todos, sendo exercida para", ("promover exclusivamente atividades de arrecadação tributária.", "preservar a ordem pública e a incolumidade das pessoas e do patrimônio.", "substituir integralmente a atuação do Poder Judiciário.", "controlar previamente a manifestação de pensamento."), "B"),
    Question(44, "CONHECIMENTOS ESPECÍFICOS", "Após a Emenda Constitucional nº 104/2019, as polícias penais vinculam-se", ("somente à União, sem órgãos estaduais.", "à segurança privada contratada por concessionárias.", "aos órgãos administradores do sistema penal da unidade federativa a que pertencem.", "às Guardas Municipais, por subordinação hierárquica direta."), "C"),
    Question(45, "CONHECIMENTOS ESPECÍFICOS", "Quanto à aplicação da lei penal no tempo, a lei posterior que de qualquer modo favorecer o agente", ("não se aplica a fatos anteriores.", "aplica-se aos fatos anteriores, ainda que decididos por sentença condenatória transitada em julgado.", "somente se aplica a crimes militares.", "depende sempre de autorização administrativa."), "B"),
    Question(46, "CONHECIMENTOS ESPECÍFICOS", "O funcionário público que solicita vantagem indevida em razão da função pratica, em tese, o crime de", ("peculato culposo.", "prevaricação.", "concussão.", "corrupção passiva."), "D"),
    Question(47, "CONHECIMENTOS ESPECÍFICOS", "A Lei de Abuso de Autoridade prevê que os crimes nela descritos exigem, como elemento subjetivo especial, finalidade específica, como", ("prejudicar outrem, beneficiar a si mesmo ou a terceiro, ou agir por mero capricho ou satisfação pessoal.", "obter lucro tributário para o erário, ainda que sem dolo.", "produzir resultado naturalístico em todos os casos.", "descumprir ordem verbal sem relação com a função pública."), "A"),
    Question(48, "CONHECIMENTOS ESPECÍFICOS", "Para a Lei de Organização Criminosa, em linhas gerais, organização criminosa pressupõe associação estruturalmente ordenada de", ("duas pessoas, sem divisão de tarefas, para qualquer contravenção.", "três pessoas, sem estabilidade, para infrações de menor potencial ofensivo.", "quatro ou mais pessoas, com divisão de tarefas, visando obter vantagem mediante prática de infrações penais graves ou transnacionais.", "cinco ou mais pessoas, apenas para crimes eleitorais."), "C"),
    Question(49, "CONHECIMENTOS ESPECÍFICOS", "A Lei de Execução Penal estabelece que a execução penal tem por objetivo efetivar as disposições de sentença ou decisão criminal e", ("impedir toda forma de assistência ao preso.", "proporcionar condições para a harmônica integração social do condenado e do internado.", "abolir a disciplina no ambiente prisional.", "transferir ao preso a administração do estabelecimento."), "B"),
    Question(50, "CONHECIMENTOS ESPECÍFICOS", "Segundo a Lei de Acesso à Informação, o acesso à informação pública é regra, sendo o sigilo", ("a regra geral para qualquer documento administrativo.", "exceção, nas hipóteses legalmente previstas.", "determinado livremente por qualquer servidor, sem motivação.", "irrestrito para dados pessoais sensíveis de terceiros."), "B"),
]

class PDF:
    def __init__(self) -> None:
        self.pages: list[str] = []
        self.ops: list[str] = []
        self.page_no = 0
        self.y = 0.0
        self.w, self.h = 595.32, 841.92
        self.margin = 42.5
        self.line_gap = 13.5
        self.font_size = 9.2
        self.current_section = ""

    def esc(self, text: str) -> str:
        text = text.replace("–", "-").replace("—", "-").replace("“", '"').replace("”", '"').replace("’", "'")
        out = []
        for b in text.encode("cp1252", errors="replace"):
            ch = chr(b)
            if ch in "\\()": out.append("\\" + ch)
            elif b < 32 or b > 126: out.append(f"\\{b:03o}")
            else: out.append(ch)
        return "".join(out)

    def add_page(self) -> None:
        if self.ops:
            self.pages.append("\n".join(self.ops))
        self.page_no += 1
        self.ops = []
        self.rect(28, 28, self.w - 56, self.h - 56, stroke=True)
        self.rect(28, self.h - 66, self.w - 56, 38, fill=(0.92,0.92,0.92), stroke=True)
        self.text(42, self.h - 48, "SIMULADO - POLÍCIA PENAL DO ESTADO DE SÃO PAULO", 9.5, "F2")
        self.text(410, self.h - 48, f"Caderno de Questões | Página {self.page_no}", 8.2, "F1")
        self.text(42, self.h - 61, "Modelo inédito para treino - padrão objetivo AOCP", 7.6, "F1")
        self.y = self.h - 88

    def finish(self) -> None:
        if self.ops:
            self.pages.append("\n".join(self.ops))
            self.ops = []

    def text(self, x: float, y: float, s: str, size: float | None = None, font: str = "F1", color: tuple[float,float,float] = (0,0,0)) -> None:
        size = self.font_size if size is None else size
        r, g, b = color
        self.ops.append(f"q {r:.3f} {g:.3f} {b:.3f} rg BT /{font} {size:.2f} Tf {x:.2f} {y:.2f} Td ({self.esc(s)}) Tj ET Q")

    def rect(self, x: float, y: float, w: float, h: float, fill: tuple[float,float,float] | None = None, stroke: bool = False) -> None:
        if fill:
            r,g,b = fill; self.ops.append(f"q {r:.3f} {g:.3f} {b:.3f} rg {x:.2f} {y:.2f} {w:.2f} {h:.2f} re f Q")
        if stroke:
            self.ops.append(f"q 0 0 0 RG 0.6 w {x:.2f} {y:.2f} {w:.2f} {h:.2f} re S Q")

    def ensure(self, needed: float) -> None:
        if self.y - needed < 48:
            self.add_page()

    def line(self, s: str = "", size: float | None = None, font: str = "F1", indent: float = 0) -> None:
        self.ensure(self.line_gap + 2)
        self.text(self.margin + indent, self.y, s, size, font)
        self.y -= self.line_gap

    def para(self, text: str, width: int = 101, size: float | None = None, font: str = "F1", indent: float = 0, first: str = "") -> None:
        for part in text.split("\n"):
            lines = wrap(part, width=width, break_long_words=False) or [""]
            for i, ln in enumerate(lines):
                self.line((first if i == 0 else "") + ln, size=size, font=font, indent=indent)

    def section(self, title: str) -> None:
        self.ensure(30)
        self.rect(self.margin, self.y - 4, self.w - 2*self.margin, 17, fill=(0.12,0.12,0.12), stroke=False)
        self.text(self.margin + 6, self.y, title, 9.4, "F2", color=(1,1,1))
        self.y -= 24
        self.current_section = title

    def question(self, q: Question) -> None:
        if q.area != self.current_section:
            self.section(q.area)
        estimated = 32 + 12 * (len(wrap(q.stem, 96)) + sum(len(wrap(o, 88)) for o in q.options))
        self.ensure(min(estimated, 170))
        self.para(q.stem, width=96, font="F1", first=f"{q.n:02d}. ")
        letters = "ABCD"
        for letter, opt in zip(letters, q.options):
            self.para(opt, width=88, indent=18, first=f"{letter}. ")
        self.y -= 4

    def intro(self) -> None:
        self.add_page()
        self.rect(self.margin, self.y - 40, self.w - 2*self.margin, 32, fill=(0.12,0.12,0.12), stroke=False)
        self.text(self.margin + 88, self.y - 20, "SIMULADO INÉDITO - AOCP | POLÍCIA PENAL/SP", 13, "F2", color=(1,1,1))
        self.y -= 62
        self.section("INSTRUÇÕES INICIAIS")
        for p in INTRO:
            if "\n" in p:
                for ln in p.split("\n"):
                    self.para(ln, width=96, font="F2")
            else:
                self.para(p, width=96)
            self.y -= 6
        self.section("COMPOSIÇÃO DA PROVA")
        for item in ["Língua Portuguesa: 20 questões", "Matemática: 15 questões", "Conhecimentos Específicos: 15 questões", "Alternativas: A, B, C e D", "Tempo recomendado: 3 horas"]:
            self.line("• " + item)
        self.y -= 8
        self.para("Ao terminar, confira o gabarito ao final do caderno e registre os temas que exigem revisão.", width=96, font="F2")

    def answer_key(self) -> None:
        self.add_page()
        self.section("GABARITO")
        cols = 5
        col_w = (self.w - 2*self.margin) / cols
        start_y = self.y
        rows = 10
        for idx, q in enumerate(QUESTIONS):
            col = idx // rows
            row = idx % rows
            x = self.margin + col * col_w
            y = start_y - row * 22
            self.rect(x, y - 6, col_w - 8, 17, fill=(0.97,0.97,0.97) if row % 2 == 0 else None, stroke=True)
            self.text(x + 6, y, f"{q.n:02d}. {q.answer}", 9.4, "F2")
        self.y = start_y - rows * 22 - 20
        self.para("Use este gabarito somente após resolver integralmente o simulado, respeitando o tempo proposto.", width=96)

def build_pdf(path: str) -> None:
    pdf = PDF()
    pdf.intro()
    for q in QUESTIONS:
        pdf.question(q)
    pdf.answer_key()
    pdf.finish()

    objects: list[bytes] = []
    def obj(data: str | bytes) -> int:
        objects.append(data.encode("latin-1") if isinstance(data, str) else data)
        return len(objects)

    catalog = obj("<< /Type /Catalog /Pages 2 0 R >>")
    pages_id = obj(b"")
    font1 = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    font2 = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    page_ids = []
    for content in pdf.pages:
        stream = content.encode("latin-1")
        content_id = obj(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
        page_id = obj(f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {pdf.w:.2f} {pdf.h:.2f}] /Resources << /Font << /F1 {font1} 0 R /F2 {font2} 0 R >> >> /Contents {content_id} 0 R >>")
        page_ids.append(page_id)
    objects[pages_id-1] = f"<< /Type /Pages /Count {len(page_ids)} /Kids [{' '.join(f'{i} 0 R' for i in page_ids)}] >>".encode("latin-1")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for i, data in enumerate(objects, 1):
        offsets.append(len(out))
        out.extend(f"{i} 0 obj\n".encode())
        out.extend(data)
        out.extend(b"\nendobj\n")
    xref = len(out)
    out.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode())
    out.extend(f"trailer << /Size {len(objects)+1} /Root {catalog} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    with open(path, "wb") as f:
        f.write(out)

if __name__ == "__main__":
    build_pdf(PDF_FILE)
    print(f"PDF gerado: {PDF_FILE} ({len(QUESTIONS)} questões)")
