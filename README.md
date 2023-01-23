# Desafio BHub
Esse projeto consiste em um CRUD simples para controle de clientes e suas contas bancárias e foi desenvolvido para o processo seletivo da empresa Bhub

## Como rodar o projeto
* Clonar o repositório 
  * https://github.com/DeeDee100/desafio_Bhub.git
* Rodar `docker compose up` e pronto, o projeto estará online na port 8000
* No link `localhost:8000/docs` está a documentação com exemplos de como usar a api

## Endpoints disponíveis
#### Clientes
|Link                                                             | Use               |
|:---------------------------------------------------------------|:------------------|
| [http://localhost:8000/](http://localhost:8000/)               | Root              |
| [http://localhost:8000/docs](http://localhost:8000/docs)       | Documentação                         |
| [http://localhost:8000/company](http://localhost:8000/company) | Lista todas os clientes cadastrados  |
| [http://localhost:8000/company/register](http://localhost:8000/company/register)    | Registra uma nova empresa              |
| [http://localhost:8000/company/delete/{cnpj}](http://localhost:8000/company/delete/{cnpj})   | Deleta uma empresa a partir do CNPJ informado  |
| [http://localhost:8000/company/update/{cnpj}](http://localhost:8000/company/update/{cnpj})   | Atualiza uma empresa a partir do CNPJ informado | 
#### Bancos
| Link | Uso |
|:---------------------------------------------------------------|:------------------|
| [http://localhost:8000/bank/cnpj](http://localhost:8000/bank/{cnpj}) | Lista os dados bancários cadastrados a partis do CNPJ informado |
| [http://localhost:8000/bank/register](http://localhost:8000/bank/register) | Registra um novo dado bacário |
| [http://localhost:8000/bank/delete/{cnpj}](http://localhost:8000/delete/{cnpj}) | Deleta um dado bancário a prtir do CNPJ informado |


#### Próximos passos:
* Adicionar regex pro cnpj
* Adicionar testes
* Adicionar autenticação OAuth
