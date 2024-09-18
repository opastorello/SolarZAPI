import requests
import json

class SolarZAPI:
    """
    Classe para interagir com a API do SolarZ.
    
    Métodos:
        - authenticate: Autentica o usuário e armazena o token.
        - get_client_context: Obtém o contexto do cliente e armazena IDs de usina.
        - get_last_status: Obtém o status atual da usina.
        - get_last_report: Obtém o último relatório da usina.
        - get_economized: Obtém dados de economia do cliente.
        - get_generation_day: Consulta dados de geração do dia.
        - get_generation_period: Consulta dados de geração por período.
        - get_unidade_sums: Obtém a geração total, consumo total e crédito corrente de uma unidade.
        - get_unidade_credit: Obtém o crédito corrente da unidade em kWh.
        - get_unidade_by_period: Retorna geração, consumo e crédito por mês em um período especificado.
        - get_notifications: Consulta as notificações do cliente.
        - mark_all_notifications_seen: Marca todas as notificações como lidas.
    """

    def __init__(self):
        """
        Inicializa a classe com a URL base da API e configura o cabeçalho padrão.
        """
        self.base_url = "https://app.solarz.com.br"
        self.usina_id = None
        self.usina_uuid = None
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }

    def authenticate(self, username, password):
        """
        Autentica o usuário na API do SolarZ e armazena o token de autenticação.

        :param username: O nome de usuário (email) para autenticação.
        :param password: A senha do usuário.
        :return: Retorna True se a autenticação for bem-sucedida, caso contrário, False.
        """
        url = f"{self.base_url}/cliente/authenticate"
        headers = self.headers.copy()
        payload = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response_data = response.json()

            # Verifica se a resposta foi bem-sucedida
            if response.status_code == 200:
                if 'token' in response_data:
                    token = response_data.get('token')
                    self.headers["Authorization"] = f"Bearer {token}"
                    print("Autenticação bem-sucedida!")
                    return True
                else:
                    print("Token de autenticação não encontrado na resposta.")
                    return None

            # Trata erros específicos da API
            if 'error' in response_data:
                print(f"Erro na autenticação: {response_data['error']}")
                return None

            # Mensagem para erros inesperados
            print(f"Erro inesperado: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura exceções específicas relacionadas ao requests
            print(f"Erro ao tentar autenticar: {str(e)}")
            return None

        except Exception as e:
            # Captura quaisquer outras exceções
            print(f"Erro inesperado: {str(e)}")
            return None

    def get_client_context(self):
        """
        Obtém o contexto do cliente, incluindo dados das usinas e a bandeira vigente.

        :return: Dicionário com os dados do contexto do cliente se bem-sucedido, caso contrário, None.
        """
        url = f"{self.base_url}/cliente/context"
        headers = self.headers.copy()

        try:
            response = requests.get(url, headers=headers)
            
            # Verifica o código de status da resposta
            if response.status_code == 200:
                client_context = response.json()
                print("Contexto do cliente obtido com sucesso!")
                
                # Processa os dados das usinas, se disponíveis
                usinas = client_context.get('usinas', [])
                if usinas:
                    self.usina_id = usinas[0].get('id')
                    self.usina_uuid = usinas[0].get('uuid')
                    print(f"UUID da usina armazenado: {self.usina_uuid}")
                    print(f"ID da usina armazenado: {self.usina_id}")
                else:
                    print("Nenhuma usina encontrada para este cliente.")
                
                return client_context
            
            # Mensagem de erro para códigos de status diferentes de 200
            print(f"Erro ao obter o contexto do cliente: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura exceções específicas relacionadas ao requests
            print(f"Erro ao tentar obter o contexto do cliente: {str(e)}")
            return None

        except Exception as e:
            # Captura quaisquer outras exceções
            print(f"Erro inesperado: {str(e)}")
            return None

    def get_last_status(self):
        """
        Obtém o status atual da usina.

        :return: Dicionário com os dados do status atual da usina se bem-sucedido, caso contrário, None.
        """
        if not self.usina_id:
            print("Erro: ID da usina não encontrado. Obtenha o contexto do cliente primeiro.")
            return None

        url = f"{self.base_url}/shareable/currently/usina"
        headers = self.headers.copy()
        params = {"id": self.usina_id}

        try:
            response = requests.get(url, headers=headers, params=params)
            
            # Verifica o código de status da resposta
            if response.status_code == 200:
                status = response.json()
                print("Status da usina obtido com sucesso!")
                return status
            
            # Trata erros específicos da API
            print(f"Erro ao obter o status: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura exceções específicas relacionadas ao requests
            print(f"Erro ao tentar obter o status: {str(e)}")
            return None

        except Exception as e:
            # Captura quaisquer outras exceções
            print(f"Erro inesperado: {str(e)}")
            return None

    def get_last_report(self):
        """
        Obtém o último relatório da usina associada ao cliente usando o UUID da usina.

        :return: Dados do último relatório da usina se bem-sucedido, caso contrário, None.
        """
        if not self.usina_uuid:
            print("Erro: UUID da usina não encontrado. Obtenha o contexto do cliente primeiro.")
            return None

        url = f"{self.base_url}/api-sz/app/cliente/plant/{self.usina_uuid}/lastReport"
        headers = self.headers.copy()

        try:
            response = requests.get(url, headers=headers)
            
            # Verifica o código de status da resposta
            if response.status_code == 200:
                last_report = response.json()
                print("Último relatório da usina obtido com sucesso!")
                return last_report
            
            # Trata erros específicos da API
            print(f"Erro ao obter o relatório: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura exceções específicas relacionadas ao requests
            print(f"Erro ao tentar obter o relatório: {str(e)}")
            return None

        except Exception as e:
            # Captura quaisquer outras exceções
            print(f"Erro inesperado: {str(e)}")
            return None

    def get_economized(self):
        """
        Obtém os dados de economia do cliente, incluindo valores economizados por mês, total economizado e retorno total.

        :return: Dicionário com os dados economizados se bem-sucedido, caso contrário, None.
        """
        url = f"{self.base_url}/api-sz/app/cliente/home/economizados"
        headers = self.headers.copy()

        try:
            response = requests.get(url, headers=headers)
            
            # Verifica o código de status da resposta
            if response.status_code == 200:
                economizados_data = response.json()
                print("Dados de economia obtidos com sucesso!")
                return economizados_data
            
            # Trata erros específicos da API
            print(f"Erro ao obter os dados economizados: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura exceções específicas relacionadas ao requests
            print(f"Erro ao tentar obter os dados economizados: {str(e)}")
            return None

        except Exception as e:
            # Captura quaisquer outras exceções
            print(f"Erro inesperado: {str(e)}")
            return None

    def get_generation_day(self, date: str, unite_portals: bool = True):
        """
        Consulta dados de geração do dia.

        :param date: Data no formato 'YYYY-MM-DD'.
        :param unite_portals: Se deve unir os portais (True/False).
        :return: Dados de geração do dia especificado se bem-sucedido, caso contrário, None.
        """
        if not self.usina_id:
            print("Erro: ID da usina não encontrado. Obtenha o contexto do cliente primeiro.")
            return None

        url = f"{self.base_url}/api-sz/generation/day"
        headers = self.headers.copy()
        params = {
            "usinaId": self.usina_id,
            "day": date,
            "unitePortals": str(unite_portals).lower()
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                generation_data = response.json()
                print("Dados de geração obtidos com sucesso!")
                return generation_data
            
            # Trata erros específicos da API
            print(f"Erro ao obter os dados de geração: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura erros específicos de requisição HTTP
            print(f"Erro ao tentar obter os dados de geração: {str(e)}")
            return None

        except Exception as e:
            # Captura erros inesperados
            print(f"Erro inesperado: {str(e)}")
            return None

    def get_generation_period(self, start_date: str, end_date: str, period: str = 'month', unite_months: bool = False, unite_portals: bool = False):
        """
        Consulta dados de geração por período.

        :param start_date: Data de início no formato 'YYYY-MM-DD'.
        :param end_date: Data de término no formato 'YYYY-MM-DD'.
        :param period: Granularidade do período. Pode ser 'day', 'week', 'month' ou 'year'.
        :param unite_months: Se deve unir os meses (True/False).
        :param unite_portals: Se deve unir os portais (True/False).
        :return: Dados de geração no período especificado se bem-sucedido, caso contrário, None.
        """
        if not self.usina_id:
            print("Erro: ID da usina não encontrado. Obtenha o contexto do cliente primeiro.")
            return None

        url = f"{self.base_url}/api-sz/generation/period"
        headers = self.headers.copy()
        params = {
            "usinaId": self.usina_id,
            "start": start_date,
            "end": end_date,
            "uniteMonths": str(unite_months).lower(),
            "unitePortals": str(unite_portals).lower(),
            "period": period
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                generation_data = response.json()
                print("Dados de geração obtidos com sucesso!")
                return generation_data
            
            # Trata erros específicos da API
            print(f"Erro ao obter os dados de geração: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura erros específicos de requisição HTTP
            print(f"Erro ao tentar obter os dados de geração: {str(e)}")
            return None

        except Exception as e:
            # Captura erros inesperados
            print(f"Erro inesperado: {str(e)}")
            return None

    def get_unidade_sums(self):
        """
        Retorna a geração total, consumo total e crédito corrente de uma unidade em kWh.

        :return: Lista de dicionários com as somas das unidades se bem-sucedido, caso contrário, None.
        """
        url = f"{self.base_url}/api-sz/app/cliente/unidades/sums"
        headers = self.headers.copy()

        try:
            response = requests.get(url, headers=headers)
            
            # Verifica o código de status da resposta
            if response.status_code == 200:
                sums_data = response.json()
                print("Somas das unidades obtidas com sucesso!")
                return sums_data
            
            # Trata erros específicos da API
            print(f"Erro ao obter as somas das unidades: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura exceções específicas relacionadas ao requests
            print(f"Erro ao tentar obter as somas das unidades: {str(e)}")
            return None

        except Exception as e:
            # Captura quaisquer outras exceções
            print(f"Erro inesperado: {str(e)}")
            return None

    def get_unidade_credit(self):
        """
        Retorna o crédito corrente da unidade em kWh.

        :return: Lista de dicionários com o crédito das unidades se bem-sucedido, caso contrário, None.
        """
        url = f"{self.base_url}/api-sz/app/cliente/unidades/credit"
        headers = self.headers.copy()

        try:
            response = requests.get(url, headers=headers)
            
            # Verifica o código de status da resposta
            if response.status_code == 200:
                credit_data = response.json()
                print("Crédito das unidades obtido com sucesso!")
                return credit_data
            
            # Trata erros específicos da API
            print(f"Erro ao obter o crédito das unidades: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura exceções específicas relacionadas ao requests
            print(f"Erro ao tentar obter o crédito das unidades: {str(e)}")
            return None

        except Exception as e:
            # Captura quaisquer outras exceções
            print(f"Erro inesperado: {str(e)}")
            return None

    def get_unidade_by_period(self, start_date: str, end_date: str):
        """
        Retorna a geração, consumo e crédito por mês em um período especificado.

        :param start_date: Data de início no formato 'YYYY-MM-DD'.
        :param end_date: Data de término no formato 'YYYY-MM-DD'.
        :return: Lista de dicionários com os dados das unidades no período se bem-sucedido, caso contrário, None.
        """
        url = f"{self.base_url}/api-sz/app/cliente/unidades"
        headers = self.headers.copy()
        params = {
            "start": start_date,
            "end": end_date
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            
            # Verifica o código de status da resposta
            if response.status_code == 200:
                period_data = response.json()
                print("Dados das unidades por período obtidos com sucesso!")
                return period_data
            
            # Trata erros específicos da API
            print(f"Erro ao obter os dados das unidades por período: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura exceções específicas relacionadas ao requests
            print(f"Erro ao tentar obter os dados das unidades por período: {str(e)}")
            return None

        except Exception as e:
            # Captura quaisquer outras exceções
            print(f"Erro inesperado: {str(e)}")
            return None

    def get_notifications(self, page: int = 0):
        """
        Consulta as notificações do cliente.

        :param page: Número da página de notificações a ser consultada (padrão é 0).
        :return: Dicionário com as notificações se bem-sucedido, caso contrário, None.
        """
        url = f"{self.base_url}/cliente/notifications/page/{page}"
        headers = self.headers.copy()

        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                notifications = response.json()
                print("Notificações obtidas com sucesso!")
                return notifications
            
            # Tratamento de erros da API
            print(f"Erro ao obter as notificações: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura erros específicos de requisição HTTP
            print(f"Erro ao tentar obter as notificações: {str(e)}")
            return None

        except Exception as e:
            # Captura erros inesperados
            print(f"Erro inesperado: {str(e)}")
            return None

    def mark_all_notifications_seen(self):
        """
        Marca todas as notificações como lidas.

        :return: Retorna True se a operação for bem-sucedida, caso contrário, False.
        """
        url = f"{self.base_url}/cliente/notifications/seenAll"
        headers = self.headers.copy()

        try:
            response = requests.post(url, headers=headers, json={})
            
            if response.status_code == 200:
                print("Todas as notificações foram marcadas como lidas com sucesso!")
                return True
            
            # Tratamento de erros da API
            print(f"Erro ao marcar notificações como lidas: {response.status_code} - {response.text}")
            return None

        except requests.RequestException as e:
            # Captura erros específicos de requisição HTTP
            print(f"Erro ao tentar marcar notificações como lidas: {str(e)}")
            return None

        except Exception as e:
            # Captura erros inesperados
            print(f"Erro inesperado: {str(e)}")
            return None
