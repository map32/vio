
def addressLabels(vios):
    header = '''<html lang="en">
<head>
    <meta charset="utf-8">
    <title>HTML & CSS Avery Labels (5160) by MM at Boulder Information Services</title>
    <link href="labels.css" rel="stylesheet" type="text/css" >
    <style>
    body {
        width: 8.5in;
        margin: 0.5in .1875in;
        }
    .label{
        /* Avery 5160 labels -- CSS and HTML by MM at Boulder Information Services */
        width: 2.425in; /* plus .6 inches from padding */
        height: .875in; /* plus .125 inches from padding */
        padding: .125in .1in 0;
        margin-right: .125in; /* the gutter */

        float: left;

        text-align: center;
        overflow: hidden;

        outline: 1px dotted; /* outline doesn't occupy space like border does */
        }
    .page-break  {
        clear: left;
        display:block;
        page-break-after:always;
        }
    </style>

</head>
<body>'''
    footer='''
<div class="page-break"></div>

</body>
</html>
'''
    i = 0
    while i < len(vios):
        mid = ''
        for v in vios[i:i+30]:
            mid += '<div class="label">'+v['name']+'<br>'+v['address']+'</div>'
        with open('labels'+str(i/30+1),'w+') as f:
            f.write(header+mid+footer)
        i += 30
    

def violationPdfs(vios):
    names = []
    for v in vios:
        with open('violations.html','a+') as f:
            f.write(v['data'])
            f.write('<p style="page-break-after: always"></p>\n<p style="page-break-before: always></p>"')
