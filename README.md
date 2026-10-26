# Gráfico 5.40 — BEN

Gráfico interativo em Python + Plotly baseado no `Dd_grafico_5_40.csv`.

## Dados

- Campo das estações: `Ano` (primeira coluna do CSV).
- Anos: 2016–2025.
- Separador de campos: `;`.
- Separador decimal: `,`.
- Valores ausentes são mantidos como lacunas no gráfico.

## Visual

- Eixo Y: 0–3,00.
- Intervalos: 0,50.
- Rótulos do eixo Y com vírgula decimal.
- Fundo `#DDE9F4`.
- Grade horizontal pontilhada.
- Uma série por estação.
- Marcadores circulares.
- Tooltip interativo.
- Zoom.
- HTML autocontido para GitHub Pages.

## Gerar

```bash
pip install pandas plotly
python gerar_grafico.py
```

## Publicar

```bash
git init
git add .
git commit -m "Adicionar grafico 5.40 BEN"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

No GitHub:
**Settings → Pages → Build and deployment → Source → GitHub Actions**
