#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Organiza um curso (Udemy) a partir de um Index.md com a estrutura:

### Section X: Título
N. Nome da Aula `Xmin`
- Recurso 1
- Recurso 2
Assignment N: Título do Assignment
N+1. Outra Aula `Ymin`
- Recurso ...

Cria pastas por seção e por aula (com normalização amigável a Windows e Linux),
e cria "0. Index.md" em cada nível quando não existirem.
"""

import logging
import re
import sys
from pathlib import Path
from typing import Optional
import unicodedata
import html

# ---------------------- Configuração de Logging ---------------------- #
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Também registrar em arquivo
    fh = logging.FileHandler("organiza_udemy.log", encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


# ---------------------- Normalização de Nomes ---------------------- #
WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}

INVALID_REGEX = re.compile(r'[<>:"/\\|?\*\x00]')  # inválidos no Windows

def normalize_name(name: str) -> str:
    """
    Normaliza o nome para ser válido em Windows e Linux:
    - Decodifica entidades HTML (&amp; -> &)
    - Substitui & por ' and '
    - Troca ':' por ' - '
    - Remove/ajusta caracteres inválidos < > : " / \ | ? *
    - Remove backticks ` e exclamação !
    - Substitui / \ | por '-'
    - Substitui aspas duplas por simples
    - Colapsa espaços múltiplos e hifens duplicados
    - Remove pontos/espaços no início/fim e ponto no final (Windows)
    - Evita nomes reservados (Windows): adiciona '_'
    - Limita tamanho para 240 chars
    """
    if not isinstance(name, str):
        name = str(name)

    # Decodifica entidades HTML
    name = html.unescape(name)

    # Normalizações semânticas
    name = name.replace("&", " and ")
    name = name.replace(":", " - ")

    # Remoção de alguns sinais supérfluos
    name = name.replace("`", "")
    name = name.replace("!", "")

    # Substitui barras e pipe por hífen
    name = name.replace("/", "-").replace("\\", "-").replace("|", "-")

    # Substitui aspas duplas por simples
    name = name.replace('"', "'")

    # Remove caracteres inválidos
    name = INVALID_REGEX.sub("", name)

    # Normaliza unicode
    name = unicodedata.normalize("NFKC", name)

    # Colapsa espaços múltiplos e hifens duplicados
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r"\-\s*\-", "-", name)

    # Trim e proibições do Windows
    name = name.strip(" .\t\r\n")
    if name.endswith("."):
        name = name.rstrip(".")

    if not name:
        name = "Untitled"

    base_upper = name.upper()
    if base_upper in WINDOWS_RESERVED_NAMES:
        name = name + "_"

    if len(name) > 240:
        name = name[:240].rstrip()

    return name


# ---------------------- Parsing do Index.md ---------------------- #
SECTION_HEADER_RE = re.compile(r"^\s*#{3}\s+(.*\S)\s*$")  # ### Section 1: Título

# Aula com duração: "331. Module Introduction `1min`"
LESSON_WITH_DURATION_RE = re.compile(
    r"^\s*(\d+)\.\s+(.*?)\s*`(\d+\s*min)`\s*$",
    re.IGNORECASE,
)

# Assignment sem duração: "Assignment 1: Practicing Components"
ASSIGNMENT_RE = re.compile(
    r"^\s*Assignment\s+(\d+):\s+(.*\S)\s*$",
    re.IGNORECASE,
)

BULLET_RE = re.compile(r"^\s*-\s+(.*\S)\s*$")

class Lesson:
    def __init__(self, raw_line: str, number: int, title: str, duration: Optional[str], line_no: int):
        self.raw_line = raw_line
        self.number = number
        self.title = title
        self.duration = duration  # pode ser None (Assignments)
        self.resources = []  # list[str]
        self.line_no = line_no

    @property
    def folder_basename(self) -> str:
        # Nome da pasta até o primeiro backtick, se houver; senão, linha inteira
        raw = self.raw_line.strip()
        if "`" in raw:
            before_tick = raw.split("`", 1)[0].strip()
        else:
            before_tick = raw
        return normalize_name(before_tick)

class Section:
    def __init__(self, header_text: str, line_no: int):
        self.header_text = header_text  # manter como usuário definiu
        self.line_no = line_no
        self.lessons = []  # list[Lesson]

    @property
    def folder_basename(self) -> str:
        # Usar o header, normalizado
        return normalize_name(self.header_text)


def find_index_file(base_dir: Path) -> Optional[Path]:
    for candidate in ("0. Index.md", "Index.md"):
        p = base_dir / candidate
        if p.exists() and p.is_file():
            return p
    return None


def parse_index_file(index_path: Path):
    errors = []
    sections = []
    current_section: Optional[Section] = None
    current_lesson: Optional[Lesson] = None

    logging.info(f"Lendo arquivo de índice: {index_path}")

    with index_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")

        if not line.strip():
            # Linha em branco: apenas ignora (mantém current_lesson)
            continue

        # Cabeçalho de seção (### ...)
        m_sec = SECTION_HEADER_RE.match(line)
        if m_sec:
            header_text = m_sec.group(1).strip()
            # Validar que começa com "Section"
            if not header_text.lower().startswith("section"):
                errors.append(
                    f"Linha {i}: Header de nível 3 não inicia com 'Section': {line!r}"
                )
            current_section = Section(header_text=header_text, line_no=i)
            sections.append(current_section)
            current_lesson = None
            logging.info(f"Seção detectada (linha {i}): {header_text}")
            continue

        # Aula com duração (N. ... `Xmin`)
        m_less_dur = LESSON_WITH_DURATION_RE.match(line)
        if m_less_dur:
            if current_section is None:
                errors.append(
                    f"Linha {i}: Aula encontrada fora de uma seção: {line!r}"
                )
                if sections and sections[-1].header_text == "Sem Seção":
                    current_section = sections[-1]
                else:
                    current_section = Section("Sem Seção", i)
                    sections.append(current_section)

            number = int(m_less_dur.group(1))
            title = m_less_dur.group(2).strip()
            duration = m_less_dur.group(3).replace(" ", "").lower()  # normaliza `2min`
            lesson = Lesson(raw_line=line.strip(), number=number, title=title, duration=duration, line_no=i)
            current_section.lessons.append(lesson)
            current_lesson = lesson
            logging.info(f"Aula (com duração) detectada (linha {i}): {lesson.raw_line}")
            continue

        # Assignment sem duração
        m_assign = ASSIGNMENT_RE.match(line)
        if m_assign:
            if current_section is None:
                errors.append(
                    f"Linha {i}: Assignment encontrado fora de uma seção: {line!r}"
                )
                if sections and sections[-1].header_text == "Sem Seção":
                    current_section = sections[-1]
                else:
                    current_section = Section("Sem Seção", i)
                    sections.append(current_section)

            number = int(m_assign.group(1))
            title = m_assign.group(2).strip()
            lesson = Lesson(raw_line=line.strip(), number=number, title=title, duration=None, line_no=i)
            current_section.lessons.append(lesson)
            current_lesson = lesson
            logging.info(f"Assignment (sem duração) detectado (linha {i}): {lesson.raw_line}")
            continue

        # Recurso (bullet) - deve vir após uma aula/assignment
        m_bul = BULLET_RE.match(line)
        if m_bul:
            if current_lesson is None:
                errors.append(
                    f"Linha {i}: Recurso sem uma aula imediatamente anterior: {line!r}"
                )
            else:
                res_text = m_bul.group(1).strip()
                current_lesson.resources.append(res_text)
                logging.info(f"Recurso detectado (linha {i}): {res_text}")
            continue

        # Qualquer outra coisa é erro de formatação
        errors.append(f"Linha {i}: Formato inesperado: {line!r}")

    return sections, errors


# ---------------------- Escrita de Arquivos/Criação de Pastas ---------------------- #
def ensure_dir(p: Path):
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
        logging.info(f"[CREATE DIR] {p}")
    else:
        logging.info(f"[EXISTS DIR] {p}")

def ensure_file(p: Path, content: str):
    if not p.exists():
        # Path.write_text não aceita newline=...
        p.write_text(content, encoding="utf-8")
        logging.info(f"[CREATE FILE] {p}")
    else:
        logging.info(f"[EXISTS FILE] {p}")

def write_section_index(section_dir: Path, section: Section):
    """
    Cria '0. Index.md' da seção (se não existir) com o nome da seção e a lista de aulas.
    """
    lines = []
    lines.append(f"# {section.header_text}\n")
    if not section.lessons:
        lines.append("\n> (Sem aulas registradas nesta seção)\n")
    else:
        lines.append("\n## Aulas\n")
        for lesson in section.lessons:
            # Mostrar exatamente a linha da aula como estava no índice raiz
            lines.append(f"- {lesson.raw_line}\n")

    content = "".join(lines)
    ensure_file(section_dir / "0. Index.md", content)

def write_lesson_index(lesson_dir: Path, lesson: Lesson):
    """
    Cria '0. Index.md' da aula (se não existir) com os recursos da aula
    ou 'Sem Recursos' se não houver.
    """
    lines = []
    lines.append(f"# {lesson.number}. {lesson.title}\n")
    if lesson.duration:
        lines.append(f"\n> Duração: `{lesson.duration}`\n\n")
    else:
        lines.append(f"\n> Duração: (não informada)\n\n")

    if lesson.resources:
        lines.append("## Recursos\n")
        for r in lesson.resources:
            lines.append(f"- {r}\n")
    else:
        lines.append("Sem Recursos\n")

    content = "".join(lines)
    ensure_file(lesson_dir / "0. Index.md", content)


# ---------------------- Fluxo Principal ---------------------- #
def main():
    setup_logging()

    base_dir = Path.cwd()
    logging.info(f"Procurando por '0. Index.md' ou 'Index.md' em: {base_dir}")

    index_file = find_index_file(base_dir)
    if not index_file:
        logging.error("Arquivo '0. Index.md' ou 'Index.md' não encontrado no diretório atual. Encerrando.")
        sys.exit(1)

    sections, parse_errors = parse_index_file(index_file)

    if parse_errors:
        logging.error("Foram encontrados problemas de formatação no arquivo de índice:")
        for e in parse_errors:
            logging.error(f" - {e}")

    # Criação de estrutura
    for section in sections:
        section_dir = base_dir / section.folder_basename
        ensure_dir(section_dir)

        # Index da seção
        write_section_index(section_dir, section)

        # Aulas
        for lesson in section.lessons:
            lesson_dir = section_dir / lesson.folder_basename
            ensure_dir(lesson_dir)
            write_lesson_index(lesson_dir, lesson)

    if parse_errors:
        logging.info("Processo finalizado COM ERROS (ver acima e em organiza_udemy.log).")
        # Se preferir falhar o processo em caso de erro de formatação:
        # sys.exit(2)
    else:
        logging.info("Processo finalizado sem erros de formatação.")

if __name__ == "__main__":
    main()