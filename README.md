
# SolarZAPI

A classe `SolarZAPI` é uma implementação em Python projetada para interagir com a API do [SolarZ](https://www.solarz.com.br/), uma plataforma líder em gerenciamento de energia solar. 

Esta classe oferece uma interface simplificada para realizar operações essenciais, incluindo:

- **Autenticação do usuário:** Login e gestão de tokens de autenticação.
- **Recuperação de informações da usina:** Facilita o acesso a dados relevantes sobre a usina, como status atual e relatórios.
- **Consulta de dados de geração e economia:** Fornece métodos para obter informações detalhadas sobre a geração de energia e a economia gerada pela usina.

**Nota:** Esta classe não é uma integração oficial fornecida pelo [SolarZ](https://www.solarz.com.br/). É uma implementação independente que visa facilitar a interação com a API para desenvolvedores.

## Instalação

Certifique-se de que você tem a biblioteca `requests` instalada. Se não tiver, instale-a usando o pip:

```bash
pip install requests
```

# Uso

## Inicialização
Para utilizar a classe `SolarZAPI`, você precisa criar uma instância dela. 
Esta instância permitirá que você acesse todos os métodos disponíveis para interagir com a API do [SolarZ](https://www.solarz.com.br/).

```python
from SolarZ import SolarZAPI

# Cria uma instância da classe SolarZAPI
api = SolarZAPI()
```
## Métodos
`authenticate(username, password)`

Autentica o usuário na API do [SolarZ](https://www.solarz.com.br/) e armazena o token de autenticação.

### Parâmetros:
* `username` (str): O nome de usuário (email) para autenticação.
* `password` (str): A senha do usuário.

### Retorno:
* `True` se a autenticação for bem-sucedida.
* `None` caso contrário.

### Exemplo:
```python
success = api.authenticate('user@example.com', 'yourpassword')
if success:
    print("Autenticado com sucesso!")
else:
    print("Falha na autenticação.")
```
------------
`get_client_context()`

Obtém o contexto do cliente, incluindo dados das usinas e a bandeira vigente, por exemplo.

### Retorno:
* Um dicionário com os dados do contexto do cliente se bem-sucedido.
* `None` caso contrário.

### Exemplo:
```python
context = api.get_client_context()
if context:
    print("Contexto do cliente obtido com sucesso!")
else:
    print("Erro ao obter o contexto do cliente.")
```
------------
`get_last_status()`

Obtém o status atual da usina.

### Retorno:
* Um dicionário com os dados do status atual da usina se bem-sucedido.
* `None` caso contrário.

### Exemplo:
```python
status = api.get_last_status()
if status:
    print("Status da usina:", status)
else:
    print("Erro ao obter o status.")
```
------------
`get_last_report()`

Obtém o último relatório da usina associada ao cliente usando o UUID da usina.

### Retorno:
* Dados do último relatório da usina se bem-sucedido.
* `None` caso contrário.

### Exemplo:
```python
report = api.get_last_report()
if report:
    print("Último relatório:", report)
else:
    print("Erro ao obter o relatório.")
```
------------
`get_economized()`

Obtém os dados de economia do cliente, incluindo valores economizados por mês, total economizado e retorno total.

### Retorno:
* Um dicionário com os dados economizados se bem-sucedido.
* `None` caso contrário.

### Exemplo:
```python
economized = api.get_economized()
if economized:
    print("Dados de economia:", economized)
else:
    print("Erro ao obter os dados economizados.")
```
------------
`get_generation_day(date, unite_portals=True)`

Consulta dados de geração do dia.

### Parâmetros:
* `date` (str): Data no formato 'YYYY-MM-DD'.
* `unite_portals` (bool): Se deve unir os portais (padrão é True).

### Retorno:
* Dados de geração do dia especificado se bem-sucedido.
* `None` caso contrário.

### Exemplo:
```python
generation_day = api.get_generation_day('2024-09-17')
if generation_day:
    print("Dados de geração do dia:", generation_day)
else:
    print("Erro ao obter os dados de geração.")
```
------------
`get_generation_period(start_date, end_date, period='month', unite_months=False, unite_portals=False)`

Consulta dados de geração por período.

### Parâmetros:
* `start_date` (str): Data de início no formato 'YYYY-MM-DD'.
* `end_date` (str): Data de término no formato 'YYYY-MM-DD'.
* `period` (str): Granularidade do período. Pode ser 'day', 'week', 'month' ou 'year' (padrão é 'month').
* `unite_months` (bool): Se deve unir os meses (padrão é False).
* `unite_portals` (bool): Se deve unir os portais (padrão é False).

### Retorno:
* Dados de geração no período especificado se bem-sucedido.
* `None` caso contrário.

### Exemplo:
```python
generation_period = api.get_generation_period('2024-01-01', '2024-09-17')
if generation_period:
    print("Dados de geração por período:", generation_period)
else:
    print("Erro ao obter os dados de geração.")
```
------------
`get_unidade_sums()`

Retorna a geração total, consumo total e crédito corrente de uma unidade em kWh.

### Retorno:
* Lista de dicionários com as somas das unidades se bem-sucedido.
* `None` caso contrário.

### Exemplo:
```python
unidade_sums = api.get_unidade_sums()
if unidade_sums:
    print("Somas das unidades:", unidade_sums)
else:
    print("Erro ao obter as somas das unidades.")
```
------------
`get_unidade_credit()`

Retorna o crédito corrente da unidade em kWh.

### Retorno:
* Lista de dicionários com o crédito das unidades se bem-sucedido.
* `None` caso contrário.

### Exemplo:
```python
unidade_credit = api.get_unidade_credit()
if unidade_credit:
    print("Crédito das unidades:", unidade_credit)
else:
    print("Erro ao obter o crédito das unidades.")
```
------------
`get_unidade_by_period(start_date, end_date)`

Retorna a geração, consumo e crédito por mês em um período especificado.

### Parâmetros:
* `start_date` (str): Data de início no formato 'YYYY-MM-DD'.
* `end_date` (str): Data de término no formato 'YYYY-MM-DD'.

### Retorno:
* Lista de dicionários com os dados das unidades no período se bem-sucedido.
* `None` caso contrário.

### Exemplo:
```python
unidade_by_period = api.get_unidade_by_period('2024-01-01', '2024-09-17')
if unidade_by_period:
    print("Dados das unidades por período:", unidade_by_period)
else:
    print("Erro ao obter os dados das unidades por período.")
```
------------
`get_notifications()`

Consulta as notificações do cliente.

### Parâmetros:
* `page` (int): Número da página de notificações a ser consultada (padrão é 0).

### Retorno:
* Dicionário com as notificações se bem-sucedido.
* `None` caso contrário.

### Exemplo:
```python
notifications = api.get_notifications()
if notifications:
    print("Notificações:", notifications)
else:
    print("Erro ao obter as notificações.")
```
------------
`mark_all_notifications_seen()`

Marca todas as notificações como lidas.

### Retorno:
* `True` se a operação for bem-sucedida.
* `None` caso contrário.

### Exemplo:
```python
success = api.mark_all_notifications_seen()
if success:
    print("Todas as notificações foram marcadas como lidas!")
else:
    print("Erro ao marcar notificações como lidas.")
```

## Exemplo Completo

Aqui está um exemplo completo de como usar a classe `SolarZAPI`:

```python
from SolarZ import SolarZAPI

# Exemplo de uso da classe
api = SolarZAPI()

# Primeiro, autentica o usuário
if api.authenticate('user@example.com', 'yourpassword')

    # Obtendo contexto do cliente
    context = api.get_client_context()
    
    if context:
        # Obtendo status da usina
        status = api.get_last_status()
        if status:
            print("Status da usina:", status)
        
        # Obtendo último relatório
        report = api.get_last_report()
        if report:
            print("Último relatório:", report)
        
        # Obtendo dados de economia
        economized = api.get_economized()
        if economized:
            print("Dados de economia:", economized)
        
        # Obtendo dados de geração do dia
        generation_day = api.get_generation_day('2024-09-15')
        if generation_day:
            print("Dados de geração do dia:", generation_day)
        
        # Obtendo dados de geração por período
        generation_period = api.get_generation_period('2024-01-01', '2024-12-31')
        if generation_period:
            print("Dados de geração por período:", generation_period)
        
        # Obtendo somas das unidades
        unidade_sums = api.get_unidade_sums()
        if unidade_sums:
            print("Somas das unidades:", unidade_sums)
        
        # Obtendo crédito das unidades
        unidade_credit = api.get_unidade_credit()
        if unidade_credit:
            print("Crédito das unidades:", unidade_credit)
        
        # Obtendo dados das unidades por período
        unidade_by_period = api.get_unidade_by_period('2024-01-01', '2024-12-31')
        if unidade_by_period:
            print("Dados das unidades por período:", unidade_by_period)
        
        # Obtendo notificações
        notifications = api.get_notifications()
        if notifications:
            print("Notificações:", notifications)
        
        # Marcando todas as notificações como lidas
        if api.mark_all_notifications_seen():
            print("Todas as notificações foram marcadas como lidas!")
else:
    print("Falha na autenticação.")
```

## Relato de Bugs e Sugestões

Se você encontrou um bug ou tem sugestões para melhorar, por favor, siga estas etapas para nos ajudar a aprimorar esta classe:

1.  **Relatar um Bug:**
    -   Descreva o problema com o máximo de detalhes possível.
    -   Inclua passos para reproduzir o erro, se aplicável.
    -   Anexe capturas de tela ou logs que possam ajudar na identificação do problema.

2.  **Enviar Sugestões:**
    -   Explique claramente a melhoria ou funcionalidade que você gostaria de ver.
    -   Compartilhe como a sugestão pode beneficiar a experiência do usuário ou o funcionamento do aplicativo.

Por favor, abra um _[problema](https://github.com/opastorello/SolarZAPI/issues/new)_ no nosso repositório para relatar bugs ou enviar sugestões. 

Agradeço seu feedback e contribuição para a melhoria contínua desta classe!
