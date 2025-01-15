from posixpath import basename
import os
import re
from bs4 import BeautifulSoup
from get_data import get_data

exceptions = ["259070", "259085", "271575", "266138"]

linkdict = {
    "271577": "/tipitaka/2V/1",
    "271576": "/tipitaka/1V/1",
    "262626": "/tipitaka/36P1/3/3.7/3.7.4/Nahetuduka/Catuvisaka_sakamma",
    "265995": "/tipitaka/39P3/3/3.1/3.1.1/3.1.1.1--7/Paccayacatukka/Hetu",
    "262625": "/tipitaka/36P1/3/3.7/3.7.4/Nahetuduka/Catuvisaka_saupanissaya",
    "260803": "/tipitaka/37P1/12/12.7/12.7.4/12.7.4",
    "265990": "/tipitaka/39P3/2/2.6/2.6.1/2.6.1.1--7/Paccayacatukka/Hetu",
    "262557": "/tipitaka/36P1/2/2.7/2.7.4/Navippayuttaduka/Bavisaka",
    "260787": "/tipitaka/37P1/12/12.1/12.1.2/12.1.2",
    "260786": "/tipitaka/37P1/12/12.1/12.1.2/2.1.2.1",
    "262350": "/tipitaka/36P1/2/2.5/2.5.3/Vippayuttaduka/evisaka_savipaka",
    "262556": "/tipitaka/36P1/2/2.7/2.7.4/Navippayuttaduka/attarasaka_saindriya",
    "262554": "/tipitaka/36P1/2/2.7/2.7.4/Navippayuttaduka/attarasaka _sahara",
    "262555": "/tipitaka/36P1/2/2.7/2.7.4/Navippayuttaduka/avisaka_sahara",
    "262268": "/tipitaka/36P1/2/2.3/2.3.3/Vippayuttaduka/uddasaka_savipaka",
    "262526": "/tipitaka/36P1/2/2.7/2.7.4/Nahetuduka/avisaka_saindriya",
    "262334": "/tipitaka/36P1/2/2.5/2.5.3/Hetuduka/evisaka_savipaka",
    "262269": "/tipitaka/36P1/2/2.3/2.3.3/Vippayuttaduka/evisaka_savipaka",
    "264430": "/tipitaka/36P1/2/2.3/2.3.1/2.3.1.2/Hetuduka/erasaka_savipaka",
    "262525": "/tipitaka/36P1/2/2.7/2.7.4/Nahetuduka/oḷasaka_saindriya",
    "262524": "/tipitaka/36P1/2/2.7/2.7.4/Nahetuduka/avisaka_sahara",
    "264431": "/tipitaka/36P1/2/2.3/2.3.1/2.3.1.2/Hetuduka/avisaka_savipaka",
    "264409": "/tipitaka/36P1/2/2.1/2.1.1/2.1.1.2/Ganana_hetumulaka_avisaka",
    "262332": "/tipitaka/36P1/2/2.5/2.5.3/Hetuduka/evisaka_sasevana",
    "264555": "/tipitaka/36P1/2/2.7/2.7.2/2.7.2.1/Nahetuduka/attarasaka_sahara",
    "262130": "/tipitaka/36P1/2/2.1/2.1.3/Hetuduka/evisaka_sasevana",
    "262131": "/tipitaka/36P1/2/2.1/2.1.3/Hetuduka/erasaka_savipaka",
    "262333": "/tipitaka/36P1/2/2.5/2.5.3/Hetuduka/erasaka_savipaka",
    "262247": "/tipitaka/36P1/2/2.3/2.3.3/Hetuduka/vadasaka_sasevana",
    "262523": "/tipitaka/36P1/2/2.7/2.7.4/Nahetuduka/olasaka_sahara",
    "262331": "/tipitaka/36P1/2/2.5/2.5.3/Hetuduka/vadasaka_sasevana",
    "264556": "/tipitaka/36P1/2/2.7/2.7.2/2.7.2.1/Nahetuduka/kavīsaka_sahara",
    "264557": "/tipitaka/36P1/2/2.7/2.7.2/2.7.2.1/Nahetuduka/oḷasaka_saindriya",
    "262132": "/tipitaka/36P1/2/2.1/2.1.3/Hetuduka/evisaka_savipaka",
    "262250": "/tipitaka/36P1/2/2.3/2.3.3/Hetuduka/evisaka_savipaka",
    "264190": "/tipitaka/39P3/3/3.1/3.1.2/3.1.2.1--7/accayacatukka",
    "262249": "/tipitaka/36P1/2/2.3/2.3.3/Hetuduka/erasaka_savipaka",
    "266013": "/tipitaka/39P3/3/3.6/3.6.3/3.6.3.1--7/Paccayacatukka/etu",
    "264604": "/tipitaka/36P1/2/2.7/2.7.2/2.7.2.1/Noatthiduka/evisaka_saupanissaya",
    "264201": "/tipitaka/39P3/3/3.6/3.6.1/3.6.1.1--7/accayacatukka",
    "264605": "/tipitaka/36P1/2/2.7/2.7.2/2.7.2.1/Noatthiduka/evisaka_sakamma",
    "262248": "/tipitaka/36P1/2/2.3/2.3.3/Hetuduka/evisaka_sasevana",
    "264188": "/tipitaka/39P3/3/3.1/3.1.1/3.1.1.1--7/accayacatukka",
    "262129": "/tipitaka/36P1/2/2.1/2.1.3/Hetuduka/vadasaka_sasevana",
    "264558": "/tipitaka/36P1/2/2.7/2.7.2/2.7.2.1/Nahetuduka/kavisaka_saindriya",
    "257743": "/tipitaka/40P16/8",
    "264428": "/tipitaka/36P1/2/2.3/2.3.1/2.3.1.2/Hetuduka/vadasaka_sasevana",
    "262267": "/tipitaka/36P1/2/2.3/2.3.3/Vippayuttaduka/evisaka_sasevana)",
    "264206": "/tipitaka/39P3/3/3.7/3.7.1/3.7.1.1--7/accayacatukka",
    "262266": "/tipitaka/36P1/2/2.3/2.3.3/Vippayuttaduka/erasaka_sasevana",
    "266014": "/tipitaka/39P3/3/3.7/3.7.1/3.7.1.1--7/Paccayacatukka/etu",
    "264429": "/tipitaka/36P1/2/2.3/2.3.1/2.3.1.2/Hetuduka/avisaka_sasevana",
    "264205": "/tipitaka/39P3/3/3.6/3.6.3/3.6.3.1--7/accayacatukka",
    "264199": "/tipitaka/39P3/3/3.5/3.5.2/3.5.2.1--7/accayacatukka",
    "262160": "/tipitaka/36P1/2/2.1/2.1.3/Vippayuttaduka/evisaka_sasevana",
    "262161": "/tipitaka/36P1/2/2.1/2.1.3/Vippayuttaduka/uddasaka_savipaka",
    "262349": "/tipitaka/36P1/2/2.5/2.5.3/Vippayuttaduka/evisaka_sasevana",
    "262162": "/tipitaka/36P1/2/2.1/2.1.3/Vippayuttaduka/evisaka_savipaka",
    "262628": "/tipitaka/36P1/3/3.7/3.7.4/Noavigataduka/atuvisaka_saupanissaya",
    "262629": "/tipitaka/36P1/3/3.7/3.7.4/Noavigataduka/atuvisaka_sakamma",
    "262561": "/tipitaka/36P1/2/2.7/2.7.4/Noatthiduka/atuvisaka_sakamma",
    "262560": "/tipitaka/36P1/2/2.7/2.7.4/Noatthiduka/atuvisaka_saupanissaya",
}
namedict = {
    "271577": "2V Pācittiyapāḷi",
    "271576": "1V Pārājikapāḷi",
    "262626": "Catuvīsaka (sakamma)",
    "265995": "Hetu",
    "262625": "Catuvīsaka (saupanissaya)",
    "260803": "12.7.4 Paccayapaccanīyānuloma",
    "265990": "Hetu",
    "262557": "Bāvīsaka (saindriya)",
    "260787": "12.1.2 Paccayapaccanīya",
    "260786": "12.1.2.1 Vibhaṅgavāra",
    "262350": "Tevīsaka (savipāka)",
    "262556": "Sattarasaka (saindriya)",
    "262554": "Sattarasaka (sāhāra)",
    "262555": "Bāvīsaka (sāhāra)",
    "262268": "Cuddasaka (savipāka)",
    "262526": "Bāvīsaka (saindriya)",
    "262334": "Tevīsaka (savipāka)",
    "262269": "Tevīsaka (savipāka)",
    "264430": "Terasaka (savipāka)",
    "262525": "Soḷasaka (saindriya)",
    "262524": "Bāvīsaka (sāhāra)",
    "264431": "Bāvīsaka (savipāka)",
    "264409": "Bāvīsaka",
    "262332": "Tevīsaka (sāsevana)",
    "264555": "Sattarasaka (sāhāra)",
    "262130": "Tevīsaka (sāsevana)",
    "262131": "Terasaka (savipāka)",
    "262333": "Terasaka (savipāka)",
    "262247": "Dvādasaka (sāsevana)",
    "262523": "Soḷasaka (sāhāra)",
    "262331": "Dvādasaka (sāsevana)",
    "264556": "Ekavīsaka (sāhāra)",
    "264557": "Soḷasaka (saindriya)",
    "262132": "Tevīsaka (savipāka)",
    "262250": "Tevīsaka (savipāka)",
    "264190": "Paccayacatukka",
    "262249": "Terasaka (savipāka)",
    "266013": "Hetu",
    "264604": "Tevīsaka (saupanissaya)",
    "264201": "Paccayacatukka",
    "264605": "Tevīsaka (sakamma)",
    "262248": "Tevīsaka (sāsevana)",
    "264188": "Paccayacatukka",
    "262129": "Dvādasaka (sāsevana)",
    "264558": "Ekavīsaka (saindriya)",
    "257743": "38 Hīnattika, Hetuduka",
    "264428": "Dvādasaka (sāsevana)",
    "262267": "Tevīsaka (sāsevana)",
    "264206": "Paccayacatukka",
    "262266": "Terasaka (sāsevana)",
    "266014": "Hetu",
    "264429": "Bāvīsaka (sāsevana)",
    "264205": "Paccayacatukka",
    "264199": "Paccayacatukka",
    "262160": "Tevīsaka (sāsevana)",
    "262161": "Cuddasaka (savipāka)",
    "262349": "Tevīsaka (sāsevana)",
    "262162": "Tevīsaka (savipāka)",
    "262628": "Catuvīsaka (saupanissaya)",
    "262629": "Catuvīsaka (sakamma)",
    "262561": "Catuvīsaka (sakamma)",
    "262560": "Catuvīsaka (saupanissaya)",
}

newlinkdict = {}
newnamedict = {}
pathdict = {}

if __name__ == "__main__":
    xml_dir = "World-Tipitaka/tipitaka"
    dst_dir = "wt-html"
    for subdir, _, files in os.walk(xml_dir):
        for file in files:
            if file.endswith(".xml"):
                link = basename(file).split(".")[0]

                if link in exceptions:
                    continue
            
                xml_path = os.path.join(subdir, file)
                data = get_data(xml_path)

                # links = re.findall(r'<a\shref="javascript:void\(0\)"\s+onclick="([^"]+)"\sid="([^"]+)"\sname="([^"]+)"\stitle="([^"]+)">(?:<< )?([^<>]+)(?:>>)?</a>', data)
                links = re.findall(
                    r'<li\sname="([^"]+)">\s*<a\shref="javascript:void\(0\)"\sonclick="outD\(([^\)]+)\)">([^<]+)</a>\s*</li>',
                    data,
                )

                for link in links:
                    path = link[0]

                    if path.startswith("data/"):
                        path = path[5:]

                    # Make sure links are consistent
                    if link[1] in linkdict:
                        if path != linkdict[link[1]]:
                            print(f"link {link[1]}: {path} != {linkdict[link[1]]}")
                    linkdict.update({link[1]: path})
                    namedict.update({link[1]: link[2].strip()})
                    if path in pathdict:
                        if link[1] != pathdict[path]:
                            print(f"path {path}: {link[1]} != {pathdict[path]}")
                    pathdict.update({path: link[1]})


    for subdir, _, files in os.walk(os.path.join(xml_dir, "data")):
        for file in files:
            if file.endswith(".xml"):
                link = basename(file).split(".")[0]

                if link in exceptions:
                    continue

                if link not in linkdict:
                    # print(f"link {link} not found")
                    xml_path = os.path.join(subdir, file)
                    data = get_data(xml_path)
                    path = re.findall(
                        r'<a\shref="([^"]+)">([^<]+)</a></div><div\sclass="i">([^<]+)</div>',
                        data,
                    )[0]
                    id = re.findall(r'<div\sclass="q"\sid="([^"]+)">', data)
                    name = re.findall(r'<div\sclass="i">([^<]+)</div>', data)[0]
                    if path[1] == "Home":
                        newpath = re.sub(r'p_([^_]+)_1', r'/tipitaka/\1/0', id[0])
                        # newpath = id[0].replace("p_", "/tipitaka/").replace("_", "/")
                        # Make sure path not already used
                        if newpath in pathdict:
                            if link != pathdict[newpath]:
                                print(f"path {newpath}: {link} != {pathdict[newpath]}")
                        linkdict.update({link: newpath})
                        namedict.update({link: name})
                    else:
                        if name[0] == " ":
                            name = name[1:]
                        newlinkdict.update({link: path[0] + "/" + name[1:]})
                        newnamedict.update({link: name})
    
    if len(newlinkdict) > 0:
        print("linkdict = {")
        for link in newlinkdict:
            print(f'    "{link}": "{newlinkdict[link]}",')
        print("}")

    if len(newnamedict) > 0:
        print("namedict = {")
        for link in newnamedict:
            print(f'    "{link}": "{newnamedict[link]}",')
        print("}")

    print("Writing links.py")
    with open("links.py", "w") as f:
        f.write("exceptions = [ \n")
        for e in exceptions:    
            f.write(f'    "{e}",\n')
        f.write("]\n\n")
        
        f.write("linkdict = {\n")
        for link in linkdict:
            f.write(f'    "{link}": "{linkdict[link]}",\n')
        f.write("}\n\n")

        f.write("namedict = {\n")
        for link in namedict:
            f.write(f'    "{link}": "{namedict[link]}",\n')
        f.write("}\n")