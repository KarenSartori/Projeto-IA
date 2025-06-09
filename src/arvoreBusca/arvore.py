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

        if idx == 0:
            g = h = f = 0

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
          candidatos = [
              (j, pj) for j, pj in enumerate(arvore[:idx])
              if pj['x'] == pai[0] and pj['y'] == pai[1]
          ]

          if candidatos:
              j_melhor, pai_melhor = min(candidatos, key=lambda item: item[1]['g'])
              pai_id = f"{pai_melhor['x']},{pai_melhor['y']}_{j_melhor}"
              peso = round(g, 1)
              dot.edge(pai_id, pos_id, label=str(peso))

    dot.render('arvore', format='pdf')

