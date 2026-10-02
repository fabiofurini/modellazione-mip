// Le stesse abbreviazioni del preambolo delle dispense: senza, il browser
// stampa \Z invece di Z. I corpi vanno tenuti identici a quelli di
// dispensa_1/preambolo.tex, altrimenti sito e PDF divergono.
window.MathJax = {
  tex: { inlineMath: [["\\(", "\\)"], ["$", "$"]],
         displayMath: [["\\[", "\\]"], ["$$", "$$"]],
         processEscapes: true,
         macros: {
           R: "\\mathbb{R}",
           Q: "\\mathbb{Q}",
           Z: "\\mathbb{Z}",
           E: "\\mathbb{E}",
           Prob: "\\mathbb{P}",
           var: "\\mathrm{VaR}",
           cvar: "\\mathrm{CVaR}",
           AND: "\\mathrel{\\texttt{ AND }}",
           OR: "\\mathrel{\\texttt{ OR }}",
           NOT: "\\mathop{\\texttt{NOT}}\\,",
           true: "\\texttt{TRUE}",
           false: "\\texttt{FALSE}",
           zmilp: "z(\\mathit{MILP})",
           zlp: "z(\\mathit{LP})",
           zlpp: "z(\\mathit{LP}^+)",
           zlppp: "z(\\mathit{LP}^{++})",
           zdual: "z(\\mathit{D}(\\mathit{LP}))",
           ub: "\\mathit{UB}",
           lb: "\\mathit{LB}"
         } },
  options: { ignoreHtmlClass: ".*|", processHtmlClass: "arithmatex" }
};
