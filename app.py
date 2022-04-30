import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image
import streamlit.components.v1 as components
import json
import requests


models = {'TRIUMPH': ('BONNEVILLE SE promo', 'BONNEVILLE T100 promo', 'Bonneville Bobber Black', 'Bonneville Speedmaster promo', 'DAYTONA 600 promo', 'DAYTONA 650', 'DAYTONA 675 TRIPLE', 'SPEED Four', 'SPEED Four promo', 'SPEED TRIPLE', 'SPEED TRIPLE ABS promo', 'SPEED TRIPLE RS', 'SPEED Triple R promo', 'STREET TRIPLE', 'STREET TRIPLE 660', 'STREET TRIPLE R', 'STREET TRIPLE R promo', 'STREET TRIPLE RS promo', 'STREET TRIPLE S', 'STREET TRIPLE S 660', 'Speed Triple S promo', 'Speedmaster 800', 'Speedmaster 900', 'Street Triple R promo', 'Street Triple R x promo', 'Street Twin', 'TIGER 1050', 'TIGER 800', 'TIGER 800 XC', 'TIGER 800 XC X', 'TIGER 800 promo', 'TIGER Explorer 1200', 'TIGER Explorer 1200 XC promo', 'TIGER Explorer 1200 XCA promo', 'TIGER Explorer 1200 XR', 'Thruxton EFI promo', 'ThruxtonRS promo', 'Tiger 800 XR X', 'Tiger 800 XR X promo'), 'SYM': ('CruisymAlpha300 promo', 'Fiddle 125', 'Fiddle III', 'Fiddle III promo', 'HD 300', 'JOYMAX 125', 'JOYMAX 300i ABS S&S Sport', 'Jet 4 50 4T', 'MAXSYM 400', 'MAXSYM 600i ABS Sport promo', 'Maxsym 600i ABS', 'Maxsym 600i ABS promo', 'Mio 115', 'Symphony ST 200i CBS'), 'YAMAHA': ('FJR 1300 A', 'FJR 1300 A promo', 'FJR 1300 AE promo', 'FZ1 N', 'FZ6 N', 'FZ6 S', 'FZ6 S ABS', 'FZ8 N', 'MT 01', 'MT 01 promo', 'MT 03', 'MT 03 promo', 'MT 09', 'MT 09 promo', 'MT10', 'MT10 SP', 'MT10 promo', 'Majesty 400', 'Niken', 'Super Ténéré promo', 'T-Max 500', 'T-Max 500 ABS', 'TMAX 560 TECH MAX promo', 'V-Max 1200', 'V-Max 1700', 'X MAX 125 Iron Max', 'X MAX 250', 'X MAX 250 promo', 'X MAX 400 ABS', 'X MAX 400 promo', 'X enter 125', 'X-CITY 250', 'X-MAX 125', 'X-MAX 125 promo', 'X-MAX 250 Momodesing', 'X-MAX 300', 'X-MAX 400 promo', 'XJ6 Diversion N', 'XJR 1300 promo', 'XSR900 ABS', 'XT 660 X', 'XV 1100 Virago', 'XVS 650 A Drag Star Classic', 'XVS 650 Drag Star Classic', 'XVZ 1300 Royal Star Venture', 'YP Majesty 150', 'YZF R 125 promo', 'YZF R1', 'YZF R1 promo', 'YZF R6', 'YZF R6R promo', 'YZF-R3'), 'PEUGEOT': ('Citystar 125 ABS', 'Django 50 Allure promo', 'Django50Heritage promo', 'Metropolis 400 RX-R promo', 'Metropolis 400 promo', 'SATELIS 125i urban promo'), 'HONDA': ('CB 1000R', 'CB 1000R promo', 'CB 500 F', 'CB 500 F promo', 'CB 500 X ABS', 'CB 500 X promo', 'CB 500F', 'CB 500F promo', 'CBF 1000', 'CBF 1000 promo', 'CBF 500 promo', 'CBF 600N', 'CBF 600S', 'CBF 600S promo', 'CBR 1000 RR Fireblade', 'CBR 1000 RR Fireblade promo', 'CBR 1000RR', 'CBR 1000RR Fireblade', 'CBR 1000RR Fireblade promo', 'CBR 1000RR promo', 'CBR 1100 XX promo', 'CBR 600 RR', 'CBR 600F', 'CBR 600F promo', 'CBR 650 F promo', 'CBR 650F', 'CRF 250 RX', 'CRF 450 L promo', 'CRF1000L Africa Twin', 'CRF1000L Africa Twin DCT', 'CTX 700', 'Crossrunner VFR800X', 'Crossrunner VFR800X promo', 'FMX 650 promo', 'FORZA 250 EX', 'FORZA 250 X', 'Forza 125', 'Forza 125 promo', 'Forza 300', 'Integra', 'Integra promo', 'NC 700 S', 'NC 750 S', 'NC 750 S DTC ABS', 'NC 750 X DCT', 'NT 650 V DEAUVILLE', 'NT 700 DEAUVILLE', 'NT 700 V DEAUVILLE', 'NTV 650 REVERE promo', 'PAN-EUROPEAN ST 1300 promo', 'Passion 125 I.E.', 'Rebel 500', 'S-WING 125', 'SCOOPY SH300i', 'SCOOPY SH300i TopBox', 'SCOOPY SH300i promo', 'SILVER WING 600', 'TRANSALP XL 650 V', 'VARADERO XL1000V', 'VFR 1200 F DCT promo', 'VFR 1200 F promo', 'VFR 800 FI', 'VFR 800 FI promo', 'VT 750 C SHADOW', 'X-ADV', 'XL 125V'), 'KAWASAKI': ('ER 5', 'ER 6F', 'ER 6F promo', 'ER 6N', 'GTR 1400', 'GTR 1400 promo', 'J 125', 'J 125 promo', 'Ninja 1000 SX', 'Ninja H2 SX SE +', 'Ninja H2 SX SE promo', 'VERSYS 1000', 'VERSYS 650', 'VERSYS 650 promo', 'VN 1600 CLASIC', 'VN VULCAN 800 CLASIC', 'Versys 650 ABS', 'Vulcan S', 'Z 1000', 'Z 1000 SX', 'Z 1000 SX promo', 'Z 750', 'Z 750 promo', 'Z 800e', 'Z 800e promo', 'Z 900', 'Z 900 promo', 'ZX 10R KRT promo', 'ZX 10R promo', 'ZX 6R', 'ZX 6R 636', 'ZX 6R promo', 'ZX-10RR', 'ZX6R promo', 'ZZR 1400', 'ZZR 1400 promo'), 'APRILIA': ('Caponord', 'Dorsoduro 750 promo', 'RS 660', 'RSV 4 R APRC promo', 'RSV Mille Tuono', 'RSV4 RR promo', 'SMV 750 Dorsoduro', 'SMV 750 Dorsoduro ABS promo', 'SMV 750 Dorsoduro promo', 'SRV 850', 'SX 125', 'Shiver 750', 'Shiver 750 GT promo', 'Shiver 750 promo', 'Shiver 900', 'Sportcity 125 promo', 'Tuono 1000 R', 'Tuono 125', 'Tuono V4 1100 Factory promo'), 'MOTO GUZZI': ('V7 II Racer', 'V7 III Stone', 'V7 III Stone promo', 'V9 Roamer promo'), 'ROYAL ENFIELD': ('Meteor 350 promo',), 'HUSQVARNA': ('701 Supermoto promo', 'SVARTPILEN 401', 'Svartpilen 701 promo', 'Vitpilen 701', 'Vitpilen 701 promo'), 'KTM': ('1050 Adventure', '1050 Adventure promo', '1090 Adventure R promo', '1190 Adventure', '1190 Adventure promo', '125 Duke', '125 Duke promo', '1290 Super Adventure', '1290 Super Adventure R promo', '1290 Super Adventure T', '1290 Super Duke GT promo', '1290 Super Duke R ABS', '1290 Super Duke R ABS promo', '250 EXC-F', '300 EXC', '390 Duke', '690 DUKE promo', '690 SMC R ABS', '690 SMC R ABS promo', '790 Duke', '790 Duke promo', '890 Adventure promo', '950 Adventure', '990 SUPER DUKE promo', 'DUKE II', 'EXC 300', 'Freeride 250 F', 'LC4 620 SUPERCOMPETICION', 'RC8 1150'), 'DUCATI': ('1098 SUPERBIKE', '1098 SUPERBIKE promo', '1299 Panigale S Anniversario', '749 R promo', '848 Superbike promo', 'DIAVEL 1198 promo', 'DIAVEL Dark promo', 'Diavel promo', 'HYPERMOTARD 1000', 'Hypermotard 939 promo', 'Hyperstrada promo', 'MONSTER 1100', 'MONSTER 1200', 'MONSTER 620', 'MONSTER 696', 'MONSTER 796', 'MONSTER 796 promo', 'MONSTER S2R 1000 promo', 'MONSTER S2R 800', 'MONSTER S2R 800 promo', 'MONSTER796 promo', 'MULTISTRADA 1000 DS', 'MULTISTRADA 1100', 'MULTISTRADA 1200 S Sport promo', 'MULTISTRADA 1200 promo', 'MULTISTRADA 620 promo', 'Multistrada 1260 S promo', 'Scrambler 1100', 'Scrambler 1100 promo', 'Scrambler Café Racer promo', 'Scrambler Classic', 'Scrambler Desert Sled', 'Scrambler Sixty2', 'Streetfighter 1100', 'Streetfighter 1100 promo', 'Streetfighter V4 promo', 'SuperSport'), 'BMW': ('C 400 X', 'C 600 Sport', 'C 600 Sport promo', 'C 650 GT', 'C 650 GT promo', 'C 650 Sport', 'F 650', 'F 650 GS', 'F 700 GS', 'F 700 GS promo', 'F 800 GS', 'F 800 GS Adventure', 'F 800 GS promo', 'F 800 GT', 'F 800 GT promo', 'F 800 R', 'F 800 R 2015', 'F 800 R promo', 'F 800 S promo', 'F 800 ST', 'F 800 ST promo', 'F 900 XR', 'G 310 GS', 'G 310 R', 'G 650 GS', 'K 1200 GT', 'K 1200 LT promo', 'K 1200 R', 'K 1200 R Sport promo', 'K 1200 R promo', 'K 1200 RS', 'K 1200 RS promo', 'K 1200 S', 'K 1200 S promo', 'K 1300 GT', 'K 1300 R promo', 'K 1300 S', 'K 1600 GT', 'K1200R promo', 'R 1200 GS', 'R 1200 GS 105cv', 'R 1200 GS 98cv promo', 'R 1200 GS Adventure', 'R 1200 GS Adventure 105cv', 'R 1200 GS promo', 'R 1200 R', 'R 1200 R promo', 'R 1200 RT', 'R 1200 RT 110cv', 'R 1200 S promo', 'R 1250 R promo', 'R 1250 RT promo', 'R 850 R', 'R 850 R promo', 'R nineT', 'R nineT Racer', 'R nineT Scrambler', 'R nineT Scrambler promo', 'R nineT Urban GS', 'R nineT promo', 'S 1000 R', 'S 1000 RR', 'S 1000 XR promo'), 'SUZUKI': ('B-KING 1340', 'BURGMAN 125', 'BURGMAN 125 promo', 'BURGMAN 200', 'BURGMAN 200 promo', 'BURGMAN 400', 'BURGMAN 400 promo', 'BURGMAN 650 Executive', 'BURGMAN 650 Executive promo', 'Bandit 650 S', 'Bandit 650 S promo', 'GS 500', 'GSF 600 Bandit S', 'GSF 600 Bandit S promo', 'GSR 600', 'GSR 750 promo', 'GSR750', 'GSX 1250 FA promo', 'GSX 650 F', 'GSX 650 F promo', 'GSX R1000', 'GSX R1000 promo', 'GSX R600', 'GSX R600 promo', 'GSX R750', 'GSX-R1000R promo', 'GSX-S 1000 F', 'GSX-S 1000 promo', 'GSX-S125 ABS promo', 'GSX250R/ABS promo', 'Gladius 650', 'Gladius 650 ABS', 'Hayabusa 1300 promo', 'Intruder C1500 promo', 'Intruder C800 promo', 'LS 650 Savage promo', 'Marauder 250', 'Marauder 250 promo', 'V-Strom 1000', 'V-Strom 1000 ABS', 'V-Strom 650', 'V-Strom 650 ABS', 'VL 800 Intruder Volusia', 'VanVan 125'), 'KYMCO': ('AK 550', 'AK 550 promo', 'Agility CITY 125', 'Grand Dink 125', 'Grand Dink 125 promo', 'Like 125', 'People 50 S', 'Super Dink 125 ABS', 'Super Dink 350i', 'Super Dink 350i promo', 'Xciting 400i'), 'HARLEY DAVIDSON': ('Dyna Low Rider', 'Dyna Switchback', 'Softail Slim', 'Sportster 1200 Custom', 'Sportster 1200 promo', 'Sportster 883', 'Sportster 883 Iron', 'Sportster 883 Superlow', 'Sportster Forty-Eight', 'Sportster Superlow 1200T', 'Sportster XR 1200 promo', 'Street 750', 'Touring Electra Glide Classic promo', 'VRSC Night Rod Special', 'VRSC V-Rod', 'VRSC V-Rod Muscle promo', 'VRSCA V-Rod Screaming Eagle promo'), 'MV AGUSTA': ('BRUTALE 1090 RR', 'BRUTALE 750S', 'BRUTALE 800', 'BRUTALE 800 EAS ABS promo', 'BRUTALE 800 RR promo', 'BRUTALE 990 R promo', 'Dragster 800 RR America', 'Turismo Veloce 800 Lusso'), 'GAS GAS': ('EC 250 R promo', 'EC 350 F'), 'VESPA': ('Elettrica L1', 'GTS 300 Super promo', 'LXV 50 2T', 'Primavera 125', 'Primavera 50 2T', 'S 125 ie'), 'PIAGGIO': ('Beverly 350 ABS promo', 'Beverly 400 HPE', 'LIBERTY 50 I-GET promo', 'MP3 350 ABS/ASR promo', 'MP3 500 Sport ABS/ASR promo', 'X EVO 400', 'X10 350 ie', 'beverly 300 ie', 'beverly 300 ie promo', 'beverly Sport Touring 350 ie'), 'HUSABERG': ('TE 250',), 'ZONTES': ('X-310',), 'BENELLI': ('502 C', 'BN 251', 'BN 251 ABS', 'Leoncino 250', 'TRK 251', 'TRK 502'), 'FANTIC': ('Caballero Flat Track 500',), 'MASH': ('Cafe Racer', 'Five Hundred', 'Seventy Five', 'X-Ride 650'), 'HANWAY': ('Raw 125 Cafe', 'Scrambler 125'), 'DAELIM': ('XQ2 300',), 'MACBOR': ('Lord Martin 125', 'Montana XR3', 'Shifter MC1'), 'LML': ('STAR 200 4T Deluxe',), 'CFMOTO': ('650 MT',), 'GOES': ('G 125 GT',), 'GILERA': ('Nexus 300',), 'SWM': ('Super Dual T promo',), 'MOTOR HISPANIA': ('REVENGE',), 'ORCAL': ('Astor 125',), 'MITT': ('125 PK',), 'FKM': ('Street Scrambler 125',), 'DERBI': ('Variant Sport 50',), 'INDIAN': ('FTR 1200 promo',), 'QUADRO': ('QV3',), 'RIEJU': ('Century',)}
brands = ('APRILIA', 'BENELLI', 'BMW', 'CFMOTO', 'DAELIM', 'DERBI', 'DUCATI', 'FANTIC', 'FKM', 'GAS GAS', 'GILERA', 'GOES', 'HANWAY', 'HARLEY DAVIDSON', 'HONDA', 'HUSABERG', 'HUSQVARNA', 'INDIAN', 'KAWASAKI', 'KTM', 'KYMCO', 'LML', 'MACBOR', 'MASH', 'MITT', 'MOTO GUZZI', 'MOTOR HISPANIA', 'MV AGUSTA', 'ORCAL', 'PEUGEOT', 'PIAGGIO', 'QUADRO', 'RIEJU', 'ROYAL ENFIELD', 'SUZUKI', 'SWM', 'SYM', 'TRIUMPH', 'VESPA', 'YAMAHA', 'ZONTES')

# embed streamlit docs in a streamlit app
#components.iframe("https://docs.streamlit.io/en/latest")
st.set_page_config(
     page_title="Mundimoto",
     page_icon="🏍️",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )
st.title('Mundimoto🏍️')
st.header('Calcula el valor de tu motocicleta')
st.subheader('Sin compromisos, sin mentiras')
#[theme]
#primaryColor="#000000"
#backgroundColor="#000000"
#secondaryBackgroundColor="#000000"
#textColor="#262730"
#font="sans serif"
brand = st.selectbox("Marca", brands)
terminos=False
name = st.selectbox("Modelo", models.get(brand))
kms = st.select_slider(
     'Seleccione los kilometros que tiene su motocicleta',
     options=['0-20', '20-100', '100-500', '500-1000', '1000-1500', '1500-3000', '3000+'])#falta especificar valores realistas
license = st.radio("Seleccione la licencia o licencias que permiten conducir su motocicleta", ['A','A1','A2','AB'])
year = st.slider("Año de matriculación", 1985,2022,2008)
cycleType = st.selectbox('Seleccione el tipo de moto que más se ajusta',('Scooter','Maxi-Scooter','Classic','Naked','Sport','Touring','Trail','Off-Road','Custom','Tres Ruedas'))
typeImage = Image.open('images/'+cycleType+'Type.png')
st.image(typeImage)
color = st.color_picker('Seleccione el color de su motocicleta', '#00f900')
if st.checkbox('Acepto los términos y condiciones'):
	terminos = True
if st.button('Dame un super precio!!'):
	if terminos:
		if not name:
			st.warning('Porfavor complete el modelo de su motocicleta')
			st.stop()
		with st.spinner('Calculando precio aproximado...'):
    			time.sleep(5)
		st.success('Precio calculado satisfactoriamente :sunglasses:')
		st.balloons()
		data_set = {"brand":brand, "name":name, "kms":kms, "license":license, "year":year, "cycleType":cycleType}
		json_dump=json.dumps(data_set)
		r = requests.post(url='http://')
		
		#enviar data a mi amigo del departamento del back-end
	else:
		st.warning('Porfavor, acepte los terminos y condiciones para continuar ')
