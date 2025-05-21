import yfinance as yf
import numpy as np
import time
import pandas as pd
from tqdm import tqdm

class AssetAnalyzer:
    """
    Classe para análise de ativos utilizando dados históricos do Yahoo Finance.
    
    Essa classe oferece métodos para:
      - Verificar a liquidez (volume médio) dos ativos.
      - Calcular o beta do ativo em relação a um benchmark.
      - Calcular o Sharpe Ratio.
      - Obter o P/E Ratio.
      - Calcular o momentum.
      - Processar ativos em lotes para evitar bloqueios em requisições.
    
    Por padrão, os dados são coletados para um período de 6 meses, o que permite uma análise 
    de médio prazo dos ativos. As pausas entre as requisições e entre os lotes (0.5 e 5 segundos, 
    respectivamente) são utilizadas para evitar bloqueios por excesso de requisições à API.
    """
    
    def __init__(
        self,
        tickers: list,
        period: str = "6mo",
        batch_size: int = 100,
        sleep_between_requests: float = 0.5,
        sleep_between_batches: float = 5.0
    ):
        """
        Inicializa a instância do AssetAnalyzer.
        
        Args:
            tickers (list): Lista de tickers a serem analisados.
            period (str, opcional): Intervalo de tempo para coleta dos dados (padrão "6mo").
            batch_size (int, opcional): Número de tickers a processar por lote (padrão 100).
            sleep_between_requests (float, opcional): Tempo de pausa entre requisições individuais (padrão 0.5s).
            sleep_between_batches (float, opcional): Tempo de pausa entre os lotes de requisições (padrão 5.0s).
        """
        self.tickers = tickers
        self.period = period
        self.batch_size = batch_size
        self.sleep_between_requests = sleep_between_requests
        self.sleep_between_batches = sleep_between_batches

    def get_liquidity(self, tickers: list) -> dict:
        """
        Verifica a liquidez dos ativos, calculando o volume médio de negociação.
        
        Para cada ticker, busca dados históricos (últimos 6 meses por padrão) e calcula a média 
        do volume diário. Caso os dados estejam ausentes, define o volume como zero.
        
        Args:
            tickers (list): Lista de tickers a serem verificados.
        
        Returns:
            dict: Dicionário onde a chave é o ticker e o valor é o volume médio.
        """
        liquidity = {}
        for ticker in tqdm(tickers, desc="Verificando liquidez"):
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(period=self.period)
                avg_volume = data['Volume'].mean()
                liquidity[ticker] = avg_volume if avg_volume is not None else 0
                time.sleep(self.sleep_between_requests)
            except Exception as e:
                print(f"Erro ao processar {ticker}: {e}")
                liquidity[ticker] = 0
        return liquidity

    def get_beta(self, ticker: str, market_ticker: str = '^BVSP') -> float:
        """
        Calcula o beta de um ativo em relação a um índice de mercado.
        
        O beta é calculado com base nos retornos diários dos ativos e do índice, considerando 
        apenas datas em que ambos possuem dados disponíveis. Retorna None caso os dados estejam vazios.
        
        Args:
            ticker (str): Ticker do ativo.
            market_ticker (str, opcional): Ticker do índice de mercado (padrão '^BVSP').
        
        Returns:
            float: Valor do beta calculado ou None se não for possível calcular.
        """
        try:
            stock = yf.Ticker(ticker)
            market = yf.Ticker(market_ticker)
            
            stock_data = stock.history(period=self.period)['Close']
            market_data = market.history(period=self.period)['Close']
            
            if stock_data.empty or market_data.empty:
                print(f"Dados vazios para {ticker} ou {market_ticker}")
                return None
            
            # Alinhar as datas dos dados dos dois ativos
            # Remove datas com dados ausentes
            aligned_data = pd.DataFrame({
                'stock': stock_data,
                'market': market_data
            }).dropna()

            stock_returns = aligned_data['stock'].pct_change().dropna()
            market_returns = aligned_data['market'].pct_change().dropna()
            
            if stock_returns.empty or market_returns.empty:
                print(f"Retornos vazios para {ticker} ou {market_ticker}")
                return None
            
            covariance = np.cov(stock_returns, market_returns)[0][1]
            market_variance = np.var(market_returns)
            beta = covariance / market_variance
            return beta
        except Exception as e:
            print(f"Erro ao calcular beta para {ticker}: {e}")
            return None

    def get_sharpe_ratio(self, ticker: str, risk_free_rate: float = 0.06) -> float:
        """
        Calcula o Sharpe Ratio de um ativo.
        
        O Sharpe Ratio é calculado como a diferença entre o retorno médio do ativo e a taxa 
        livre de risco (ajustada para o período diário), dividido pela volatilidade dos retornos.
        
        Args:
            ticker (str): Ticker do ativo.
            risk_free_rate (float, opcional): Taxa livre de risco anual (padrão 0.06).
        
        Returns:
            float: Valor do Sharpe Ratio ou None se não for possível calcular.
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=self.period)['Close']
            daily_returns = data.pct_change().dropna()
            
            avg_return = daily_returns.mean()
            volatility = daily_returns.std()

            sharpe_ratio = (avg_return - risk_free_rate / 252) / volatility
            return sharpe_ratio
        except Exception as e:
            print(f"Erro ao calcular Sharpe Ratio para {ticker}: {e}")
            return None

    def get_pe_ratio(self, ticker: str) -> float:
        """
        Obtém o P/E Ratio (relação preço/lucro) de um ativo.
        
        Busca o valor na propriedade 'trailingPE' disponibilizada pela API do Yahoo Finance.
        
        Args:
            ticker (str): Ticker do ativo.
        
        Returns:
            float: Valor do P/E Ratio ou None se não estiver disponível.
        """
        try:
            stock = yf.Ticker(ticker)
            pe_ratio = stock.info.get('trailingPE', None)
            return pe_ratio
        except Exception as e:
            print(f"Erro ao obter P/E Ratio para {ticker}: {e}")
            return None

    def get_momentum(self, ticker: str, period: str = None) -> float:
        """
        Calcula o momentum de um ativo.
        
        O momentum é definido como a soma das variações percentuais do fechamento dos preços ao longo do período.
        Caso o período não seja informado, utiliza o período padrão definido na instância.
        
        Args:
            ticker (str): Ticker do ativo.
            period (str, opcional): Intervalo de tempo para análise (ex: '6mo'). Se None, utiliza self.period.
        
        Returns:
            float: Valor do momentum ou None se não for possível calcular.
        """
        try:
            period_to_use = period if period is not None else self.period
            stock = yf.Ticker(ticker)
            data = stock.history(period=period_to_use)['Close']
            momentum = data.pct_change().sum()
            return momentum
        except Exception as e:
            print(f"Erro ao calcular Momentum para {ticker}: {e}")
            return None

    def process_in_batches(self) -> list:
        """
        Processa os tickers em lotes, calculando diversas métricas para cada ativo.
        
        Para cada lote:
          - Verifica a liquidez dos ativos.
          - Calcula beta, Sharpe Ratio, P/E Ratio e momentum.
          - Armazena os resultados em uma lista de dicionários.
        
        São adicionadas pausas entre os ativos e entre os lotes para evitar bloqueios nas requisições.
        
        Returns:
            list: Lista de dicionários contendo as métricas para cada ativo.
        """
        selected_assets = []
        
        # Dividindo os tickers em lotes conforme o batch_size definido
        total_batches = (len(self.tickers) + self.batch_size - 1) // self.batch_size
        for i in range(0, len(self.tickers), self.batch_size):
            batch = self.tickers[i:i+self.batch_size]
            print(f"\n🔄 Processando lote {i // self.batch_size + 1} de {total_batches}...\n")
            
            liquidity = self.get_liquidity(batch)
            
            for ticker in tqdm(batch, desc="Analisando ativos", position=0):
                try:
                    beta = self.get_beta(ticker)
                    sharpe = self.get_sharpe_ratio(ticker)
                    pe_ratio = self.get_pe_ratio(ticker)
                    momentum = self.get_momentum(ticker)
                    
                    print(f"Analisando {ticker}: Beta={beta}, Sharpe={sharpe}, PE={pe_ratio}, Momentum={momentum}")
                    
                    selected_assets.append({
                        'ticker': ticker,
                        'liquidity': liquidity[ticker],
                        'beta': beta,
                        'sharpe': sharpe,
                        'pe_ratio': pe_ratio,
                        'momentum': momentum
                    })
                    
                    time.sleep(self.sleep_between_requests)
                except Exception as e:
                    print(f"Erro ao processar {ticker}: {e}")
            
            print("⏳ Aguardando para evitar limitação...")
            time.sleep(self.sleep_between_batches)
        
        return selected_assets

# Leitura dos tickers a partir de um arquivo
with open("/workspaces/Case-H2/data/valid_tickers/valid_tickers_part_4.txt", "r") as file:
    tickers_list = [line.strip() for line in file.readlines()]

# Criação da instância do AssetAnalyzer
analyzer = AssetAnalyzer(
    tickers=tickers_list,
    period="6mo",           # Utilizando dados dos últimos 6 meses
    batch_size=100,
    sleep_between_requests=0.5,
    sleep_between_batches=5.0
)

# Processamento dos ativos em lotes
selected_assets = analyzer.process_in_batches()

# Criação do DataFrame e salvamento em CSV para análise futura
df = pd.DataFrame(selected_assets)
df.to_csv("selected_assets_5.csv", index=False)
print("\nAtivos selecionados salvos em 'selected_assets_5.csv'")