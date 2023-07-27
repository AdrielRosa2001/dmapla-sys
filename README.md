# Dmapla Sys

Sistema Web Feito em Flask destinado a uso interno da empresa D'mapla - Utilidades para o lar

![preview](./demo/representation.png)

> Adriel Rosa (update 27/07/2023  19:20 PM)

## Funcionalidades: 

### Cadastro:

![preview](./demo/cadastro_sis.png)

- Realiza o cadastro de novos usuários fazendo validações de usuarios ja cadastrados com o banco de dados.

##

### Login:

![preview](./demo/login_sis.png)

- Realiza o login de usuários no sistema.

##

### Perfil:

![preview](./demo/perfil_sis.png)

- Exibe o perfil do usuario logado permitindo alterações de dados do mesmo.

##

###  Consulta:

![preview](./demo/consulta_produto.png)

##

  ## Consulta PC:

  ![preview](./demo/consulta-pc.gif)
  
  - Realiza a consulta de produtos em dispositivos desktop via digitação no input text ou atravez do leitor de codigo de barras.
  
  ###
  
  ## Consulta Mobile:

  ![preview](./demo/consulta-phone.gif)
  
  - Realiza consulta de produtos via digitação ou foto do codigo de barras do produto.
  - Foi utilizado o OpenCV para manipulação da imagem e o pyzbar para detecão do codigo de barras na imagem.
  
  ###
  
  ## Gerenciamento de Usuários:

  ![preview](./demo/user_manager.png)
  
  - Painel destinado ao gerenciamento de usuários (Apenas o admin do sistema tem acesso ao painel).
  
  ###

  ## Logs do sistema:

  ![preview](./demo/log_sys.png)
  
  - Painel destinado a exibição de logs do sistema (Apenas o admin do sistema tem acesso ao painel).
  
  ###

 ##
 
 ## Tecnologias:
 - Flask
 - Flask-SQLAlchemy
 - SQLAlchemy
 - pyodbc
 - waitress
 - opencv-python
 - pathlib
 - pyzbar
 
 ## Contato:
 
 - E-mail: adrielrosa@live.com 
 - LinkedIn: https://www.linkedin.com/in/adriel-rosa-660431144/
