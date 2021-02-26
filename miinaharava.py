import random
import time
import os

def main_menu():  print()                                         #Alkuvalikko  print("Miinaharava")  print("(P)elaa miinaharavaa")  print("(T)ilastot")  print("(L)opeta")  print()  while True:    valinta = input("Anna valinta: ")    if valinta.lower() == "p":      uusi_peli()    elif valinta.lower() == "t":      tilastot()    elif valinta.lower() == "l":      quit()    else:      print()      print("Virheellinen syöte!")      print("Valitse: (P)elaa, (T)ilastot tai (L)opeta")      print()def uusi_peli():
  """Luo kenttälistat, ottaa muistiin ajankohdan,
  käynnistää pelisilmukan ja tallentaa lopputuloksen."""
  leveys, korkeus = kysy_kentta()
  miinat = kysy_miinat(leveys, korkeus)
  print()
  
  kentta_hum = []
  for rivi in range(korkeus):
    kentta_hum.append([])
    for sarake in range(leveys):
      kentta_hum[-1].append("O")
  
  """Tietokoneelle luodaan oma versio listasta"""
  kentta_comp = []
  for rivi in range(korkeus):
    kentta_comp.append([])
    for sarake in range(leveys):
      kentta_comp[-1].append(" ")
      
  
  jaljella = []
  for x in range(leveys):
    for y in range(korkeus):
        jaljella.append((x, y))
  
  for _ in range(miinat):
    miinoita(kentta_comp, jaljella)

  kentta_comp = viimeistele_kentta(kentta_comp)
  
  aika = time.strftime("%H:%M")                     #Tilastoja varten tarvittavien tietojen keräys
  pvm = time.strftime("%d/%m/%Y")
  kulunut_aika, vuorot, lopputulos = peli_silmukka(kentta_comp, kentta_hum, miinat)
  tallenna_tilasto(aika, pvm, kulunut_aika, vuorot, lopputulos, leveys, korkeus, miinat)
  pelaa_uudelleen()

def kysy_kentta():
  while True:
    try:
      print()
      print("Anna pelikentän leveys (5-20) tai")
      leveys = input("palaa alkuvalikkoon syöttämällä (L): ")
      if leveys.lower() == "l":
        main_menu()
      elif int(leveys) > 20:
        print("Maksimileveys on 20")
        continue
      elif int(leveys) < 5:
        print("Minimileveys on 5")
        continue
      else:
        leveys = int(leveys)
        korkeus = int(input("Anna pelikentän korkeus (5-20): "))
        if korkeus > 20:
          print("Maksimikorkeus on 20")
          continue
        elif korkeus < 5:
          print("Minimikorkeus on 5")
          continue
        else:
          return leveys, korkeus
    except ValueError:
      print()
      print("Anna pelikentän leveys ja korkeus kokonaislukuina (5-20)!")
      continue

def kysy_miinat(leveys, korkeus):
  while True:
    try:
      print()
      miinat = int(input("Kuinka monta miinaa: "))
      if miinat == leveys * korkeus:
        print()
        print("Oletko itsetuhoinen?")
        return miinat
      elif miinat > leveys * korkeus:
        print()
        print("Miinat eivät mahdu pelikentälle!")
        continue
      elif miinat < 1:
        print()
        print("Syötä miinan määräksi ainakin 1")
      else:
        return miinat
    except ValueError:
      print()
      print("Anna miinojen määrä kokonaislukuna!")
      continue

def tarkista_koordinaatit(ymp_x, ymp_y, leveys, korkeus):
  """Tarkistaa, ovatko annetut koordinaatit pelikentän sisällä."""
  if ymp_x < 0 or ymp_x >= leveys or ymp_y < 0 or ymp_y >= korkeus:
    return False
  else:
    return True

def viimeistele_kentta(kentta_comp):
  """Sijoittaa numeroruudut tietokoneen käyttämään kenttään."""
  
  leveys = len(kentta_comp[0])
  korkeus = len(kentta_comp)                                      
  luvut = [-1, 0, 1]
  for y in range(korkeus):
    for x in range(leveys):
      if kentta_comp[y][x] == "X":
        continue
      ymparilla = []
      for y_1 in luvut:
        for x_1 in luvut:
          ymp_y = y + y_1
          ymp_x = x + x_1
          if tarkista_koordinaatit(ymp_x, ymp_y, leveys, korkeus) == True:
            ymparilla.append(kentta_comp[ymp_y][ymp_x]) 
          else:
            continue
          kentta_comp[y][x] = str(ymparilla.count("X"))
  return kentta_comp
  
def miinoita(kentta_comp, jaljella):
  """Asettaa kentälle yhden miinan satunnaiseen,
  vapaaseen ruutuun."""
  
  ruutu = jaljella[random.randint(0, len(jaljella) -1)]
  miina_x = ruutu[0]
  miina_y = ruutu[1]
  kentta_comp[miina_y][miina_x] = "X"
  jaljella.remove((miina_x, miina_y))

def peli_silmukka(kentta_comp, kentta_hum, miinat):
  """Kysyy koordinaatteja ja muokkaa pelaajan näkemää
  kenttää niiden mukaan. Tarkistaa myös onko peli voitettu
  vai ei, eli onko jaljella olevien ei-aukaistujen ruutujen
  määrä miinojen määrä. Palauttaa kuluneen ajan, vuorot,
  sekä lopputuloksen."""
  leveys = len(kentta_comp[0])
  korkeus = len(kentta_comp)
  start_time = time.time()
  vuorot = 0
  while True:
    jaljella = []
    
    for rivi in kentta_hum:                     #Lasketaan "O":n määrä
      jaljella.append(rivi.count("O"))
    jaljella = sum(jaljella)
    
    if miinat == leveys * korkeus:              #Jos pelaaja on syöttänyt maksimimäärän miinoja
      pass                                      #peliä ei voiteta automaattisesti.

    elif jaljella - miinat == 0:                #Tarkistetaan onko peli voitettu
      kulunut_aika = time.time() - start_time
      print()
      tulosta_kentta(kentta_hum)
      print()
      print("Voitit pelin {} vuorossa! Aikaa kului: {:.2f} sekuntia".format(vuorot, kulunut_aika))
      print()
      return kulunut_aika, vuorot, "Voitto"
    
    tulosta_kentta(kentta_hum)                  #Tulostetaan pelin tilanne
    print()
    
    x, y = kysy_koor(kentta_hum)                #Kysytään ja tarkistetaan koordinaatit
    vuorot += 1
    if kentta_comp[y][x] == "X":                #Käydään läpi mikä aukaistu koordinaatti on
      kentta_hum[y][x] = "X"
      print()
      tulosta_kentta(kentta_hum)
      print()
      print("Astuit miinaan ja räjähdit palasiksi!")
      print()
      kulunut_aika = time.time() - start_time
      return kulunut_aika, vuorot, "Häviö"
    elif kentta_hum[y][x] == " ":
      print("Ruutu on jo aukaistu!")
      print()
      continue
    elif kentta_comp[y][x] == "0":
      ruutu_taytto(kentta_comp, kentta_hum, x, y)
      continue
    elif 1 <= int(kentta_comp[y][x]) <= 8:
      kentta_hum[y][x] = kentta_comp[y][x]
      continue

def pelaa_uudelleen():
  while True:
        print()
        syote = input("(P)elaa uudelleen, palaa (A)lkuvalikkoon, tai (L)opeta peli: ")
        if syote.lower() == "p":
          uusi_peli()
        elif syote.lower() == "a":
          main_menu()
        elif syote.lower() == "l":
          quit()
        else:
          print()
          print("Virheellinen syöte!")
          continue

def ruutu_taytto(kentta_comp, kentta_hum, x, y):
  """Aukaisee algoritmisesti tyhjiä ruutuja."""
  leveys = len(kentta_comp[0])
  korkeus = len(kentta_comp)
  lista = [(x, y)]
  while(lista):
      pari = lista.pop()
      x = pari[0]
      y = pari[1]
      kentta_hum[y][x] = " "
      kentta_comp[y][x] = " "
      luvut = [-1, 0, 1]
      luvut_1 = [-1, 1]
      for ymp_y in luvut:              #Luodaan ympärillä olevat koordinaatit tarkastettaviksi
        for ymp_x in luvut:            #loopin avulla.
          x_1 = x + ymp_x
          y_1 = y + ymp_y
          if tarkista_koordinaatit(x_1, y_1, leveys, korkeus) == False:
            continue
          elif kentta_comp[y_1][x_1] == "0":
            lista.append((x_1, y_1))
          elif kentta_comp[y_1][x_1] == "X":
            continue
          elif kentta_comp[y_1][x_1] == " ":
            continue
          else:
            kentta_hum[y_1][x_1] = kentta_comp[y_1][x_1]

def tulosta_kentta(kentta):
  for rivi in kentta:
    print(" ".join(rivi))   #Muutetaan lista-alkiot merkkijonoksi

def kysy_koor(kentta_hum):
  leveys = len(kentta_hum[0])
  korkeus = len(kentta_hum)
  while True:
    print("Anna koordinaatit muodossa x,y tai")
    koor = input("palaa alkuvalikkoon painamalla enteriä: ")
    print()
    if len(koor) == 0:
      main_menu()
    koor = koor.split(",")
    try:
      if len(koor) != 2:
        continue
      x = int(koor[0])
      y = int(koor[1])
    except (ValueError, IndexError):
      print(("Anna koordinaatit kokonaislukuina"))
    else:
      if tarkista_koordinaatit(x, y, leveys, korkeus) == True:
        return x, y
      else:
        print("Koordinaatit ovat pelikentän ulkopuolella!")
        continue
        def tilastot():
  print()
  print("Näytä (T)ilastot, (N)ollaa tilastot tai palaa (A)lkuvalikkoon.")
  print("Tilastot näytetään muodossa:")
  print("Pelin ajankohta, pelissä kulunut aika, vuorojen määrä, lopputulos, pelikentän koko ja miinojen määrä.")
  while True:
    print()
    syote = input("Tee valintasi: ")
    if syote.lower() == "t":
      lataa_tilastot()
    elif syote.lower() == "n":
      nollaa_tilastot()
      print()
      print("Tilastot nollattu!")
    elif syote.lower() == "a":
      main_menu()
    else:
      print("Virheellinen syöte!")
  
def lataa_tilastot():
  try:
    if os.stat("miinaharava.txt").st_size == 0:
      print()
      print("Tilastoja ei ole vielä olemassa. Pelaa ensin yksi peli!")
      print()
      print("Palataan alkuvalikkoon...")
      main_menu()
    with open("miinaharava.txt") as tiedosto:
      for rivi in tiedosto.readlines():
        print(rivi)
  except IOError:
    print("Tilastoja ei ole vielä olemassa. Pelaa ensin yksi peli!")  
    print()
    print("Palataan alkuvalikkoon...")

def nollaa_tilastot():
  open("miinaharava.txt", "w").close()

def tallenna_tilasto(aika, pvm, kulunut_aika, vuorot, lopputulos, leveys, korkeus, miinat):               #pvm, kellonaika, kesto(m), kesto vuoroissa,
  try:                                                                                                    #lopputulos, kentän koko ja miinojen määrä
    with open("miinaharava.txt", "a") as kohde:
      kohde.write("{}, {}, {}, {:.2f}s, {} vuoroa, {}x{}, {} miinaa\n".format(lopputulos, aika, pvm, kulunut_aika, vuorot, leveys, korkeus, miinat))
  except IOError:
    print("Tilastoa ei voitu tallentaa.")

if __name__ == "__main__":
  
  main_menu()
  