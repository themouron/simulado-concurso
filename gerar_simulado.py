#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera um simulado premium em PDF para Polícia Penal de São Paulo.

O conteúdo foi elaborado a partir da estrutura programática extraída dos PDFs
oficiais presentes no repositório, especialmente os tópicos do edital AOCP:
Língua Portuguesa, Matemática e conhecimentos jurídicos/específicos.
"""
from __future__ import annotations

import math
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

W, H = 595.28, 841.89  # A4 em pontos
MARGIN_X = 42
TOP = 86
BOTTOM = 52
GUTTER = 18
COL_W = (W - 2 * MARGIN_X - GUTTER) / 2
FONT = "Helvetica"
BOLD = "Helvetica-Bold"
ITALIC = "Helvetica-Oblique"
TITLE = "Times-Bold"


def pdf_escape(text: str) -> str:
    text = text.replace("—", "-").replace("•", "-").replace("“", '"').replace("”", '"')
    text = text.replace("’", "'").replace("–", "-").replace("→", "->")
    raw = text.encode("cp1252", errors="replace")
    return raw.decode("latin-1").replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class Canvas:
    def __init__(self):
        self.pages: list[list[str]] = []
        self.c: list[str] = []

    def new_page(self):
        if self.c:
            self.pages.append(self.c)
        self.c = []

    def finish(self):
        if self.c:
            self.pages.append(self.c)
            self.c = []

    def text(self, x, y, txt, size=9, font=FONT, color=(0, 0, 0)):
        r, g, b = color
        self.c.append(f"BT {r:.3f} {g:.3f} {b:.3f} rg /{font_key(font)} {size:.2f} Tf {x:.2f} {y:.2f} Td ({pdf_escape(txt)}) Tj ET")

    def line(self, x1, y1, x2, y2, width=0.5, color=(0, 0, 0)):
        r, g, b = color
        self.c.append(f"q {r:.3f} {g:.3f} {b:.3f} RG {width:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S Q")

    def rect(self, x, y, w, h, stroke=(0, 0, 0), fill=None, width=0.5):
        cmd = "q "
        if fill:
            cmd += f"{fill[0]:.3f} {fill[1]:.3f} {fill[2]:.3f} rg "
        cmd += f"{stroke[0]:.3f} {stroke[1]:.3f} {stroke[2]:.3f} RG {width:.2f} w {x:.2f} {y:.2f} {w:.2f} {h:.2f} re "
        cmd += "B Q" if fill else "S Q"
        self.c.append(cmd)

    def circle(self, x, y, r, stroke=(0, 0, 0), fill=None, width=0.5):
        # aproximação por curvas Bezier
        k = 0.5522847498 * r
        cmd = "q "
        if fill:
            cmd += f"{fill[0]:.3f} {fill[1]:.3f} {fill[2]:.3f} rg "
        cmd += f"{stroke[0]:.3f} {stroke[1]:.3f} {stroke[2]:.3f} RG {width:.2f} w "
        cmd += f"{x+r:.2f} {y:.2f} m {x+r:.2f} {y+k:.2f} {x+k:.2f} {y+r:.2f} {x:.2f} {y+r:.2f} c "
        cmd += f"{x-k:.2f} {y+r:.2f} {x-r:.2f} {y+k:.2f} {x-r:.2f} {y:.2f} c "
        cmd += f"{x-r:.2f} {y-k:.2f} {x-k:.2f} {y-r:.2f} {x:.2f} {y-r:.2f} c "
        cmd += f"{x+k:.2f} {y-r:.2f} {x+r:.2f} {y-k:.2f} {x+r:.2f} {y:.2f} c "
        cmd += "B Q" if fill else "S Q"
        self.c.append(cmd)


FONT_KEYS = {FONT: "F1", BOLD: "F2", ITALIC: "F3", TITLE: "F4", "Times-Roman": "F5"}

def font_key(name):
    return FONT_KEYS[name]


def approx_width(text: str, size: float) -> float:
    # aproximação conservadora para Helvetica/Times; evita estouro de coluna.
    return sum((0.32 if ch in "ilI.,:;!|'" else 0.52 if ch == " " else 0.56) * size for ch in text)


def wrap_text(text: str, width: float, size: float) -> list[str]:
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        words = para.split()
        cur = ""
        for w in words:
            cand = w if not cur else cur + " " + w
            if approx_width(cand, size) <= width:
                cur = cand
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


@dataclass
class Question:
    n: int
    subject: str
    stem: str
    alternatives: list[str]
    answer: str
    figure: str | None = None


@dataclass
class LayoutState:
    canvas: Canvas
    page_no: int = 0
    col: int = 0
    y: float = H - TOP

    def new_exam_page(self):
        self.canvas.new_page()
        self.page_no += 1
        header(self.canvas, self.page_no)
        self.col = 0
        self.y = H - TOP

    @property
    def x(self):
        return MARGIN_X + self.col * (COL_W + GUTTER)

    def next_col_or_page(self):
        if self.col == 0:
            self.col = 1
            self.y = H - TOP
        else:
            self.new_exam_page()


def header(c: Canvas, page_no: int):
    c.rect(36, H - 54, W - 72, 30, stroke=(0.08, 0.08, 0.08), fill=(0.94, 0.95, 0.96), width=0.6)
    c.text(46, H - 39, "SIMULADO AOCP - POLÍCIA PENAL DO ESTADO DE SÃO PAULO", 8.5, BOLD)
    c.text(430, H - 39, "Prova Objetiva | 3 horas", 7.7, BOLD, (0.22, 0.22, 0.22))
    c.line(MARGIN_X + COL_W + GUTTER / 2, H - TOP + 8, MARGIN_X + COL_W + GUTTER / 2, BOTTOM - 8, 0.35, (0.78, 0.78, 0.78))
    c.text(W / 2 - 18, 27, f"Página {page_no}", 7.5, FONT, (0.35, 0.35, 0.35))


def draw_lines(c: Canvas, x, y, lines, size=7.8, font=FONT, leading=9.4, color=(0,0,0)):
    yy = y
    for line in lines:
        c.text(x, yy, line, size, font, color)
        yy -= leading
    return yy


def question_height(q: Question) -> float:
    h = 21
    h += len(wrap_text(q.stem, COL_W - 12, 7.55)) * 9.0
    if q.figure:
        h += 58 if q.figure != "table" else 72
    h += 4
    for alt in q.alternatives:
        h += max(1, len(wrap_text(alt, COL_W - 28, 7.35))) * 8.6 + 2
    return h + 9


def draw_figure(c: Canvas, q: Question, x, y):
    if q.figure == "bars":
        c.rect(x + 8, y - 45, COL_W - 28, 48, stroke=(0.45,0.45,0.45), fill=(0.985,0.985,0.985), width=.4)
        vals = [42, 54, 63, 51]
        labels = ["A", "B", "C", "D"]
        base = y - 37
        c.line(x + 26, base, x + COL_W - 36, base, .35, (.3,.3,.3))
        for i, v in enumerate(vals):
            bx = x + 38 + i * 42
            bh = v * .42
            c.rect(bx, base, 18, bh, stroke=(0.10,0.20,0.34), fill=(0.58,0.70,0.86), width=.3)
            c.text(bx + 2, base - 9, labels[i], 6.5, BOLD)
            c.text(bx - 1, base + bh + 3, str(v), 6.2, FONT)
        c.text(x + 15, y - 7, "Entradas registradas por turno", 6.7, ITALIC, (.25,.25,.25))
        return y - 56
    if q.figure == "triangle":
        c.rect(x + 20, y - 54, COL_W - 52, 55, stroke=(.7,.7,.7), fill=(.99,.99,.99), width=.3)
        x1,y1=x+55,y-42; x2,y2=x+155,y-42; x3,y3=x+55,y-8
        c.line(x1,y1,x2,y2,.8,(.05,.05,.05)); c.line(x1,y1,x3,y3,.8,(.05,.05,.05)); c.line(x2,y2,x3,y3,.8,(.05,.05,.05))
        c.text(x+93,y-51,"24 m",6.8,BOLD); c.text(x+37,y-26,"10 m",6.8,BOLD); c.text(x+113,y-20,"x",7.4,BOLD)
        c.line(x1+5,y1,x1+5,y1+5,.5); c.line(x1,y1+5,x1+5,y1+5,.5)
        return y - 62
    if q.figure == "table":
        c.rect(x+8, y-63, COL_W-24, 64, stroke=(.45,.45,.45), fill=(.99,.99,.99), width=.35)
        rows=[("Faixa de atraso","Frequência"),("0 a 5 min","12"),("6 a 10 min","18"),("11 a 15 min","15"),("16 a 20 min","5")]
        yy=y-12
        for i,(a,b) in enumerate(rows):
            if i==0: c.rect(x+8, yy-2, COL_W-24, 12, stroke=(.25,.25,.25), fill=(.90,.92,.95), width=.25)
            c.text(x+15, yy+1, a, 6.6, BOLD if i==0 else FONT)
            c.text(x+COL_W-73, yy+1, b, 6.6, BOLD if i==0 else FONT)
            yy-=12
        return y-73
    return y


def draw_question(st: LayoutState, q: Question):
    h = question_height(q)
    if st.y - h < BOTTOM:
        st.next_col_or_page()
    c = st.canvas; x = st.x; y = st.y
    c.rect(x, y - h + 5, COL_W, h - 3, stroke=(0.86,0.86,0.86), fill=(1,1,1), width=.25)
    c.rect(x, y - 13, COL_W, 17, stroke=(0.12,0.16,0.20), fill=(0.12,0.16,0.20), width=.25)
    c.text(x + 7, y - 7, f"QUESTÃO {q.n:02d}", 7.4, BOLD, (1,1,1))
    c.text(x + 72, y - 7, q.subject.upper(), 6.7, BOLD, (.82,.87,.93))
    yy = y - 22
    yy = draw_lines(c, x + 7, yy, wrap_text(q.stem, COL_W - 14, 7.55), 7.55, FONT, 9.0)
    if q.figure:
        yy = draw_figure(c, q, x, yy - 2)
    yy -= 2
    letters = "ABCD"
    for letter, alt in zip(letters, q.alternatives):
        c.circle(x + 11, yy + 2.1, 4.1, stroke=(0.20,0.20,0.20), width=.35)
        c.text(x + 8.3, yy - .4, letter, 5.7, BOLD)
        lines = wrap_text(alt, COL_W - 29, 7.35)
        yy = draw_lines(c, x + 22, yy, lines, 7.35, FONT, 8.6)
        yy -= 2
    st.y = y - h - 5


QUESTIONS: list[Question] = []

def add(subject, stem, alts, answer, figure=None):
    QUESTIONS.append(Question(len(QUESTIONS)+1, subject, stem, alts, answer, figure))

# Língua Portuguesa - texto base mais longo e questões de alta interpretação.
texto1 = ("Texto para as questões 01 a 08.\n\n"
"Nas instituições que lidam diariamente com a restrição legítima da liberdade, a rotina costuma ser confundida com repetição mecânica. O equívoco é perigoso. A rotina, quando compreendida como método, protege servidores, custodiados e a própria sociedade; quando reduzida a hábito irrefletido, transforma sinais discretos em ruído e faz parecer normal aquilo que apenas se repetiu muitas vezes. Em ambiente prisional, pequenas alterações de comportamento, de fluxo ou de linguagem podem anteceder incidentes relevantes. Não se exige do agente público uma suspeita permanente, mas uma atenção qualificada, capaz de separar a casualidade do indício.\n\n"
"Também é ilusório imaginar que a humanização do sistema penal se oponha à segurança. A legalidade não enfraquece a disciplina: dá-lhe fundamento. Procedimentos claros, comunicação precisa e registro adequado de ocorrências reduzem improvisos, preservam direitos e dificultam arbitrariedades. Por isso, a autoridade que se exerce no cárcere não se mede pelo tom de voz, mas pela consistência técnica da decisão e pela possibilidade de explicá-la à luz da norma. O servidor que conhece os limites de sua atuação tende a ser mais firme, porque não depende do excesso para se fazer obedecer.\n\n"
"Há, contudo, um obstáculo menos visível: a linguagem burocrática pode encobrir a realidade. Relatórios que trocam fatos por fórmulas vagas, expressões automáticas e eufemismos deixam de informar e passam a apenas preencher arquivos. A palavra oficial, se não descreve com rigor o que ocorreu, compromete a memória institucional. Em tempos de circulação acelerada de boatos, a precisão documental é também forma de proteção: protege quem agiu corretamente, orienta quem apura e impede que a versão mais ruidosa substitua o acontecimento verificável.")
add("Língua Portuguesa", "Com base no Texto I, a tese central é a de que", [
"a rotina prisional deve ser substituída por decisões intuitivas, pois a repetição dificulta a percepção de incidentes.",
"a atuação segura e legítima no sistema prisional depende de método, legalidade e precisão comunicativa.",
"a humanização fragiliza a disciplina quando impede o uso de autoridade em ambientes de alta tensão.",
"o registro burocrático é suficiente para preservar a memória institucional, ainda que não descreva minúcias."], "B")
add("Língua Portuguesa", "No primeiro parágrafo, a oposição entre rotina como método e rotina como hábito irrefletido tem a função de", [
"delimitar uma distinção conceitual que sustenta o restante da argumentação.",
"apresentar uma enumeração de procedimentos administrativos obrigatórios.",
"contrapor servidores experientes e servidores recém-ingressos na carreira.",
"defender que a previsibilidade institucional elimina completamente riscos."], "A")
add("Língua Portuguesa", "Em 'a legalidade não enfraquece a disciplina: dá-lhe fundamento', o sinal de dois-pontos introduz uma relação de", [
"retificação, pois a segunda oração nega integralmente a primeira.",
"explicação, pois a segunda oração esclarece o sentido da afirmação anterior.",
"concessão, pois a segunda oração admite uma exceção à regra geral.",
"conclusão, pois a segunda oração apresenta consequência temporal."], "B")
add("Língua Portuguesa", "A expressão 'atenção qualificada', no contexto, deve ser compreendida como", [
"vigilância baseada em desconfiança constante e generalizada.",
"capacidade técnica de interpretar sinais sem abandonar critérios objetivos.",
"intuição pessoal do servidor adquirida exclusivamente pela antiguidade.",
"procedimento de revista aplicado indistintamente a todos os custodiados."], "B")
add("Língua Portuguesa", "Assinale a alternativa em que a reescrita preserva o sentido e a correção gramatical de: 'O servidor que conhece os limites de sua atuação tende a ser mais firme'.", [
"O servidor, onde conhece os limites de sua atuação, tende ser mais firme.",
"Conhecendo os limites de sua atuação, o servidor tende a ser mais firme.",
"O servidor cujo conhece os limites da atuação tende a ser mais firme.",
"O servidor que conhece os limites de sua atuação tendem a serem mais firmes."], "B")
add("Língua Portuguesa", "No trecho 'não se mede pelo tom de voz, mas pela consistência técnica da decisão', a conjunção 'mas' estabelece", [
"adição de duas características equivalentes da autoridade.",
"alternância entre dois procedimentos igualmente recomendados.",
"oposição argumentativa entre aparência de autoridade e fundamento técnico.",
"causa para o aumento do tom de voz em situações excepcionais."], "C")
add("Língua Portuguesa", "A crítica à linguagem burocrática, no terceiro parágrafo, recai principalmente sobre", [
"o excesso de termos jurídicos inevitáveis em documentos públicos.",
"o uso de registros que substituem a descrição precisa por fórmulas vazias.",
"a necessidade de padronização de relatórios nas instituições públicas.",
"a divulgação de documentos oficiais para a imprensa e para a sociedade."], "B")
add("Língua Portuguesa", "Considerando o texto, a palavra 'eufemismos' foi empregada para indicar expressões que", [
"agravam deliberadamente a descrição de fatos simples.",
"suavizam ou disfarçam a gravidade de determinados acontecimentos.",
"tornam o relatório incompatível com a norma culta.",
"representam estrangeirismos comuns na linguagem administrativa."], "B")
texto2 = ("Texto para as questões 09 a 14.\n\n"
"Se a execução de uma política pública pudesse ser resumida a um organograma, bastaria desenhar caixas e setas. Ocorre que a vida administrativa se realiza nos intervalos entre uma caixa e outra: no memorando que chega incompleto, na ordem verbal que precisa ser confirmada, na urgência que não dispensa motivação, no conflito entre eficiência e cautela. A maturidade institucional aparece quando o servidor percebe que obedecer não é abdicar de pensar; é cumprir a finalidade pública por meios juridicamente sustentáveis.\n\n"
"Essa compreensão não autoriza voluntarismos. Ao contrário: quanto maior o poder conferido ao Estado, maior deve ser a densidade das justificativas. A decisão administrativa não se torna legítima porque parece conveniente ao agente, mas porque encontra suporte na competência, na forma, no motivo, no objeto e na finalidade. A falta de um desses elementos não é detalhe de estilo; pode comprometer o ato e produzir consequências para a Administração e para o agente.")
add("Língua Portuguesa", "Com base no Texto II, a metáfora 'caixas e setas' é utilizada para", [
"reduzir a Administração Pública a um sistema incompatível com controles jurídicos.",
"mostrar que a realidade administrativa é mais complexa que sua representação formal.",
"defender que organogramas devem ser substituídos por ordens verbais.",
"negar a importância de hierarquia em órgãos públicos de segurança."], "B")
add("Língua Portuguesa", "A oração 'quanto maior o poder conferido ao Estado, maior deve ser a densidade das justificativas' expressa ideia de", [
"proporcionalidade.", "condição irreal.", "oposição absoluta.", "finalidade indireta."], "A")
add("Língua Portuguesa", "Em 'obedecer não é abdicar de pensar', o texto sugere que a obediência funcional deve ser", [
"automática, pois a hierarquia dispensa análise do servidor.",
"crítica e juridicamente orientada, sem romper a finalidade pública.",
"facultativa sempre que houver urgência operacional.",
"substituída pela conveniência individual do agente."], "B")
add("Língua Portuguesa", "Assinale a alternativa em que o emprego da crase está correto, conforme a norma-padrão.", [
"O relatório foi encaminhado à autoridade competente antes do plantão.",
"O servidor permaneceu atento à qualquer alteração no pavilhão.",
"A equipe retornou à cumprir a determinação superior.",
"O procedimento foi aplicado à todos os setores da unidade."], "A")
add("Língua Portuguesa", "No trecho 'A falta de um desses elementos não é detalhe de estilo; pode comprometer o ato', o ponto e vírgula", [
"separa orações coordenadas com estreita relação de sentido.",
"introduz uma citação literal de texto normativo.",
"isola aposto explicativo deslocado para o fim do período.",
"marca interrupção sintática típica da oralidade informal."], "A")
add("Língua Portuguesa", "A palavra 'voluntarismos', no contexto, refere-se a condutas administrativas", [
"baseadas na vontade pessoal do agente, sem suficiente amparo jurídico.",
"motivadas por ordem escrita e controle hierárquico formal.",
"dirigidas exclusivamente à proteção de direitos fundamentais.",
"caracterizadas por delegação regular de competência."], "A")
add("Língua Portuguesa", "Assinale a alternativa em que todas as palavras estão acentuadas pela mesma regra.", [
"pública, política, jurídica.", "relatório, memória, competência.", "cárcere, possível, legítima.", "também, porém, órgão."], "A")
add("Língua Portuguesa", "Em 'relatórios que trocam fatos por fórmulas vagas', o termo 'que' exerce função de", [
"pronome relativo, retomando 'relatórios'.", "conjunção integrante, introduzindo oração substantiva.", "partícula expletiva, sem função sintática.", "pronome interrogativo indireto."], "A")
add("Língua Portuguesa", "Assinale a alternativa cuja concordância verbal está de acordo com a norma-padrão.", [
"Fazem três horas que a ocorrência foi registrada.", "Houveram alterações relevantes no fluxo da unidade.", "Existem sinais discretos que antecedem incidentes.", "Tratam-se de documentos indispensáveis à apuração."], "C")
add("Língua Portuguesa", "A colocação pronominal está adequada à norma-padrão em", [
"Não exige-se do servidor suspeita permanente.", "A autoridade se exerce dentro dos limites legais.", "Sempre deve explicar-se a decisão adotada.", "Registraria-se o fato se houvesse formulário disponível."], "B")
add("Língua Portuguesa", "Assinale a alternativa que apresenta relação correta entre termo destacado e classificação sintática: em 'a precisão documental é também forma de proteção', 'forma de proteção' exerce função de", [
"predicativo do sujeito.", "objeto direto.", "adjunto adverbial.", "complemento nominal de precisão."], "A")
add("Língua Portuguesa", "No período 'Procedimentos claros, comunicação precisa e registro adequado reduzem improvisos', a enumeração inicial funciona como", [
"sujeito composto da forma verbal 'reduzem'.", "aposto resumitivo de 'improvisos'.", "vocativo institucional deslocado.", "objeto direto composto da forma verbal."], "A")

# Matemática contextualizada.
add("Matemática", "Em uma unidade prisional, 60 servidores foram distribuídos em três equipes A, B e C. A equipe A tem 8 servidores a mais que a equipe B; a equipe C tem o dobro da equipe B menos 4. O número de servidores da equipe C é", ["24.", "26.", "28.", "30."], "C")
add("Matemática", "Durante uma semana, a quantidade de entradas registradas por turno foi representada no gráfico. Se a meta é reduzir em 20% o total dos dois turnos com maior movimento, o número de entradas a serem reduzidas é", ["21.", "22.", "23.", "24."], "C", "bars")
add("Matemática", "Um lote de 480 formulários deve ser conferido por servidores com a mesma produtividade. Com 6 servidores, a conferência levaria 8 horas. Para concluir o serviço em 5 horas, mantendo-se a produtividade individual, devem atuar", ["8 servidores.", "9 servidores.", "10 servidores.", "12 servidores."], "C")
add("Matemática", "Um investimento institucional de R$ 18.000,00 foi aplicado a juros simples de 1,4% ao mês. Após 10 meses, o montante será de", ["R$ 20.120,00.", "R$ 20.340,00.", "R$ 20.520,00.", "R$ 21.040,00."], "C")
add("Matemática", "A tabela apresenta atrasos, em minutos, observados em 50 deslocamentos internos. Considerando os pontos médios das classes, a média aproximada do atraso é", ["8,6 min.", "9,4 min.", "10,1 min.", "11,2 min."], "B", "table")
add("Matemática", "Um pátio retangular de 36 m por 24 m será cercado internamente por uma faixa de segurança de largura constante x. A área livre central deverá ser 616 m². O valor de x é", ["2 m.", "3 m.", "4 m.", "5 m."], "A")
add("Matemática", "Em uma inspeção, 40% dos itens eram equipamentos de comunicação, 35% eram materiais administrativos e os 30 itens restantes eram de segurança. O total de itens inspecionados foi", ["100.", "110.", "120.", "130."], "C")
add("Matemática", "Um triângulo retângulo representa a distância direta entre dois pontos de vigilância. Com catetos de 10 m e 24 m, a distância direta x é", ["25 m.", "26 m.", "28 m.", "34 m."], "B", "triangle")
add("Matemática", "Uma senha operacional é formada por 3 letras distintas escolhidas entre A, B, C, D e E, seguidas de 2 algarismos distintos escolhidos entre 1, 2, 3 e 4. A quantidade de senhas possíveis é", ["720.", "840.", "960.", "1.200."], "A")
add("Matemática", "Em determinado procedimento, a probabilidade de um formulário conter erro de preenchimento é 0,08. Selecionados dois formulários de modo independente, a probabilidade de pelo menos um conter erro é", ["0,0064.", "0,0736.", "0,1536.", "0,1600."], "C")
add("Matemática", "A sequência 7, 11, 15, 19, ... representa o número acumulado de relatórios ao final de sucessivas horas extras. O 18º termo dessa progressão é", ["71.", "73.", "75.", "77."], "C")
add("Matemática", "A função C(t)=120+18t representa, em reais, o custo de manutenção após t horas de uso de determinado equipamento. Se o custo total foi R$ 426,00, então t foi igual a", ["15.", "16.", "17.", "18."], "C")
add("Matemática", "Uma sala retangular foi representada em escala 1:200. No desenho, suas medidas são 4,5 cm e 3,0 cm. A área real da sala é", ["36 m².", "48 m².", "54 m².", "60 m²."], "C")
add("Matemática", "Três setores consumiram, juntos, 1.260 folhas. O segundo consumiu 20% a mais que o primeiro, e o terceiro consumiu 60 folhas a menos que o segundo. O primeiro setor consumiu", ["360 folhas.", "380 folhas.", "400 folhas.", "420 folhas."], "C")
add("Matemática", "Um cilindro de raio 3 cm e altura 20 cm tem volume, em cm³, igual a (adote pi = 3,14)", ["376,8.", "471,0.", "565,2.", "628,0."], "C")

# Conhecimentos específicos com base no programa do edital extraído dos PDFs.
add("Conhecimentos Específicos", "À luz dos princípios da Administração Pública e dos elementos do ato administrativo, assinale a alternativa correta.", [
"A finalidade do ato pode ser livremente escolhida pelo agente quando houver conveniência administrativa.",
"Competência, forma, motivo, objeto e finalidade são referências essenciais para aferir a validade do ato.",
"A revogação incide sobre atos ilegais e produz, necessariamente, efeitos retroativos.",
"A convalidação é obrigatória em qualquer vício, inclusive quando houver desvio de finalidade."], "B")
add("Conhecimentos Específicos", "Sobre organização administrativa, centralização, descentralização, concentração e desconcentração, assinale a alternativa correta.", [
"Desconcentração pressupõe criação de pessoa jurídica distinta da entidade originária.",
"Descentralização ocorre apenas quando há distribuição interna de competências entre órgãos.",
"Concentração e desconcentração relacionam-se à distribuição de competências dentro da mesma pessoa jurídica.",
"Administração indireta é composta exclusivamente por órgãos sem personalidade jurídica."], "C")
add("Conhecimentos Específicos", "Nos termos gerais do regime disciplinar de agentes públicos, a responsabilidade administrativa", [
"exclui automaticamente a responsabilidade civil e penal pelo mesmo fato.",
"pode coexistir com responsabilidades civil e criminal, conforme a natureza da conduta.",
"somente é apurada se houver condenação penal transitada em julgado.",
"depende sempre de dano material quantificável ao erário."], "B")
add("Conhecimentos Específicos", "Conforme a Constituição Federal, os direitos e garantias fundamentais", [
"podem ser afastados por regulamento administrativo sempre que houver interesse público genérico.",
"incluem garantias de legalidade, devido processo legal e proteção contra tratamento desumano ou degradante.",
"aplicam-se exclusivamente a brasileiros natos em território nacional.",
"impedem qualquer forma de restrição de liberdade determinada pelo Estado."], "B")
add("Conhecimentos Específicos", "No capítulo constitucional da Segurança Pública, a Polícia Penal", [
"integra a segurança pública e vincula-se à segurança dos estabelecimentos penais.",
"substitui integralmente as funções jurisdicionais da execução penal.",
"exerce policiamento ostensivo geral em igualdade de atribuições com a polícia militar.",
"atua apenas mediante autorização judicial individual para cada ato de rotina."], "A")
add("Conhecimentos Específicos", "A respeito da aplicação da lei penal, assinale a alternativa correta.", [
"A lei penal posterior que favorece o agente retroage, ainda que já tenha havido condenação definitiva.",
"A lei excepcional perde todos os efeitos sobre fatos praticados durante sua vigência.",
"A analogia pode criar crime e pena quando houver lacuna legislativa relevante.",
"A lei penal mais grave retroage quando o crime envolver administração pública."], "A")
add("Conhecimentos Específicos", "No Direito Penal, o crime doloso ocorre quando o agente", [
"age sem consciência da conduta, mas produz resultado típico.",
"quer o resultado ou assume o risco de produzi-lo.",
"descumpre dever de cuidado sem prever qualquer consequência.",
"pratica fato atípico por erro plenamente justificável."], "B")
add("Conhecimentos Específicos", "Nos crimes contra a Administração Pública, o peculato, em linhas gerais, pressupõe que o funcionário público", [
"solicite vantagem indevida em razão da função, ainda sem posse de bem público.",
"retarde ato de ofício para satisfazer interesse pessoal, sem apropriação de valores.",
"aproprie-se ou desvie bem móvel público ou particular de que tem posse em razão do cargo.",
"atribua a terceiro fato definido como crime sabendo-o inocente."], "C")
add("Conhecimentos Específicos", "A Lei de Execução Penal prevê que a execução penal deve proporcionar condições para", [
"o isolamento absoluto do condenado, como finalidade autônoma da pena.",
"a harmônica integração social do condenado e do internado, além de efetivar a sentença.",
"a transferência da função jurisdicional ao diretor do estabelecimento penal.",
"a aplicação de sanções disciplinares sem necessidade de procedimento."], "B")
add("Conhecimentos Específicos", "Nos termos da Lei de Abuso de Autoridade (Lei nº 13.869/2019), é correto afirmar que", [
"qualquer divergência interpretativa razoável configura crime de abuso de autoridade.",
"os crimes exigem, em regra, finalidade específica de prejudicar, beneficiar ou agir por capricho ou satisfação pessoal.",
"a responsabilização penal dispensa análise de dolo e finalidade do agente.",
"a lei aplica-se somente a autoridades do Poder Judiciário."], "B")
add("Conhecimentos Específicos", "A Lei de Organizações Criminosas (Lei nº 12.850/2013) caracteriza organização criminosa, entre outros requisitos, pela associação de", [
"duas pessoas, ainda sem divisão de tarefas, para qualquer contravenção penal.",
"quatro ou mais pessoas, estruturalmente ordenada e com divisão de tarefas, visando obter vantagem mediante crimes previstos na lei.",
"três pessoas, apenas quando houver vínculo familiar entre os envolvidos.",
"qualquer número de pessoas, desde que o crime seja praticado em ambiente prisional."], "B")
add("Conhecimentos Específicos", "Segundo a Lei de Acesso à Informação, a publicidade é diretriz geral da Administração Pública, sendo o sigilo", [
"a regra para documentos produzidos por órgãos de segurança.",
"exceção, admitida nas hipóteses legais e pelo prazo necessário.",
"vedado em qualquer documento público, independentemente do conteúdo.",
"definido livremente pelo servidor responsável pelo protocolo."], "B")
add("Conhecimentos Específicos", "A Declaração Universal dos Direitos Humanos afirma, em sua lógica geral, que", [
"a dignidade humana depende de nacionalidade e condição processual.",
"todas as pessoas nascem livres e iguais em dignidade e direitos.",
"direitos humanos são prerrogativas exclusivas de pessoas sem condenação criminal.",
"a vedação à tortura admite exceções em situações de emergência administrativa."], "B")
add("Conhecimentos Específicos", "No âmbito da ética pública, integridade administrativa e prevenção de conflitos de interesse exigem que o agente público", [
"confunda interesse institucional e interesse privado quando ambos parecerem úteis.",
"atue com transparência, impessoalidade e lealdade às finalidades públicas.",
"priorize relações pessoais se isso acelerar a solução informal de demandas.",
"dispense registro de decisões sensíveis para preservar a celeridade."], "B")
add("Conhecimentos Específicos", "Considerando a Polícia Penal paulista e o conteúdo programático de legislação estadual, é correto afirmar que o estudo da carreira envolve", [
"apenas normas federais de processo penal, excluídas normas estaduais sobre servidores.",
"normas constitucionais estaduais, lei orgânica, estatuto funcional e regras disciplinares aplicáveis.",
"somente conhecimentos de informática e atualidades, por serem matérias transversais.",
"exclusivamente a Lei de Drogas e a Lei de Crimes Hediondos."], "B")


def intro(c: Canvas):
    c.new_page()
    c.rect(0, 0, W, H, stroke=(1,1,1), fill=(0.97,0.98,0.99), width=0)
    c.rect(42, 690, W-84, 78, stroke=(0.08,0.13,0.18), fill=(0.08,0.13,0.18), width=.5)
    c.text(62, 738, "SIMULADO PREMIUM", 17, TITLE, (1,1,1))
    c.text(62, 714, "POLÍCIA PENAL DO ESTADO DE SÃO PAULO", 15, BOLD, (.86,.91,.96))
    c.text(62, 696, "Padrão AOCP | Prova objetiva | Duração total: 3 horas", 9.5, FONT, (.88,.88,.88))
    c.rect(62, 210, W-124, 430, stroke=(0.78,0.80,0.82), fill=(1,1,1), width=.5)
    y=607
    c.text(84, y, "Antes de iniciar", 15, BOLD, (.08,.13,.18)); y-=32
    intro_lines = [
        "Este simulado foi preparado para reproduzir, com rigor e seriedade, a experiência de uma prova objetiva da banca AOCP para a Polícia Penal de São Paulo.",
        "Reserve 3 horas completas, marque o tempo no relógio e respeite o limite como se estivesse no dia oficial do concurso.",
        "Desative notificações, afaste o celular, evite consultas e mantenha sobre a mesa apenas o material que seria permitido no ambiente real de prova.",
        "Procure um local silencioso, sente-se com postura de prova e responda às questões na ordem que considerar estratégica, sem pausar o cronômetro.",
        "Ao final, confira o gabarito apenas depois de concluir toda a prova. O objetivo é treinar domínio de conteúdo, resistência e tomada de decisão sob pressão.",
    ]
    for para in intro_lines:
        lines = wrap_text(para, W-178, 10.4)
        y = draw_lines(c, 84, y, lines, 10.4, FONT, 14.2)
        y -= 9
    c.rect(84, 255, W-168, 56, stroke=(0.12,0.16,0.20), fill=(0.94,0.96,0.98), width=.4)
    c.text(102, 288, "Professor Mourão", 13, BOLD, (.08,.13,.18))
    c.text(102, 268, "@mouraoprofessor", 11, FONT, (.22,.22,.22))
    c.text(84, 178, "Quando estiver pronto, vire a página e comece a prova.", 10, ITALIC, (.18,.18,.18))



def text_block_height(text: str) -> float:
    return 28 + len(wrap_text(text, COL_W - 18, 7.25)) * 8.45


def draw_text_block(st: LayoutState, title: str, text: str):
    h = text_block_height(text)
    if st.y - h < BOTTOM:
        st.next_col_or_page()
    x = st.x; y = st.y; c = st.canvas
    c.rect(x, y - h + 5, COL_W, h - 2, stroke=(0.68,0.70,0.72), fill=(0.985,0.988,0.992), width=.35)
    c.rect(x, y - 15, COL_W, 19, stroke=(0.18,0.22,0.26), fill=(0.18,0.22,0.26), width=.25)
    c.text(x + 8, y - 8, title, 7.8, BOLD, (1,1,1))
    yy = y - 25
    for para in text.split("\n\n"):
        yy = draw_lines(c, x + 9, yy, wrap_text(para, COL_W - 18, 7.25), 7.25, FONT, 8.45)
        yy -= 5
    st.y = y - h - 6

def section_title(st: LayoutState, title: str, subtitle: str):
    if st.y - 38 < BOTTOM:
        st.next_col_or_page()
    x=st.x; y=st.y
    st.canvas.rect(x, y-25, COL_W, 25, stroke=(0.10,0.14,0.18), fill=(0.10,0.14,0.18), width=.25)
    st.canvas.text(x+8, y-10, title, 9, BOLD, (1,1,1))
    st.canvas.text(x+8, y-21, subtitle, 6.7, FONT, (.88,.88,.88))
    st.y -= 37


def answer_key(c: Canvas):
    c.new_page()
    c.rect(0, 0, W, H, stroke=(1,1,1), fill=(0.98,0.985,0.99), width=0)
    c.rect(42, H-82, W-84, 42, stroke=(0.08,0.13,0.18), fill=(0.08,0.13,0.18), width=.4)
    c.text(58, H-59, "GABARITO PRELIMINAR", 15, TITLE, (1,1,1))
    c.text(388, H-59, "Simulado AOCP - Polícia Penal SP", 8.5, FONT, (.85,.88,.92))
    subjects = [("Língua Portuguesa", 1, 20), ("Matemática", 21, 35), ("Conhecimentos Específicos", 36, 50)]
    x0=62; y0=700
    for idx,(name,a,b) in enumerate(subjects):
        x=x0+idx*168
        c.rect(x, y0-300, 150, 318, stroke=(0.72,0.74,0.76), fill=(1,1,1), width=.45)
        c.rect(x, y0, 150, 18, stroke=(0.12,0.16,0.20), fill=(0.12,0.16,0.20), width=.3)
        c.text(x+8, y0+5, name, 7.5, BOLD, (1,1,1))
        yy=y0-18
        for n in range(a,b+1):
            ans=QUESTIONS[n-1].answer
            c.text(x+14, yy, f"{n:02d}", 8, BOLD)
            for j,letter in enumerate("ABCD"):
                cx=x+50+j*23
                fill=(0.10,0.16,0.24) if letter==ans else None
                c.circle(cx, yy+2.5, 5.2, stroke=(0.12,0.12,0.12), fill=fill, width=.35)
                c.text(cx-2.6, yy, letter, 5.6, BOLD, (1,1,1) if letter==ans else (0,0,0))
            yy-=18
    c.text(62, 315, "Observação: utilize o gabarito apenas após concluir a prova dentro do tempo de 3 horas.", 8.5, ITALIC, (.25,.25,.25))
    c.text(W/2-18, 27, "Gabarito", 7.5, FONT, (.35,.35,.35))


def rebalance_answers():
    """Distribui as respostas corretas para evitar padrões artificiais no gabarito."""
    desired = list("BADBCADCABDACBDCABDA" "CDABDCABDCABDCA" "BCADBACDBADCBAD")
    assert len(desired) == len(QUESTIONS)
    for q, target in zip(QUESTIONS, desired):
        current_idx = "ABCD".index(q.answer)
        target_idx = "ABCD".index(target)
        if current_idx != target_idx:
            alts = q.alternatives[:]
            correct = alts.pop(current_idx)
            alts.insert(target_idx, correct)
            q.alternatives = alts
            q.answer = target

rebalance_answers()


def build_pdf(path: Path):
    c=Canvas()
    intro(c)
    st=LayoutState(c)
    st.new_exam_page()
    section_title(st, "LÍNGUA PORTUGUESA", "Questões 01 a 20")
    draw_text_block(st, "TEXTO I - para as questões 01 a 08", texto1.replace("Texto para as questões 01 a 08.\n\n", ""))
    for q in QUESTIONS[:8]:
        draw_question(st,q)
    draw_text_block(st, "TEXTO II - para as questões 09 a 14", texto2.replace("Texto para as questões 09 a 14.\n\n", ""))
    for q in QUESTIONS[8:20]:
        draw_question(st,q)
    section_title(st, "MATEMÁTICA", "Questões 21 a 35")
    for q in QUESTIONS[20:35]:
        draw_question(st,q)
    section_title(st, "CONHECIMENTOS ESPECÍFICOS", "Questões 36 a 50")
    for q in QUESTIONS[35:]:
        draw_question(st,q)
    answer_key(c)
    c.finish()
    write_pdf(path, c.pages)


def write_pdf(path: Path, pages: list[list[str]]):
    objects=[]
    def obj(s):
        objects.append(s.encode('latin-1'))
        return len(objects)
    catalog_id=1; pages_id=2
    objects=[b'', b'']
    font_obj = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    font_bold_obj = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    font_it_obj = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>")
    font_title_obj = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>")
    font_times_obj = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>")
    page_ids=[]
    for page in pages:
        stream="\n".join(page).encode('latin-1')
        content_id=obj(f"<< /Length {len(stream)} >>\nstream\n".encode('latin-1').decode('latin-1') + stream.decode('latin-1') + "\nendstream")
        res=f"<< /Font << /F1 {font_obj} 0 R /F2 {font_bold_obj} 0 R /F3 {font_it_obj} 0 R /F4 {font_title_obj} 0 R /F5 {font_times_obj} 0 R >> >>"
        page_id=obj(f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {W:.2f} {H:.2f}] /Resources {res} /Contents {content_id} 0 R >>")
        page_ids.append(page_id)
    objects[catalog_id-1]=f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode('latin-1')
    kids=" ".join(f"{i} 0 R" for i in page_ids)
    objects[pages_id-1]=f"<< /Type /Pages /Count {len(page_ids)} /Kids [ {kids} ] >>".encode('latin-1')
    out=bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets=[]
    for i,o in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{i} 0 obj\n".encode('latin-1')+o+b"\nendobj\n")
    xref=len(out)
    out.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode('latin-1'))
    for off in offsets:
        out.extend(f"{off:010d} 00000 n \n".encode('latin-1'))
    out.extend(f"trailer\n<< /Size {len(objects)+1} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode('latin-1'))
    path.write_bytes(out)


if __name__ == "__main__":
    assert len(QUESTIONS)==50
    build_pdf(Path("simulado_aocp_policia_penal_sp.pdf"))
    print("PDF gerado: simulado_aocp_policia_penal_sp.pdf")
