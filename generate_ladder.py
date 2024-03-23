import files
import classes
from pathlib import Path
import os

# {class name => [[name, lvl], [name, lvl], ...]}
ladders = {}
data_dir = Path(__file__).parent.joinpath('test/char/')
for file_path in data_dir.iterdir():
	# print(file_path)
	try:
		d2sfile = files.D2SFile(file_path)
	except:
		pass
	print([d2sfile.char_name, d2sfile.char_level, classes.CLASS_NAMES[d2sfile.char_class_id]])
	class_name = classes.CLASS_NAMES[d2sfile.char_class_id]
	if class_name not in ladders:
		ladders[class_name] = []
	if d2sfile.last_played > 1694390400 and d2sfile.is_ladder:
		ladders[class_name].append([d2sfile.char_name, d2sfile.char_level])
	#print(d2sfile.to_dict())

rtn = """    <div class="container">\n"""
for class_name in ladders:
	rtn += """
        <h1>%s</h1>
        <div class="stats">""" % class_name
	chars = sorted(ladders[class_name], key=lambda x: x[1], reverse=True)
	for i in range(0, min(10, len(chars))):
		char_name = chars[i][0]
		lvl = chars[i][1]
		rtn += """
            <div class="stat">
            <div class="stat-label"><a href="/api/char/%s">%s</a></div>
                <div class="stat-value">%d</div>
            </div>""" % (char_name, char_name, lvl)
	rtn += """
        </div>"""
rtn += """
    </div>\n"""

print(rtn)
