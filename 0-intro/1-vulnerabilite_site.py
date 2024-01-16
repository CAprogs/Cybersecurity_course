# Import bibliothèque
import requests

# https://www.ecam-epmi.fr/robots.txt
response = requests.get('https://www.ecam-epmi.fr/')
 
if(response.status_code == 200):
  response = requests.get('https://www.ecam-epmi.fr/admin.php')
  print('Demande réussie!')
 
  if(response.status_code == 200):
    print('Site vulnérable')
  else:
    print("Le site n'es pas vulnérable")
else:
  print('Demande échouée!')