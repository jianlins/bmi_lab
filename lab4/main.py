# %%
import pyConTextNLP.pyConText as pyConText
import pyConTextNLP.itemData as itemData
import networkx as nx
from nltk.tokenize import sent_tokenize
import pyConTextNLP.display.html as html
from IPython.display import display, HTML
# %%
from pyConTextNLP.utils import get_document_markups

reports = [
    """IMPRESSION: Evaluation limited by lack of IV contrast; however, no evidence of
      bowel obstruction or mass identified within the abdomen or pelvis. Non-specific interstitial opacities and bronchiectasis seen at the right
     base, suggestive of post-inflammatory changes.""",
    """IMPRESSION: Evidence of early pulmonary vascular congestion and interstitial edema. Probable scarring at the medial aspect of the right lung base, with no
     definite consolidation."""
    ,
    """IMPRESSION:

     1.  2.0 cm cyst of the right renal lower pole.  Otherwise, normal appearance
     of the right kidney with patent vasculature and no sonographic evidence of
     renal artery stenosis.
     2.  Surgically absent left kidney.""",
    """IMPRESSION:  No pneumothorax.""",
    """IMPRESSION: No definite pneumothorax""",
    """IMPRESSION:  New opacity at the left lower lobe consistent with pneumonia."""
]

modifiers = itemData.get_items(
    "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml")
targets = itemData.get_items(
    "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/utah_crit.yml")

def markup_sentence(s, modifiers, targets, prune_inactive=True):
    """
    """
    markup = pyConText.ConTextMarkup()
    markup.setRawText(s)
    markup.cleanText()
    markup.markItems(modifiers, mode="modifier")
    markup.markItems(targets, mode="target")
    markup.pruneMarks()
    markup.dropMarks('Exclusion')
    # apply modifiers to any targets within the modifiers scope
    markup.applyModifiers()
    markup.pruneSelfModifyingRelationships()
    if prune_inactive:
        markup.dropInactiveModifiers()
    return markup

context = pyConText.ConTextDocument()

# %%
count = 0
rslts = []
for s in sent_tokenize(reports[0]):
    m = markup_sentence(s, modifiers=modifiers, targets=targets)
    rslts.append(m)

for r in rslts:
    context.addMarkup(r)

# %%
clrs = {
    "bowel_obstruction": "blue",
    "inflammation": "blue",
    "definite_negated_existence": "red",
    "probable_negated_existence": "indianred",
    "ambivalent_existence": "orange",
    "probable_existence": "forestgreen",
    "definite_existence": "green",
    "historical": "goldenrod",
    "indication": "pink",
    "acute": "golden"
}

# %%
display(HTML(html.mark_document_with_html(context,colors = clrs, default_color="black")))

# %%
mks=get_document_markups(context)
def get_node_brief(n,id_digits=3):
    return """%s %s(%s)"""%(n.getPhrase(),
                             n.getCategory(),
                             str(n.getSpan()))

def documentgraph_to_viewgraph(dg):
    newg = nx.DiGraph()
    G = nx.Graph()
    edges = dg.edges()
    for e in edges:
        newg.add_edge(get_node_brief(e[0]),
                      get_node_brief(e[1]))
        G.add_edge(get_node_brief(e[0]), get_node_brief(e[1]))
    return newg
# %%
dg=documentgraph_to_viewgraph(context.getDocumentGraph())

#%%
cg=context.getDocumentGraph().edges()
for e in cg:
    for ee in e:
        print(type(ee),ee.getSpan())

# %%
import matplotlib.pyplot as plt
G=nx.Graph()
for e in dg.edges:
    G.add_edge(e[0],e[1])
graph_pos=nx.kamada_kawai_layout(G)
nx.draw_networkx_nodes(G, graph_pos, node_size=1000, node_color='blue', alpha=0.3)
nx.draw_networkx_edges(G, graph_pos)
nx.draw_networkx_labels(G, graph_pos, font_size=12, font_family='sans-serif')

# show graph
plt.show()