window.MathJax = {
    tex2jax: {
      inlineMath: [ ['\\(','\\)'] ],
      processEscapes: true
    },
    TeX: {
        TagSide: "left",
        TagIndent: "0em",
        Macros: {
	    ket: ["{\\lvert #1 \\rangle}",1],
	    near: "\\ \\mathrm{near}\\ ",
	    amp: "\\mathbin{\\&}",
            bfrac: ["{^{#1}\\unicode{x2044}_{#2}}",2],
	    dproves: "\\,\\rvert\\!{\\sim}\\,",
	    llbracket: "[\\![",
	    rrbracket: "]\\!]"
	}
    },
    "HTML-CSS": { linebreaks: { automatic: true } },
    "SVG": { linebreaks: { automatic: true } },
};
