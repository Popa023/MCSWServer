# MCSWServer

# Dependinte

flask, sqlalchemy, marshmallow, marshmallow_sqlalchemy, rdflib

# Descriere

Serverul foloseste trei endpoint-uri:
Primul este cel care descopera muzeele din orasul trimis ca parametru si le salveaza in baza de date: (/findMuseumsURIs/"city")
Cel de al doilea endpoint extrage abstractul tuturor muzeelor din baza de date: (/fetchMuseumsInformation)
Cel de al treilea endpoint este folosit pentru vizualizarea muzeelor din baza de date (/museums)

Totate endpoint-urile pot fi folosite ca si GET endpoint, pot fi folosite din browser.
  
Modelul de date:
  
 Museum: {
          "museumID" : int,
          "museumAbstract" : string,
          "museumGeo" : string
          }
  
  Geolocatia muzeului nu a fost implementata, iar limba folosita este limba engleza.
 
  Colectarea datelor este foarte lenta, aprox. 15 min pentru /findMuseumsURIs/"city" si aproximativ 30 min pentru /fetchMuseumsInformation in cazul colectarii informatiilor pentru muzeele din Bucuresti. Cauza poate fi folosirea unui parser ineficient de turtle de catre libraria rdflib.
