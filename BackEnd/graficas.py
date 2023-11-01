
import graphviz
import re

def rep_MBR(table_content):
    s = graphviz.Digraph('MBR', filename=r'BackEnd\static\reportes_pdf\MBR.pdf',
                     node_attr={'shape': 'plaintext'})

    # print(table_content)
    table_content = table_content.replace("►","")
    
    try:
        s.node('struct1', table_content)
        # s.view()
        s.render()
    except Exception as e:
        print(e)
    
    # print(s)


def rep_FDISK(total, part1, part2, part3, part4):
    s = graphviz.Digraph('DISK', filename=r'BackEnd\static\reportes_pdf\DISK.pdf',
                     node_attr={'shape': 'plaintext'})
    if part4 > total:
        part4 = 0

    espacio_libre = total-part1-part2-part3-part4
    porcentaje = espacio_libre/total
    table_content = f"""<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"> 
        <tr>
            <td>MBR</td>
            <td>ESPACIO LIBRE \n {espacio_libre}M {porcentaje}%</td>
            <td>PARTICION 1 \n {part1}</td>
            <td>PARTICION 2 \n {part2}</td>
            <td>PARTICION 3 \n {part3}</td>
            <td>PARTICION 4 \n {part4}</td>
        </tr>
</TABLE>>"""

    s.node('struct2', table_content)
    # s.view()
    s.render()


def rep_SB(dot): 
    s = graphviz.Digraph('SB', filename=r'BackEnd\static\reportes_pdf\SB.pdf',
                     node_attr={'shape': 'plaintext'})

    # print(table_content)

    s.node('struct3', dot)
    # s.view() 
    s.render()


def rep_INODES(dot):
    s = graphviz.Digraph('INODES', filename=r'BackEnd\static\reportes_pdf\INODES.pdf',
                     node_attr={'shape': 'plaintext'})

    # print(table_content)

    s.node('struct4', dot)
    # s.view() 
    s.render()



def rep_BLOQUES(dot):
    s = graphviz.Digraph('BLOCKS', filename=r'BackEnd\static\reportes_pdf\BLOCKS.pdf',
                     node_attr={'shape': 'plaintext'})

    # print(table_content)

    s.node('struct5', dot)
    # s.view() 
    s.render()


def rep_BM_INODES_1(dot):
    s = graphviz.Digraph('BM_INODES', filename=r'BackEnd\static\reportes_pdf\BM_INODES.pdf',
                     node_attr={'shape': 'record'})

    # print(table_content)

    s.node('struct5', dot)
    # s.view() 
    s.render()



def rep_Journaling():
    s = graphviz.Digraph('JS', filename=r'BackEnd\static\reportes_pdf\Journaling.pdf',
                     node_attr={'shape': 'plaintext'})

    # print(table_content)
    table_content = f"""<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"> 
        <tr>
            <td>JOURNALING</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
</TABLE>>"""

    s.node('struct6', table_content)
    # s.view() 
    s.render()


def rep_LS():
    s = graphviz.Digraph('LS', filename=r'BackEnd\static\reportes_pdf\LS.pdf',
                     node_attr={'shape': 'plaintext'})

    # print(table_content)
    table_content = f"""<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"> 
        <tr>
        <td>PERMISOS</td>
        <td>OWNER</td>
        <td>GRUPO</td>
        <td>SIZE</td>
        <td>FECHA</td>
        <td>HORA/td>
        <td>TIPO</td>
        <td>NAME/td>
    </tr>
    <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
</TABLE>>"""

    s.node('struct6', table_content)
    # s.view() 
    s.render()


def rep_Tree():
    s = graphviz.Digraph('TREE', filename=r'BackEnd\static\reportes_pdf\TREE.pdf',
                     node_attr={'shape': 'plaintext'})

    # print(table_content)
    table_content = f"""<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"> 
        <tr>
            <td>TREE</td>
        </tr>
</TABLE>>"""

    s.node("struck1", "TABLA INODO /.")

    s.node('struct6', table_content)
    # s.view() 
    s.render()



def rep_file():
    s = graphviz.Digraph('FILE', filename=r'BackEnd\static\reportes_pdf\Rep_FILE.pdf',
                     node_attr={'shape': 'plaintext'})
    
    dpt = ""
    with open(r"BackEnd\static\reportes_pdf\file.txt", "r") as file:
        dot = file.read()
        print(dot)

    s.node('struct7', dot)
    # s.view()
    s.render()
    # print("REPORTE DE FILE LISTOOOOOOOOOO")



# rep_file()