import json
import requests
 
# euro_value = 2.7864
# rus_rub_value = 4.2141
# zl_value = 6.8531
euro_value = json.loads(requests.get(" https://api.nbrb.by/exrates/rates/451").text)['Cur_OfficialRate']
rus_rub_value = json.loads(requests.get(" https://api.nbrb.by/exrates/rates/456").text)['Cur_OfficialRate']
zl_value = json.loads(requests.get(" https://api.nbrb.by/exrates/rates/508").text)['Cur_OfficialRate']

euro_to_rus_rub = 100*euro_value/rus_rub_value

rus_rub_to_euro = 64.86689


easygifts_coefficient = 3.51
easygifts_discount = 0.45

asgard_coefficient = 3.51
asgard_discount = 0.48

axpol_coefficient = 3.51
axpol_discount = 0.3

macma_coefficient = 3.51
macma_discount = 0.15

portobello_coefficient = 1.4
portobello_discount = 0.33

midocean_coefficient = 3.51
midocean_discount = 0

toppoint_coefficient = 3.51
toppoint_discount = 0.03

royal_coefficient = 3.51
royal_discount = 0.5

inspirion_coefficient = 3.51
inspirion_discount = 0.49

stricker_coefficient  = 3.51
stricker_discount = 0

cool_coefficient = 3.51
cool_discount = 0.5

project111_coefficient = 1.4
project111_discount = 0

oasiscatalog_coefficient = 1.62
oasiscatalog_discount = 0

happygifts_coefficient = 1.27
happygifts_discount = 0.19

plastoria_coefficient = 3.51
plastoria_discount = 0

citizengreen_coefficient = 3.51
citizengreen_discount = 0

sagaform_coefficient = 3.51
sagaform_discount = 0

pf_coefficient = 3.51
pf_discount = 0

maximceramics_coefficient = 3.51
maximceramics_discount = 0.3

cifra_coefficient = 3.51
cifra_discount = 0

l_shop_coefficient = 3.51
l_shop_discount = 0

malfini_coefficient = 3.51
malfini_discount = 0

mpm_coefficient = 3.51
mpm_discount = 0.4

makito_coefficient = 3.51
makito_discount = 0

fare_coefficient = 3.51
fare_discount = 0

avant_coefficient = 3.51
avant_discount = 0

voyager_xd_coefficient = 3.51
voyager_xd_discount = 0.3

promotionway_coefficient = 3.51
promotionway_discount = 0.42

# jaguar_coefficient = 3.51
# jaguar_discount = 0.43