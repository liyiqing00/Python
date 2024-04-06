import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

filepath="tour.csv"
posts=[]

try:
    with open(filepath, "r", encoding="utf-8")as file:
        for line in file:
            post=line.rstrip('\n')
            post=post.split(',')
            if post[3] not in posts:
                posts.append(post[3])
except IOError:
    pass
else:
    file.close()

contents="<fieldset>"
contents+="<legend align='center'><font size='4'>どんな観光資源を探してますか(選択)</font></legend>"
contents+="<div style='display:flex;flex-wrap:wrap'>"
for i in posts:
    contents+=f"<div style=' width:calc(100%/3)'><p><input type='checkbox' name='genre' value='{i}'>{i}</p></div>"
contents+="</div>"
contents+="</fieldset>"


template="""
<html>
<head>
    <meta charset="utf-8">
    <title>観光資源を探そう</title>
</head>
<body>
    <form method="POST" action="find.py">
    <fieldset>
    <legend align="center"><font size="4">旅行先を入れてください(必須)</font></legend>
    <p align="center"> 所在地:<input type="text" name="city">(都市)</p>
    <p align="center"> 例：東京</p>
    <p align="center"><input type="submit" value="検索"></p>
    </fieldset>
    {contents}   
</body>
</html>
"""

result=template.format(contents=contents)
print("Content-type: text/html\n")
print(result)
