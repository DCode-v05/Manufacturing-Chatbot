import pathlib

def load_context_doc():
    try:
        return pathlib.Path("app/data/context_doc.md").read_text(encoding="utf-8")
    except:
        return ""

# Export the context so other modules can import directly
CONTEXT_DOC = load_context_doc()

# Optional shorter version (trimmed for batch prompts)
CONTEXT_DOC_BRIEF = CONTEXT_DOC[:3000]  # keeps tokens low
