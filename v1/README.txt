# Crear virtual env

conda deactivate
mkdir v1
cd v1
conda create -n CEPAL_NLP


# Activar virtual env
conda activate CEPAL_NLP


# Instalar dependencias
conda install pandas
conda install tensorflow
conda install flask
conda install keras
conda install pillow
conda install sentence-transformers

# Opcionalmente, exportar
conda list -e > req.txt

# Opcionalmente, cargar todas
conda install --file Requirements_Python38.txt

# Ejecutar
python3 app.py


# NUEVO:
conda create --name pytorch_env python=3.8

conda activate pytorch_env python=3.8

conda install -c pytorch pytorch torchvision
conda install tensorflow
conda install flask
conda install pandas
conda install keras
conda install sentence-transformers
conda install scikit-learn

# Opcionalmente, exportar
conda list -e > Requirements_Python38.txt

# Ejecutar
python3 app.py

o
python3.8 app.py

# Colocar lista de ODS
lista_ods.txt