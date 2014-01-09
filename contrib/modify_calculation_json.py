'''
Script to modify calculation JSON.
'''
import json
import webbrowser


PATH = '/home/local/WX/ben.koziol/Dropbox/nesii/project/ClimateTranslator/git/ClimateTranslator/ncpp/config/ocgis_calc.json'
OUT_PATH = '/tmp/ocgis_calc.json'


with open(PATH) as f:
    data = json.load(f)
data.pop('qed_dynamic_percentile_threshold')

with open(OUT_PATH,'w') as f:
    json.dump(data,f)
    
webbrowser.open(OUT_PATH)