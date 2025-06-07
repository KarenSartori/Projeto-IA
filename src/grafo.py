from graphviz import Digraph

def exibir_arvore_restricao(arvore, objetivo=None):
    dot = Digraph(comment='Árvore de Restrição - A*')
    dot.attr(rankdir='TB', fontsize='12', nodesep='0.6')

    for (x, y), info in arvore.items():
        g = info['g']
        h = info['h']
        f = info['f']
        pai = info['pai']
        pos_id = f"{x},{y}"

        atual_str = f"({x},{y})"
        pai_str = f"({pai[0]},{pai[1]})" if pai else "None"
        f_str = f"f={f:.1f}"

        label = f'''<
<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>{atual_str}</TD>
    <TD>{pai_str}</TD>
    <TD>{f_str}</TD>
  </TR>
</TABLE>>'''

        dot.node(pos_id, label=label, shape='plaintext')

        if pai:
            pai_id = f"{pai[0]},{pai[1]}"
            peso = round(g - arvore[pai]['g'], 1)
            dot.edge(pai_id, pos_id, label=str(peso))

    dot.render('arvore_mapamedio', format='pdf', view=True)
