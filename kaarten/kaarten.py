rws = [l.strip() for l in open("rws.txt")]
tarot = [l.strip() for l in open("tarot.txt")]  # decks from tarot.com
hersteld = [l.strip() for l in open("hersteld.txt")]
shadow = [l.strip() for l in open("shadow.txt")]
marseille = [l.strip() for l in open("marseille.txt")]

print(
    """
<style>
@media print {
    table {page-break-inside: avoid;}
}
</style>
"""
)

for c in range(78):
    if (c % 5) == 0:
        if c > 0:
            print("</table>")
        print(
            """
<table>
<tr>
<th>Marseille</th>
<th>Rider-Waite</th>
<th>Hersteld</th>
<th>Morgan-Greer</th>
<th>Connolly</th>
<th>Crystal Vision</th>
<th>Shadowscapes</th>
</tr>
"""
        )
    print(
        """<tr>
        <td><img width=180 src="marseille/%s"></td>
        <td><img width=220 src="rws/%s"></td>
        <td><img width=210 src="hersteld/%s"></td>
        <td><img style="margin-bottom: 10" src="mg/%s"></td>
        <td><img width=220 src="connolly/%s"></td>
        <td><img width=210 src="crystal/%s"></td>
        <td><img width=210 src="shadow/%s"></td>
    </tr>
    """
        % (marseille[c], rws[c], hersteld[c], tarot[c], tarot[c], tarot[c], shadow[c])
    )
print("</table>")