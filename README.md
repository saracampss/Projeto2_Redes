# Projeto2_Redes

Dentro da VM do Mininet, entre no diretório ./mininet/custom e coloque o topologia.py
Dentro da VM do Mininet, entre no diretório ./pox/pox/misc e coloque o firewall.py

Para rodar com o firewall, no diretório ./pox, utilize o comando "./pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning misc.firewall"
Para rodar sem o firewall, utilize o comando "./pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning"

No diretório ./mininet/custom, utilize o comando "sudo python topologia.py". As vezes pode ocorrer um erro e ser necessário utilizar o "sudo mn -c" antes para limpar os controladores´.
Utilize 10 hosts e 4 switches (acho que funciona de qualquer jeito, mas é o indicado no relatório do projeto). A partir daí, é possível utilizar comandos disponíveis no CLI. 
Escreva píngall para testar a conexão entre todos os hosts, hx ping hy para testar a conexão entre dois dos hosts, sendo hx e hy dois hosts.
