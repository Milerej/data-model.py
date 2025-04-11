# At the beginning of your code, add this CSS style to format the tooltips
custom_css = """
<style>
.vis-tooltip {
    position: absolute;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 10px;
    font-family: Arial;
    font-size: 14px;
    z-index: 1000;
    max-width: 500px;
    white-space: normal;
}
.vis-tooltip table {
    border-collapse: collapse;
    width: 100%;
    margin-top: 5px;
}
.vis-tooltip th, .vis-tooltip td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}
.vis-tooltip th {
    background-color: #f2f2f2;
}
</style>
"""

# After creating the HTML content, modify how it's inserted:
net.save_graph("graph.html")
with open("graph.html", "r", encoding='utf-8') as f:
    html_content = f.read()
    # Insert custom CSS and JavaScript
    html_content = html_content.replace('</head>', f'{custom_css}</head>')
    html_content = html_content.replace('</body>', f'{highlight_js}</body>')
    # Fix HTML escaping in node titles
    html_content = html_content.replace('&lt;', '<').replace('&gt;', '>')
components.html(html_content, height=750, scrolling=True)
