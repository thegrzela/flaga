import os

os.system('sudo systemctl daemon-reload')
os.system('sudo systemctl restart nginx')
os.system('sudo systemctl restart flaga.service')
