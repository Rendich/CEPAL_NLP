# Crear y activar virtual env

conda deactivate
mkdir v1
cd v1
conda create -n CEPAL_NLP
conda activate CEPAL_NLP


# Instalar dependencias
conda install tensorflow
conda install flask
conda install keras
conda install pillow

# Opcionalmente, exportar
conda list -e > req.txt

# Ejecutar
python3 app.py


# NUEVO:
conda create --name pytorch_env python=3.8

conda activate pytorch_env

conda install -c pytorch pytorch torchvision
conda install tensorflow
conda install flask
conda install keras
conda install sentence-transformers

# Opcionalmente, exportar
conda list -e > Requirements_Python38.txt

# Ejecutar
python3 app.py
