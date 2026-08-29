#!/usr/bin/env python3
"""Generate charts for the 2024 Bolsa Familia comparative research document."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "2024_master.csv"
OUT = ROOT / "assets" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

# Presentation palette
NAVY = "#0B3D5C"
TEAL = "#1A7A6D"
AMBER = "#D97706"
CORAL = "#C2410C"
SLATE = "#475569"
LIGHT = "#F1F5F9"
TEXT = "#0F172A"


def load_metrics() -> dict[str, float]:
    df = pd.read_csv(DATA)
    return {row.metric: float(row.value) for row in df.itertuples()}


def style_axes(ax: plt.Axes) -> None:
    ax.set_facecolor("white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.tick_params(colors=TEXT, labelsize=10)
    ax.grid(axis="x", color="#E2E8F0", linewidth=0.8)
    ax.set_axisbelow(True)


def bilhoes(x: float) -> str:
    return f"R$ {x / 1e9:.1f} bi"


def save(fig: plt.Figure, name: str, *, tight: bool = True) -> Path:
    path = OUT / name
    if tight:
        fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {path}")
    return path


def chart_comparativo(m: dict[str, float]) -> None:
    items = [
        ("Juros da dívida\n(setor público, Banco Central)", m["interest_consolidated_bc"], CORAL),
        ("Renúncias fiscais\n(DIRBI total)", m["tax_expenditures_dirbi_total"], AMBER),
        ("Bolsa Família", m["bf_cost_annual"], TEAL),
        ("Emendas parlamentares\n(empenhado)", m["amendments_committed"], NAVY),
        ("Previdência militar\n(sistema completo)", m["military_expenses_system"], SLATE),
    ]
    items.sort(key=lambda x: x[1], reverse=True)
    labels = [i[0] for i in items]
    values = [i[1] / 1e9 for i in items]
    colors = [i[2] for i in items]

    fig, ax = plt.subplots(figsize=(11, 6.2))
    bars = ax.barh(labels[::-1], values[::-1], color=colors[::-1], height=0.62)
    style_axes(ax)
    ax.set_xlabel("R$ bilhões (nominal, 2024)", fontsize=11, color=TEXT)
    ax.set_title(
        "Custo anual comparado — Brasil 2024",
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        pad=12,
    )
    for bar, val in zip(bars, values[::-1]):
        ax.text(
            bar.get_width() + 8,
            bar.get_y() + bar.get_height() / 2,
            f"R$ {val:.1f} bi",
            va="center",
            fontsize=10,
            color=TEXT,
            fontweight="bold",
        )
    ax.set_xlim(0, max(values) * 1.18)
    ax.annotate(
        "Juros = juros nominais apropriados do setor público consolidado (Banco Central).\n"
        "Inclui União, estados, municípios e efeito de swaps cambiais.",
        xy=(0.0, -0.18),
        xycoords="axes fraction",
        fontsize=8.5,
        color=SLATE,
    )
    save(fig, "01_custo_anual_comparativo.png")


def chart_custo_por_pessoa(m: dict[str, float]) -> None:
    bf_cost = m["bf_cost_annual"]
    bf_people = m["bf_people_jan"]
    mil_cost = m["military_expenses_system"]
    # Approximate beneficiaries: pensioners 2024 + inativos (~pension trunks not double-counted)
    # Use pensioners + estimate of inativos from actuarial (pension trunks ~136k are pensões,
    # inativos roughly ~160k from Defense payroll share). Use 235k pensioners + 160k inativos.
    mil_people = 235416 + 160000
    bf_per = bf_cost / bf_people
    mil_per = mil_cost / mil_people

    labels = [
        "Bolsa Família\n(por pessoa na família)",
        "Previdência militar\n(por inativo/pensionista)",
    ]
    values = [bf_per, mil_per]
    colors = [TEAL, SLATE]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    style_axes(ax)
    ax.grid(axis="y", color="#E2E8F0", linewidth=0.8)
    ax.set_ylabel("R$ por pessoa / ano (2024)", fontsize=11)
    ax.set_title(
        "Custo anual estimado por pessoa beneficiada",
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        pad=12,
    )
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() * 1.03,
            f"R$ {val:,.0f}".replace(",", "."),
            ha="center",
            fontsize=11,
            fontweight="bold",
            color=TEXT,
        )
    ax.set_ylim(0, max(values) * 1.25)
    ax.annotate(
        f"Bolsa Família: R$ {bf_cost/1e9:.1f} bi ÷ {bf_people/1e6:.0f} mi pessoas. "
        f"Militar: R$ {mil_cost/1e9:.1f} bi ÷ ~{mil_people/1e3:.0f} mil inativos+pensionistas "
        "(estimativa).",
        xy=(0.0, -0.16),
        xycoords="axes fraction",
        fontsize=8.5,
        color=SLATE,
    )
    save(fig, "02_custo_por_pessoa.png")


def chart_selic(m: dict[str, float]) -> None:
    items = [
        ("1 p.p. da Selic\n(custo anual estimado)", m["selic_1pp_cost"] / 1e9, CORAL),
        ("Bolsa Família\n(2024)", m["bf_cost_annual"] / 1e9, TEAL),
        ("Emendas parlamentares\n(empenhado 2024)", m["amendments_committed"] / 1e9, NAVY),
        ("Previdência militar\n(2024)", m["military_expenses_system"] / 1e9, SLATE),
    ]
    labels = [i[0] for i in items]
    values = [i[1] for i in items]
    colors = [i[2] for i in items]

    fig, ax = plt.subplots(figsize=(10, 5.8))
    bars = ax.bar(labels, values, color=colors, width=0.6)
    style_axes(ax)
    ax.grid(axis="y", color="#E2E8F0", linewidth=0.8)
    ax.set_ylabel("R$ bilhões / ano", fontsize=11)
    ax.set_title(
        "Quanto custa 1 ponto percentual da Selic?",
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        pad=12,
    )
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 3,
            f"R$ {val:.1f} bi",
            ha="center",
            fontsize=10,
            fontweight="bold",
            color=TEXT,
        )
    ax.set_ylim(0, max(values) * 1.2)
    ratio = m["selic_1pp_cost"] / m["bf_cost_annual"]
    ax.annotate(
        f"1 p.p. da Selic ≈ {ratio:.0%} do custo anual do Bolsa Família. "
        "Estimativa depende do estoque e da composição da dívida (~54% atrelada à Selic).",
        xy=(0.0, -0.16),
        xycoords="axes fraction",
        fontsize=8.5,
        color=SLATE,
    )
    save(fig, "03_custo_1pp_selic.png")


def chart_renuncias(m: dict[str, float]) -> None:
    # Top SPE sectors + residual so total matches DIRBI closed year
    industry = m["tax_industry_transformacao"]
    comercio = m["tax_comercio"]
    admin = m["tax_admin_services"]
    total = m["tax_expenditures_dirbi_total"]
    # SPE absolutes imply a slightly higher total; scale to DIRBI total while keeping order
    spe_top3 = industry + comercio + admin
    # Residual sectors from SPE share (~21.31% remaining after 78.69%)
    remaining_share = 1 - (0.4815 + 0.2492 + 0.0562)
    # Use SPE absolute for top 3 and compute residual vs DIRBI total for honesty
    residual = max(total - spe_top3, 0)
    # If SPE top3 already exceed DIRBI total (methodology gap), show SPE values as-is
    # and note residual as "other SPE sectors" using percentage remainder of SPE universe
    if residual < 1e9:
        spe_total = spe_top3 / (0.4815 + 0.2492 + 0.0562)
        residual = spe_total - spe_top3
        total_label = spe_total
    else:
        total_label = total

    items = [
        ("Indústria de transformação", industry),
        ("Comércio", comercio),
        ("Atividades administrativas\ne serviços complementares", admin),
        ("Demais setores", residual),
    ]
    items.sort(key=lambda x: x[1], reverse=True)
    labels = [i[0] for i in items]
    values = [i[1] / 1e9 for i in items]

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    bars = ax.barh(labels[::-1], values[::-1], color=[AMBER, NAVY, TEAL, SLATE][::-1], height=0.55)
    style_axes(ax)
    ax.set_xlabel("R$ bilhões (DIRBI / SPE, 2024)", fontsize=11)
    ax.set_title(
        "Renúncias fiscais federais por setor — 2024",
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        pad=12,
    )
    for bar, val in zip(bars, values[::-1]):
        ax.text(
            bar.get_width() + 2,
            bar.get_y() + bar.get_height() / 2,
            f"R$ {val:.1f} bi",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=TEXT,
        )
    ax.set_xlim(0, max(values) * 1.2)
    ax.annotate(
        "Fonte: SPE/Receita Federal (DIRBI). Valores de Indústria, Comércio e Admin. "
        "conforme Guia do Painel SPE. Demais setores = residual.",
        xy=(0.0, -0.16),
        xycoords="axes fraction",
        fontsize=8.5,
        color=SLATE,
    )
    save(fig, "04_renuncias_por_setor.png")


def chart_saida_escolaridade(m: dict[str, float]) -> None:
    items = [
        ("Menos que fundamental", m["exit_bf_edu_menos_fundamental"]),
        ("Fundamental incompleto", m["exit_bf_edu_fund_incompleto"]),
        ("Fundamental completo", m["exit_bf_edu_fund_completo"]),
        ("Médio incompleto", m["exit_bf_edu_medio_incompleto"]),
        ("Médio completo ou mais", m["exit_bf_edu_medio_mais"]),
    ]
    labels = [i[0] for i in items]
    values = [i[1] for i in items]

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    # Manual teal gradient (matplotlib may lack a named Teal colormap)
    teal_rgb = np.array([26, 122, 109]) / 255.0
    colors = [
        (* (teal_rgb * (0.45 + 0.55 * t)), 1.0)
        for t in np.linspace(0.0, 1.0, len(values))
    ]
    bars = ax.barh(labels, values, color=colors, height=0.55)
    style_axes(ax)
    ax.set_xlabel("Taxa de saída do Bolsa Família (%)", fontsize=11)
    ax.set_xlim(0, 100)
    ax.set_title(
        "Saída do Bolsa Família × escolaridade da pessoa de referência (2014→2025)",
        fontsize=13,
        fontweight="bold",
        color=TEXT,
        pad=12,
    )
    for bar, val in zip(bars, values):
        ax.text(
            val + 1.2,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}%",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=TEXT,
        )
    ax.axvline(60.68, color=CORAL, linestyle="--", linewidth=1.4, label="Média geral 60,68%")
    ax.legend(loc="lower right", fontsize=9)
    ax.annotate(
        "Jovens de 6–17 anos em 2014. Fonte: FGV/MDS — Filhos do Bolsa Família (Figura 9).",
        xy=(0.0, -0.14),
        xycoords="axes fraction",
        fontsize=8.5,
        color=SLATE,
    )
    save(fig, "05_saida_por_escolaridade.png")


def chart_efeito_trabalho(m: dict[str, float]) -> None:
    labels = [
        "IPEA NT78\n(piso R$400→R$600)\nredução na força\nde trabalho",
        "FGV IBRE\n(Bolsa Família ampliado)\nefeito sobre\nformalidade*",
        "Ocupados em\ndomicílios Bolsa Família\n2019 → 2023",
    ]
    # For FGV, use ~13% reduction in formal employment probability among newly eligible
    # as midpoint narrative figure from the blog; show as 13 pp-equivalent on secondary note
    ipea_mid = (m["ipea_labor_force_effect_low"] + m["ipea_labor_force_effect_high"]) / 2
    fgv_formal = 13.0
    occupied_change = m["ipea_occupied_share_bf_2023"] - m["ipea_occupied_share_bf_2019"]

    fig, ax = plt.subplots(figsize=(11, 6))
    # Panel-style bars with error for IPEA
    ax.bar(
        [0],
        [ipea_mid],
        yerr=[[ipea_mid - m["ipea_labor_force_effect_low"]],
              [m["ipea_labor_force_effect_high"] - ipea_mid]],
        color=AMBER,
        width=0.55,
        capsize=6,
        error_kw={"elinewidth": 1.5, "ecolor": TEXT},
        label="IPEA (p.p.)",
    )
    ax.bar([1], [fgv_formal], color=CORAL, width=0.55, label="FGV formalidade (%)")
    ax.bar([2], [occupied_change], color=TEAL, width=0.55, label="Variação ocupação (p.p.)")
    style_axes(ax)
    ax.grid(axis="y", color="#E2E8F0", linewidth=0.8)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Efeito (p.p. ou %)", fontsize=11)
    ax.set_title(
        "Efeitos estimados do Bolsa Família sobre oferta de trabalho — evidência mista",
        fontsize=13,
        fontweight="bold",
        color=TEXT,
        pad=12,
    )
    ax.axhline(0, color="#94A3B8", linewidth=1)
    ax.text(0, ipea_mid + 1.2, f"{m['ipea_labor_force_effect_low']:.1f}–{m['ipea_labor_force_effect_high']:.1f} p.p.",
            ha="center", fontsize=9, fontweight="bold")
    ax.text(1, fgv_formal + 0.6, "~13%", ha="center", fontsize=9, fontweight="bold")
    ax.text(2, occupied_change + 0.35, f"+{occupied_change:.1f} p.p.",
            ha="center", fontsize=9, fontweight="bold", color=TEAL)
    ax.set_ylim(-1, 16)
    ax.annotate(
        "*FGV IBRE: redução ~13% na probabilidade de emprego formal entre quem se torna elegível "
        "(Daniel Duque). IPEA: efeito pequeno na participação; sem efeito sobre informalidade.",
        xy=(0.0, -0.22),
        xycoords="axes fraction",
        fontsize=8.2,
        color=SLATE,
    )
    save(fig, "06_efeito_trabalho.png")


def chart_populacao(m: dict[str, float]) -> None:
    bar_spacing = 1.45
    bar_width = 0.46
    x_label_font_size = 7.2
    footnote_font_size = 9.1

    labels = [
        "Trabalhadores\nCLT\n(PNAD privado)",
        "Trabalhadores\nInformais +\nIntermitentes*",
        "Trabalhadores\nMEI\n(ativos)",
        "Empresários\nativos\n(não-MEI)**",
        "Trabalhadores\nbeneficiários\ndo Bolsa\nFamília***",
        "Beneficiários\ndo Bolsa\nFamília\nem idade\nativa -\nDesocupados***",
        "Crianças e\nIdosos no\nBolsa\nFamília***",
    ]
    values = [
        m["pnad_clt_privado"] / 1e6,
        m["informais_mais_intermitentes"] / 1e6,
        m["mei_ativos"] / 1e6,
        m["empresarios_nao_mei"] / 1e6,
        m["bf_working_age_employed_est"] / 1e6,
        m["bf_working_age_not_employed_est"] / 1e6,
        m["bf_not_working_age_est"] / 1e6,
    ]
    colors = [NAVY, AMBER, "#7C3AED", SLATE, TEAL, CORAL, "#0D9488"]

    fig, ax = plt.subplots(figsize=(11.8, 8.0))
    x_pos = np.arange(len(labels)) * bar_spacing
    bars = ax.bar(x_pos, values, color=colors, width=bar_width)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, fontsize=x_label_font_size)
    ax.tick_params(axis="x", pad=10)
    ax.set_xlim(x_pos[0] - 0.68, x_pos[-1] + 0.68)
    style_axes(ax)
    ax.grid(axis="y", color="#E2E8F0", linewidth=0.8)
    ax.set_ylabel("Milhões de pessoas", fontsize=11)
    ax.set_title(
        "Pessoas Ativas e Inativas no Mercado de Trabalho",
        fontsize=13,
        fontweight="bold",
        color=TEXT,
        pad=12,
    )
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.7,
            f"{val:.1f} mi",
            ha="center",
            fontsize=9,
            fontweight="bold",
            color=TEXT,
        )
    ax.set_ylim(0, max(values) * 1.22)
    footnotes = [
        "* Informais PNAD (40,3 mi) + intermitentes RAIS (~0,47 mi; celetistas atípicos).",
        "** Empresas ativas menos MEI (Mapa de Empresas).",
        "*** Estimativas Bolsa Família: trabalhadores ocupados = 46,8% das pessoas em "
        "lares (IPEA);",
        "desocupados em idade ativa = residual; crianças (0–13 anos) e idosos (65+) ≈ "
        "50% do total. Conjuntos se cruzam.",
    ]
    footnote_y_start = -0.22
    footnote_line_step = 0.036
    for idx, line in enumerate(footnotes):
        ax.text(
            0.0,
            footnote_y_start - idx * footnote_line_step,
            line,
            transform=ax.transAxes,
            fontsize=footnote_font_size,
            color=SLATE,
            ha="left",
            va="top",
            clip_on=False,
        )
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.21, top=0.90)
    save(fig, "07_populacao_trabalho_bf.png", tight=False)


def main() -> None:
    m = load_metrics()
    chart_comparativo(m)
    chart_custo_por_pessoa(m)
    chart_selic(m)
    chart_renuncias(m)
    chart_saida_escolaridade(m)
    chart_efeito_trabalho(m)
    chart_populacao(m)
    print("done")


if __name__ == "__main__":
    main()
