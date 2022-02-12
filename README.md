# FemQO
Flashcards per l'estudi i memorització de Química Orgànica
 
## 1.	Introducció
FemQO és un programa d’ordinador escrit en el llenguatge Python, dissenyat amb l’objectiu d’ajudar en l’estudi i memorització de les reaccions treballades en Química Orgànica I, II i III. El programa mostra unes targetes (flashcards) que tenen, per una cara, els reactius de la reacció, demanant pel producte que es forma; i per l’altra el reactiu i producte, preguntant per les condicions de la reacció. El programa no està pensat per l’avaluació, sinó per l’auto-avaluació i aprenentatge personal de cada usuari.
 
El programa permet decidir quin grup de reaccions estudiar: si focalitzar-se solament en una assignatura concreta (QOI, QOII o QOIII) o si estudiar simultàniament més d’una assignatura. 

Per això, l’aplicació pot ser utilitzada com una eina didàctica pels estudiants de qualsevol de les tres assignatures, fent més amè l’estudi i memorització de les reaccions que s’hi ensenyen; així com també servir com una eina de repàs de les assignatures anteriors (QOI o QOII) abans de començar les seves successores (QOII o QOIII).

FemQO només funciona en Windows, i pot ser utilitzat tant amb el ratolí o una pantalla tàctil, com únicament amb el teclat. 

La secció 2 explica com obrir el programa per Windows, i la secció 3 explica en detall el seu funcionament, incloent els modes d’estudi inclosos (3.1); com canviar l’assignatura a estudiar (3.2); el procés a seguir si es vol modificar el contingut de, afegir o eliminar alguna targeta (3.3); com fer un reset de l’aplicació abans de distribuir-lo a altres persones (3.4) i sobre el llenguatge de programació utilitzat (3.5).

## 2.	Com obrir el programa
Seguidament es mostren instruccions sobre com obrir el programa amb Windows.
Un cop descarregada i descomprimida la carpeta de WeTransfer, entra dins la carpeta FemQO.2.1 i obre el programa "FemQO.2.1.exe". En obrir-lo, Microsoft Defender t'avisarà que córrer l’app pot posar el PC en perill. Hauràs de clicar a "més informació", i a "córrer igualment". 

Depèn de com tinguis configurat el teu ordinador, és possible que et surti una pantalla indicant que "L'aplicació que intentes instal·lar no és una aplicació comprovada per Microsoft". En aquest cas, hauràs d'anar a "canviar la configuració de les meves recomanacions d'aplicacions", i canviar la configuració a "De qualsevol lloc" o a "De qualsevol lloc, però avisa'm abans d'instal·lar una aplicació que no està a Microsoft Store" (recomano la segona opció, per tenir un avís en instal·lar futures apps).

Amb això, ja podràs utilitzar el programa!

Com és ben sabut, Windows bloqueja tots els programes que no coneix. No he tingut temps de demanar a Windows que assegurés la seguretat del meu programa, però asseguro que el programa no és capaç de fer res maliciós al teu ordinador. Només és capaç de modificar certs elements dins la pròpia carpeta "FemQO". 

## 3.	Sobre el programa
El programa, escrit en el llenguatge Python, conté totes les reaccions del llibre "Organic Chemistry, Paula Yurkanis 8th edition" dividides en 3 grups: les ensenyades a QOI, QOII i QOIII. Les instruccions es troben especificades en el propi programa, però a continuació s’explica en més detall com funciona i com utilitzar l’aplicació per treure’n el màxim rendiment.
Cada targeta té doble cara, i cada cara està dividida en dues parts: a la esquerra es troba el reactiu, i a la dreta es troba, per una cara de la targeta, les condicions necessàries, i per l'altra cara, el producte que s'obté de la reacció. En alguns casos hi ha més d’un mètode per arribar al mateix producte. En aquests casos, la part de les “condicions necessàries” es subdivideix en diverses parts, a cada una de les quals es mostra un dels mètodes.

El programa permet estudiar les targetes en 3 modes: 
* Y - Repassar en l'ordre del llibre. Repassa en ordre de les 3 assignatures (primer QOI, llavors QOII, etc.), i dins de cada assignatura, en ordre del llibre.
*	R - Repassar en ordre aleatori.
*	A - Auto-avaluació de les targetes, en què les que menys et saps surten més sovint.

### 3.1. Modes d’estudi
#### 3.1.1	Repassar en ordre cronològic i aleatori
En els dos primers modes (Y i R) es pot navegar a través de les targetes o amb les fletxes del teclat o amb el ratolí: les fletxes ↑ i ↓ canvien de targeta, mentre que clicar sobre aquesta o les fletxes ← i → canvien entre la part del davant i darrere.
#### 3.1.2	Mode d’autoevaluació
En el mode d’autoavaluació (A), s’ha de prémer les tecles 1-4 (o clicar en els botons corresponents) depenent de com de bé l’estudiant es sap cada targeta, sent 1 que no se la sap, i 4 que se la sap perfectament. El programa té un algorisme que ensenya les targetes amb pitjor puntuació més sovint, de manera que es pugui focalitzar l’atenció en aquestes, i no es perdi el temps en les targetes que l’estudiant ja se sap. De nou, es pot canviar entre la part del davant i darrere de la targeta o bé amb les fletxes ← i → o bé clicant sobre aquesta.
 
L’estudiant pot escollir si vol estudiar només el producte que es formarà, només els reactius que es necessiten, o una barreja dels dos, així com el nombre de targetes que vol estudiar per cada set. L’aplicació ensenya el nombre de targetes que falta per estudiar, el nombre de targetes fallades, fàcils, mitjanes i difícils, així com la puntuació mitjana (sobre 10) que porta l’estudiant en aquell moment.

En el cas que aparegui una targeta que no és rellevant estudiar, es pot prémer la tecla [B] (o el botó corresponent) perquè no torni a aparèixer. L'acció només borrarà la targeta del mode [A]. Continuarà però apareixent en els modes de revisar les targetes per ordre [Y] o en ordre aleatori [R]. Per desfer aquesta acció, s’haurà de fer un reset del progrés (clicant [A] > [R] > [R] des de l’inici), que tornarà la puntuació a 0. Per borrar permanentment una targeta, vegi l’apartat 3.3.
El programa indica que es premi la tecla [Q] sempre que es vulgui tornar a la pantalla d'inici. En prémer la tecla, es guardarà automàticament tot el progrés que s’hagi fet, encara que un es trobi enmig de la revisió d'un set. Tot i així, el progrés no es guardarà si, enmig del set, es tanca l'aplicació. Per això, és recomanable prémer [Q] abans de tancar l'aplicació per assegurar que tot el progrés fet es guardi.

### 3.2	Com canviar l’assignatura a estudiar
En iniciar el programa per primer cop, aquest demanarà de quines assignatures es vol estudiar les targetes. Més endavant, per canviar l’assignatura a estudiar, s’ha d’anar a la pantalla d’inici ([Q]) i prémer la tecla [D] o clicar en el botó corresponent ([D] – Decidir de quina assignatura estudiar les reaccions).
Abans de distribuir l’aplicació és aconsellable anar a aquesta pàgina i, sense escollir cap de les opcions, prémer Enter dues vegades i tancar l’aplicació. Quan no hi ha cap set de targetes escollit, en obrir-la de nou aquesta demanarà automàticament de quina de les assignatures es vol estudiar les targetes, de manera que cadascú podrà escollir el que més li convingui.

### 3.3	Com modificar les targetes
En cas que una targeta contingui un error, o que els professors o l’alumne considerin que una targeta no és necessària o que falta alguna reacció; modificar, afegir o treure una targeta és un procés senzill.

Per tal de mostrar les imatges, el programa les va a buscar als PDFs “QOI_flaschards.pdf”, “QOII_flaschards.pdf” o “QOIII_flashcards.pdf” segons el cas, dins la carpeta “flashcard_docs”. En aquests PDFs es troben totes les targetes, alternant entre la seva part del davant i del darrere: les pàgines senars contenen el reactiu i producte, mentre que els pàgines parelles contenen el reactiu i les condicions necessàries.

Cada PDF ha estat creat a partir del Word corresponent, també en la carpeta, que consisteix en fulls modificats perquè tinguin les dimensions (8x6)cm. Cada full és alhora una casella d’una taula que ocupa tot el document, de manera que cada casella/full correspon a una cara d’una targeta. Per modificar una targeta simplement s’ha de buscar en aquest Word i fer les modificacions corresponents. Per eliminar-la, s’han de suprimir les dues caselles corresponents (cara de davant i de darrere). Es pot fer simplement seleccionant el contingut de les dues caselles, prenent el botó “DEL” i prémer “Enter”. Per afegir una targeta nova, s’ha d’inserir dues caselles (botó dret > Insereix > Insereix una fila a baix (x2)), i omplir-les amb la informació corresponent. S’ha d’assegurar que sempre es mantingui l’estructura: senars – reactiu/producte ; parells – reactiu/condicions. 
Un cop fetes les modificacions pertinents, s’ha de tornar a transformar el Word en PDF (Fitxer > Exportar > Crear PDF) i substituir-lo pel PDF actual (mantenint el seu nom). 
Si la targeta només s’ha modificat, en actualitzar el PDF el programa s’actualitzarà també automàticament. En el cas que s’hagi afegit o borrat alguna targeta, en entrar a l’aplicació s’haurà de fer un reset del progrés: des de la pantalla d’inici, s’haurà de prémer les tecles A > R > R. Amb això, l’aplicació ja estarà actualitzada per ser utilitzada amb les noves targetes.

### 3.4	Com fer un reset complet de l’aplicació.
El reset complet de l’aplicació es realitza en 2 passos:
1.	Des de la pantalla d’inici, clicar en A (Auto-avaluació) i llavors en R dos cops (Fer un reset del progrés). D’aquesta manera, es retornarà la puntuació actual a 0. 
2.	A la pantalla d’inici, clicar en D, i prémer Enter dos cops. Llavors tancar l’aplicació. D’aquesta manera, en obrir l’aplicació de nou, apareixerà la pantalla de decisió de les assignatures de les quals es volen estudiar les targetes. 
Amb el reset també tornaran a aparèixer totes les targetes que s’han borrat amb B. Per borrar/modificar completament una targeta, vegi l’apartat 3.3.

El reset borrarà la puntuació i la decisió sobre quines assignatures estudiar però no modificarà el PDF que conté les targetes: si s’ha modificat/afegit/eliminat targetes amb el procés explicat a l’apartat 3.3, aquestes es mantindran modificades després del reset.

### 3.5	Especificacions tècniques del programa i llenguatge de programació
El programa s’ha escrit en el llenguatge Python. Com a llibreries addicionals s’ha utilitzat pygame, random, os, json, PIL i fitz. Per crear l’executable s’ha utilitzat pyinstaller, una llibreria que permet passar de fitxers .py a .exe per ser utilitzats en ordenadors que no tenen Python instal·lat. 
Per funcionar, el programa requereix dels fitxers, tots inclosos dins de la carpeta “flashcard_docs”
*	benzene_icon.png: icona del programa
*	flashcard_dictionary.json: diccionari que emmagatzema el nom de les targetes i la seva puntuació
*	QO_type_dictionary.json: diccionari que emmagatzema 3 variables booleanes sobre quines assignatures estudiar
*	QOI/QOII/QOIII_flashcards.pdf: PDFs des d’on s’extreuen les imatges
*	photo.png: imatge que es mostra, extreta del PDF. Es va actualitzant cada vegada que es canvia de targeta en el programa.
El programa es pot trobar a GitHub en el següent enllaç: https://github.com/nuriafari/FemQO.git 
Qualsevol dubte, recomanació o modificació que es vulgui fer sobre el programa està benvingut. No dubtis en contactar-me en el correu nuriafarimd@gmail.com.
