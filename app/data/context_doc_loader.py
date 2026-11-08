import pathlib

def load_context_doc():
    try:
        return pathlib.Path("app/data/context_doc.md").read_text(encoding="utf-8")
    except:
        return ""

CONTEXT_DOC = load_context_doc()

CONTEXT_DOC_BRIEF = CONTEXT_DOC[:3000]
