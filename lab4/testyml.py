# %%
from visual import Vis, view_pycontext_output
import pyConTextNLP.pyConText as pyConText
import itemData
modifiers=itemData.get_items('https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/pneumonia_modifiers.yml')
targets = itemData.get_items("https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/pneumonia_targets.yml")
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

def markup_doc(doc_text:str):
    context = pyConText.ConTextDocument()
    rslts = []
    for s in doc_text.split('\.'):
        m = markup_sentence(s, modifiers=modifiers, targets=targets)
        rslts.append(m)

    for r in rslts:
        context.addMarkup(r)
    return context


# %%
context=markup_doc('the patient has no pneumonia on x-ray.')
dg=context.getDocumentGraph()

# %%
view_pycontext_output(context)