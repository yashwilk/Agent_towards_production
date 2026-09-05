"""
hushvert file-conversion demo (server lane): discovers the hosted API's supported
format pairs, generates a sample office document, and converts it to LLM-ready
markdown through the submit/upload/poll/download REST flow.

Local lane (images, HEIC, audio, archives, PDF page ops, data files) runs as
WebAssembly in the browser instead - see local-lane/example.ts. Agent hosts
(Claude Code, Cursor, etc.) can skip this script entirely and use the MCP
server config in mcp/hushvert.mcp.json.
"""

import client
import config
import sample_document


def main():
    pairs = client.list_formats()
    md_inputs = sorted(p["from"] for p in pairs if p["to"] == "md")
    print(f"{len(pairs)} server pairs available")
    print("Convertible to LLM-ready markdown:", ", ".join(md_inputs))

    sample_document.write_sample_docx()

    markdown = client.convert_file(config.SAMPLE_DOCX_PATH, to="md").decode("utf-8")
    print(markdown)


if __name__ == "__main__":
    main()