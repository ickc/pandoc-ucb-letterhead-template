#!/usr/bin/env python3

from __future__ import annotations

import subprocess


def get_pandoc_version() -> str:
    """Fetch the Pandoc version using subprocess."""
    return subprocess.run(
        ["pandoc", "--version"], check=True, text=True, capture_output=True
    ).stdout.split("\n")[0]


def get_pandoc_template() -> list[str]:
    """Fetch the default Pandoc LaTeX template using subprocess."""
    return subprocess.run(
        ["pandoc", "--print-default-template=latex"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.split("\n")


def make_ucb_letterhead_template(pandoc_template: list[str]) -> list[str]:
    r"""
    Modify the Pandoc template content by inserting specific lines and
    commenting out or removing certain lines based on the given requirements.

    - Inserts UCB-letterhead setup before $for(header-includes)$.
    - Inserts UCB-letterhead letter start before $for(include-before)$.
    - Inserts \end{letter} after the first $endfor$ following $for(include-after)$.
    - Comments out lines starting with \setkeys{Gin}.
    - Comments out the \maketitle line.
    - Removes $if(graphics)$ and the first $endif$ after it, keeping everything in between intact.
    """
    header_includes_insertion = """
\\usepackage[a-1b]{pdfx}
% begin UCB-letterhead
\\usepackage{fancyhdr} % for fancy headers
\\usepackage{lastpage}
\\pagestyle{fancy}
\\renewcommand{\\headrulewidth}{0pt}
\\fancyhead{} % footer for pages 2 on
\\fancyhfoffset[R]{0pt}
$if(ucb-letterhead.lfoot)$\\lfoot{\\footnotesize {\\textit{$ucb-letterhead.lfoot$}}}$endif$ % Left footer
\\cfoot{$if(ucb-letterhead.cfoot)$\\footnotesize {\\textit{$ucb-letterhead.cfoot$}}$endif$} % Change for center footer
\\rfoot{\\footnotesize Page \\thepage\\ of \\pageref{LastPage}} % Right footer page #s 
\\renewcommand{\\footrulewidth}{0pt}
%first page margins are different to accommodate the letterhead
\\topmargin=-1.1in % Moves the top margin; here it is a negative value to move the text up
\\textheight=9.5in % Total text height for this page
\\oddsidemargin=-10pt % Left margin; widened here with a negative value
\\textwidth=7in % Text width
\\let\\raggedleft\\raggedright % Makes the date appear on the left
% end UCB-letterhead
""".strip()

    include_before_insertion = """
% begin UCB-letterhead
\\begin{letter}{$if(ucb-letterhead.recipient)$$ucb-letterhead.recipient$$endif$} %put the recipient information here and maybe a reference line

\\begin{center}

\\begin{picture}(1000,1)
  \\put(1,-2){\\includegraphics[scale=0.38]{UCBerkeley_wordmark_blue.pdf}}
  \\put(439,-20){\\includegraphics[scale=0.125]{ucberkeleyseal_139_540.pdf}}
  $if(author)$\\put(150,33){\\textbf{\\footnotesize $for(author)$$author$$sep$ \\and $endfor$ }}$endif$
  $if(ucb-letterhead.title)$\\put(150,22){\\footnotesize $ucb-letterhead.title$ }$endif$
  $if(ucb-letterhead.department)$\\put(150,11){\\footnotesize $ucb-letterhead.department$ }$endif$
  $if(ucb-letterhead.address)$\\put(280,33){\\footnotesize $ucb-letterhead.address$ }$endif$
  $if(ucb-letterhead.address2)$\\put(280,22){\\footnotesize $ucb-letterhead.address2$ }$endif$
  $if(ucb-letterhead.phone)$\\put(280,11){\\footnotesize Phone: $ucb-letterhead.phone$ } $endif$
  $if(ucb-letterhead.mobile)$\\put(280,0){\\footnotesize Mobile: $ucb-letterhead.mobile$ }$endif$ % Comment this out to omit your mobile
  $if(ucb-letterhead.email)$\\put(280,-11){\\footnotesize E-mail: $ucb-letterhead.email$ }$endif$
  $if(ucb-letterhead.url)$\\put(280,-22){\\footnotesize $ucb-letterhead.url$ }$endif$
  \\put(0,-28){\\rule{\\textwidth}{0.4pt}}
\\end{picture}
\\end{center}
\\vspace{10mm}
% end UCB-letterhead
""".strip()

    include_after_insertion = "\\end{letter}"

    output_lines = []

    inside_graphics_block = False

    for line in pandoc_template:
        if line.strip() == "$for(header-includes)$":
            output_lines.append(header_includes_insertion)

        if line.strip() == "$for(include-before)$":
            output_lines.append(include_before_insertion)

        if line.strip() == "$if(graphics)$":
            inside_graphics_block = True
            continue

        if inside_graphics_block and line.strip() == "$endif$":
            inside_graphics_block = False
            continue

        if line.strip() == "\\maketitle":
            output_lines.append("% " + line)
            continue

        if line.strip().startswith("\\setkeys{Gin}"):
            output_lines.append("% " + line)
            continue

        output_lines.append(line)

    # Handle insertion after $for(include-after)$ and the first occurrence of $endfor$
    for i, line in enumerate(output_lines):
        if line.strip() == "$for(include-after)$":
            for j in range(i + 1, len(output_lines)):
                if output_lines[j].strip() == "$endfor$":
                    output_lines.insert(j + 1, include_after_insertion)
                    break
            break

    return output_lines


def main() -> None:
    """Generate the Pandoc template with UCB-letterhead insertions and write to stdout."""
    version = get_pandoc_version()
    print(f"% Generated using {version}")
    for line in make_ucb_letterhead_template(get_pandoc_template()):
        print(line)


if __name__ == "__main__":
    main()
