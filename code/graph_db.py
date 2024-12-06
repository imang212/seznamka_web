from py2neo import Graph, Node, Relationship
import base64

graph = Graph("neo4j://neo4j2:7687", auth=("neo4j", "adminpass"))
def Vrat_pocet_profilu():
    result = graph.run(f"""MATCH (n) RETURN count(n) AS profile_count""").data()
    id = result[0]['profile_count'] if result else 0
    return id
def Vytvor_profil_Node(node_id,jmeno,vek,orientace,konicky,popis):
    profil = Node("Osoba", node_id=node_id, name=jmeno, age=vek, orintace=orientace, hobbies=konicky, popis_profilu=popis)
    graph.create(profil)
def Add_profile_neo(node_id,jmeno,prijmeni,pohlavi,email,heslo,vek,orientace,konicky,popis):
    query = f"""
    MERGE (o:Osoba {{node_id: $node_id}}) 
    SET o.name = $name,
        o.surname = $surname,
        o.pohlavi = $pohlavi,
        o.email = $email,
        o.heslo = $heslo,
        o.age = $age,
        o.orientace = $orientace,
        o.hobbies = $hobbies,
        o.popis_profilu = $popis_profilu
    RETURN o
    """    
    result = graph.run(query, node_id=node_id, name=jmeno,surname=prijmeni,pohlavi=pohlavi,email=email,heslo=heslo,age=vek,orientace=orientace,hobbies=konicky,popis_profilu=popis)
    return result
def Kontrola_existence_profilu(email):
    query = f"""
    MATCH (o:Osoba {{email: $email}})
    RETURN COUNT(o) > 0 AS profileExists
    """    
    result = graph.run(query, email=email).evaluate()
    return result
def Vrat_uzivatele_podle_id(email):
    query = f"""
    MATCH (o:Osoba {{email: $email}})
    RETURN o
    """
    result = graph.run(query, email=email).data()
    if not result:
        return None
    if result: return result[0]['o'] 
    return None
def Vrat_prihlasovaci_udaje(email):
    query = """
    MATCH (o:Osoba {email: $email})
    RETURN o
    """
    result = graph.run(query, email=email).data()
    if result: return result[0]['o']
    return None        
def Vymaz_vsechny_prfily():
    query = f"""
    MATCH (n)
    DETACH DELETE n
    """    
    result = graph.run(query)
    return result
def Vymaz_profil(id_uziv):
    query = f"""
    MATCH (n:Person {{node_id: $id_uziv}})
    DELETE n
    """    
    result = graph.run(query)
    return result
def Pridej_obrazek(node_id,image_path):
    with open(image_path, "rb") as image_file: image = base64.b64encode(image_file.read()).decode('utf-8')
    query = f"""
    MATCH (n {{nodeid: $node_id}})
    SET n.picture = $encoded_picture
    RETURN n
    """
    result = graph.run(query, node_id=node_id, encoded_picture=image).data()
    return result
def Pridej_cislo(node_id,tel_cislo):
    query = f"""
    MATCH (n {{nodeid: $node_id}})
    SET n.telefoni_cislo = $telefoni_cislo
    RETURN n
    """
    result = graph.run(query, node_id=node_id, encoded_picture=tel_cislo).data()
    return result
def Pridej_popis(node_id, popis):
    query = f"""
    MATCH (n {{nodeid: $node_id}})
    SET n.popis_profilu = $popis_
    RETURN n
    """
    result = graph.run(query, node_id=node_id, popis_=popis).data()
    return result