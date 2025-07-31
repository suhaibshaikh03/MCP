from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", stateless_http=True)

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


# TODO: Write a tool to read a doc
@mcp.tool(name="read_doc",description="Tool for reading a document")
async def read_doc(doc_id: str) -> str:
    return docs.get(doc_id, "Document not found")

# TODO: Write a tool to edit a doc
@mcp.tool()
def edit_doc(doc_id: str, content: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found.")
    docs[doc_id] = docs[doc_id].replace(content, "")
    return f"Document {doc_id} updated successfully."

# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc

@mcp.resource("docs://documents",
mime_type="application/json"
)
def list_docs():
    """List all available documents"""
    return list(docs.keys())

@mcp.resource("docs://document/{doc_id}",
mime_type="application/json"
)
def read_doc(doc_id: str):
    """Read a document by ID"""
    return docs.get(doc_id, "Document not found")


mcp_app = mcp.streamable_http_app()