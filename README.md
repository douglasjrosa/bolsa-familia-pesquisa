# Bolsa Família — Pesquisa Comparativa 2024

Pesquisa que compara o custo e a escala do **Bolsa Família** com juros da
dívida pública, renúncias fiscais, emendas parlamentares e previdência militar —
usando fontes oficiais e institucionais (MDS, IBGE, Banco Central, Receita/SPE,
Portal da Transparência, TCU, IPEA, FGV), e registrando opiniões que circularam
sobre cada tema.

O documento foi escrito para leitura independente (incluindo conversão a PDF).
Não é guia de conversa nem apresentação. Não defende nem ataca o programa.

## Documento principal

Abra **[docs/bolsa-familia-pesquisa.md](docs/bolsa-familia-pesquisa.md)** —
pesquisa completa (seções 0–11, gráficos, Opiniões e Fatos, e fontes).

## Ano-base

**2024** — último exercício em que todas as rúbricas do estudo têm série anual
fechada e comparável (incluindo a DIRBI de renúncias fiscais).

## Estrutura do repositório

```
docs/bolsa-familia-pesquisa.md  # Pesquisa completa
data/2024_master.csv            # Todos os números usados
data/sources_registry.json      # Título + URL de cada fonte de dado
assets/charts/*.png             # Gráficos gerados
scripts/generate_charts.py      # Regenera os PNGs
scripts/extract_data.py         # Valida métricas-chave
```

## Como regenerar os gráficos

```bash
python3 -m pip install matplotlib pandas numpy
python3 scripts/generate_charts.py
```

Os PNGs são gravados em `assets/charts/`.

## Números-chave (2024)

| Rubrica | Valor |
|---------|-------|
| Juros (setor público consolidado, BC) | R$ 950,4 bi |
| Renúncias fiscais (DIRBI) | R$ 331,6 bi |
| Bolsa Família | R$ 168,3 bi |
| Previdência militar (sistema) | R$ 61,5 bi |
| Emendas parlamentares (empenhado) | R$ 44,8 bi |

Detalhes, limitações metodológicas e links oficiais estão na Pesquisa.

## Licença de uso dos dados

Os números são de órgãos públicos brasileiros. Cite sempre a fonte original ao
reutilizar.
