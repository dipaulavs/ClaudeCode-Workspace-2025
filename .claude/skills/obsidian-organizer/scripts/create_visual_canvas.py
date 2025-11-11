#!/usr/bin/env python3
"""
Create visual Canvas explanation for YouTube video content.
Automatically generates interactive diagrams in Obsidian Canvas format.
"""

import json
import sys
import hashlib
from typing import List, Dict, Any


def generate_node_id(text: str, index: int) -> str:
    """Generate unique node ID from text and index."""
    return hashlib.md5(f"{text}{index}".encode()).hexdigest()[:12]


def create_canvas_nodes(
    title: str,
    summary: str,
    learnings: List[str],
    transcript_chunks: List[str] = None
) -> Dict[str, Any]:
    """
    Create Canvas JSON structure with visual layout.

    Args:
        title: Video title
        summary: Brief summary
        learnings: List of key learnings
        transcript_chunks: Optional transcript sections

    Returns:
        Canvas JSON structure
    """
    nodes = []
    edges = []

    # Title node (top center)
    title_node = {
        "id": "title",
        "type": "text",
        "text": f"# 🎬 {title}\n\n**Resumo Visual do Vídeo**",
        "x": -200,
        "y": -400,
        "width": 500,
        "height": 140,
        "color": "5"
    }
    nodes.append(title_node)

    # Summary node (below title)
    summary_node = {
        "id": "summary",
        "type": "text",
        "text": f"## 📝 RESUMO\n\n{summary}",
        "x": -200,
        "y": -200,
        "width": 500,
        "height": 200,
        "color": "3"
    }
    nodes.append(summary_node)
    edges.append({
        "id": "e-title-summary",
        "fromNode": "title",
        "fromSide": "bottom",
        "toNode": "summary",
        "toSide": "top",
        "color": "5"
    })

    # Learning nodes (grid layout)
    learning_colors = ["1", "2", "4", "6", "3", "5"]
    x_start = -600
    y_start = 100
    cols = 2
    node_width = 350
    node_height = 200
    x_gap = 100
    y_gap = 50

    for idx, learning in enumerate(learnings[:6]):  # Max 6 learnings
        col = idx % cols
        row = idx // cols

        x = x_start + col * (node_width + x_gap)
        y = y_start + row * (node_height + y_gap)
        color = learning_colors[idx % len(learning_colors)]

        node_id = f"learning-{idx}"
        node = {
            "id": node_id,
            "type": "text",
            "text": f"## 💡 Aprendizado {idx + 1}\n\n{learning}",
            "x": x,
            "y": y,
            "width": node_width,
            "height": node_height,
            "color": color
        }
        nodes.append(node)

        # Connect to summary
        edges.append({
            "id": f"e-summary-learning-{idx}",
            "fromNode": "summary",
            "fromSide": "bottom",
            "toNode": node_id,
            "toSide": "top",
            "color": color
        })

    # Add transcript chunks if available
    if transcript_chunks and len(transcript_chunks) > 0:
        transcript_y = y_start + ((len(learnings) // cols) + 1) * (node_height + y_gap)

        for idx, chunk in enumerate(transcript_chunks[:3]):  # Max 3 chunks
            chunk_id = f"transcript-{idx}"
            chunk_node = {
                "id": chunk_id,
                "type": "text",
                "text": f"## 📄 Parte {idx + 1}\n\n{chunk[:300]}...",
                "x": x_start + idx * (node_width + x_gap),
                "y": transcript_y,
                "width": node_width,
                "height": 250,
                "color": "2"
            }
            nodes.append(chunk_node)

    return {
        "nodes": nodes,
        "edges": edges
    }


def save_canvas(canvas_data: Dict[str, Any], output_path: str) -> None:
    """Save Canvas JSON to file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(canvas_data, f, indent='\t', ensure_ascii=False)


def main():
    """CLI interface for Canvas generation."""
    if len(sys.argv) < 4:
        print("Usage: create_visual_canvas.py <title> <summary> <learning1,learning2,...> [output_path]")
        sys.exit(1)

    title = sys.argv[1]
    summary = sys.argv[2]
    learnings = sys.argv[3].split('|||')  # Use ||| as separator
    output_path = sys.argv[4] if len(sys.argv) > 4 else "visual-canvas.canvas"

    canvas_data = create_canvas_nodes(title, summary, learnings)
    save_canvas(canvas_data, output_path)

    print(f"✅ Canvas criado: {output_path}")


if __name__ == "__main__":
    main()
