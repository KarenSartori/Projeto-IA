from graphviz import Digraph

def exibir_arvore(arvore):
    dot = Digraph(comment='Árvore de Busca - A*')
    dot.attr(rankdir='TB', fontsize='12', nodesep='0.6')

    for idx, info in enumerate(arvore):
        x = info['x']
        y = info['y']
        g = info['g']
        h = info['h']
        f = info['f']
        pai = info['pai']
        pos_id = f"{x},{y}_{idx}"  

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
            for j in reversed(range(idx)):
                pj = arvore[j]
                if pj['x'] == pai[0] and pj['y'] == pai[1]:
                    pai_id = f"{pj['x']},{pj['y']}_{j}"
                    peso = round(g - pj['g'], 1)
                    dot.edge(pai_id, pos_id, label=str(peso))
                    break

    dot.render('arvore', format='pdf')
