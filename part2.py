#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json

def csv_to_nested_dict(csv_file):
    """Read CSV and convert data into a 3-level nested dictionary: Semester -> Unit -> Module Name[cite: 29, 30]."""
    data = {"S1": {}, "S2": {}}
    
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            semester = row['semester'].strip()
            unit = row['unit'].strip()
            module_name = row['module_name'].strip()
            
            # Build module dictionary[cite: 30]
            module = {
                "module_title": row['module_title'].strip(),
                "coef": int(row['coef']),
                "credit": int(row['credit']),
                "percent_tp": float(row['percent_tp']),
                "percent_td": float(row['percent_td']),
                "percent_exam": float(row['percent_exam'])
            }
            
            # Initialize unit level if it doesn't exist[cite: 30]
            if unit not in data[semester]:
                data[semester][unit] = {}
                
            # Add module under the unit level (3-level nested dictionary)[cite: 30]
            data[semester][unit][module_name] = module
            
    return data

def modules_to_html(data):
    """Convert the nested dictionary structure into a formatted HTML page with tables[cite: 30, 31]."""
    html = ['<html><head><meta charset="utf-8"><title>M1 GSI Modules</title>',
            '<style>body{font-family:Arial,sans-serif;margin:20px;} table{width:100%;border-collapse:collapse;margin-bottom:20px;} th,td{border:1px solid #ddd;padding:8px;text-align:left;} th{background-color:#f2f2f2;}</style>',
            '</head><body>',
            '<h1>M1 GSI Course Canvas</h1>']
    
    for semester, units in data.items():
        html.append(f"<h2>{semester}</h2>")
        for unit, modules in units.items():
            html.append(f"<h3>Unit: {unit}</h3>")
            html.append("<table>")
            html.append("<tr><th>Module Code</th><th>Title</th><th>Coef</th><th>Credit</th><th>TP%</th><th>TD%</th><th>Exam%</th></tr>")
            
            for mod_name, info in modules.items():
                html.append("<tr>")
                html.append(f"<td>{mod_name}</td>")
                html.append(f"<td>{info['module_title']}</td>")
                html.append(f"<td>{info['coef']}</td>")
                html.append(f"<td>{info['credit']}</td>")
                html.append(f"<td>{info['percent_tp'] * 100:.0f}%</td>")
                html.append(f"<td>{info['percent_td'] * 100:.0f}%</td>")
                html.append(f"<td>{info['percent_exam'] * 100:.0f}%</td>")
                html.append("</tr>")
                
            html.append("</table>")
            html.append("<hr>")
            
    html.append("</body></html>")
    return "\n".join(html)

if __name__ == "__main__":
    filename = "modules.csv"
    
    # 1. Convert CSV to Nested Dictionary[cite: 30]
    result = csv_to_nested_dict(filename)
    
    # 2. Display result as JSON
    print("--- JSON Output ---")
    print(json.dumps(result, indent=4, ensure_ascii=False))
    
    # 3. Convert Data into HTML format and save[cite: 30, 31]
    html_content = modules_to_html(result)
    with open("modules.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("\n[Success] HTML file generated: modules.html")