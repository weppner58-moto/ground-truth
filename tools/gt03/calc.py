"""Ground Truth No. 03 — derived figures. Every 'Calculated' caption in the brief reproduces from here."""
# --- MV Agusta (H-D 10-K FY2009 R9.xml, FY2010 R10.xml, FY2011 R10.htm; XBRL IncomeLossFromDiscontinuedOperationsNetOfTax)
mv_consideration_eur, mv_consideration_usd = 68.3, 105.1
mv_debt_eur, mv_debt_usd = 47.5, 73.2
mv_cash_paid_net = 95.554            # $M, net of cash acquired (final allocation net assets)
mv_goodwill, mv_intang, mv_iprd = 85.750, 52.811, 20.1
mv_imp_2009, mv_imp_2010 = 115.4, 111.8
mv_dis = {2008: -29.517, 2009: -125.757, 2010: -113.124, 2011: +51.036}   # $M net of tax
mv_loss_3yr = sum(v for y, v in mv_dis.items() if y <= 2010)
mv_loss_net_of_2011 = sum(mv_dis.values())
mv_months = 24   # 8 Aug 2008 -> 6 Aug 2010
mv_op_capital_eur = 20.0
print(f"MV: 3-yr discontinued-ops loss = {mv_loss_3yr:.1f}M; after 2011 tax reversal = {mv_loss_net_of_2011:.1f}M")
print(f"MV: impairments 2009+2010 = {mv_imp_2009+mv_imp_2010:.1f}M; loss per month held = {mv_loss_3yr/mv_months:.1f}M")
print(f"MV: loss / consideration = {abs(mv_loss_3yr)/mv_consideration_usd:.2f}x")
# --- StaCyc (H-D Q1 2019 10-Q; LVWR 8-K 30 Sep 2022 Ex. 99.1; LVWR 10-K FY2022 R71)
st_total, st_cash, st_goodwill, st_intang = 14.9, 7.0, 9.5, 5.3
st_earnout_fv, st_earnout_max, st_earnout_paid = 4.978, 6.537, 3*2.180
print(f"StaCyc: cash at close + earn-out paid = {st_cash+st_earnout_paid:.2f}M; residual consideration not itemised = {st_total-st_cash-st_earnout_fv:.2f}M")
# --- LiveWire FY2025 (LVWR results release 10 Feb 2026)
lw_moto_2025, st_units_2025 = 653, 21633
lw_moto_rev, st_rev = 6.1, 19.6
print(f"StaCyc units per LiveWire motorcycle, 2025 = {st_units_2025/lw_moto_2025:.1f}x")
print(f"Revenue per unit: motorcycle ${lw_moto_rev*1e6/lw_moto_2025:,.0f}; StaCyc ${st_rev*1e6/st_units_2025:,.0f}")
print(f"StaCyc share of LiveWire product revenue 2025 = {st_rev/(st_rev+lw_moto_rev):.0%}")
# --- Eaglemark (10-K FY1994, FY1996) vs HDFS 2024/2025
eagle_total = 10 + 45
print(f"Eaglemark total cost = ${eagle_total}M; HDFS 2024 operating income $248.4M = {248.4/eagle_total:.1f}x purchase price, per year")
# --- Dealers / retail (10-K FY2014, FY2025)
us_dealers_2014, us_dealers_2025 = 694, 554
us_retail_2014, us_retail_2025 = 171079, 82698
print(f"US dealers 2014->2025 {us_dealers_2014}->{us_dealers_2025} = {(us_dealers_2025/us_dealers_2014-1):.1%}; US retail = {(us_retail_2025/us_retail_2014-1):.1%}")
print(f"US retail per dealer: 2014 {us_retail_2014/us_dealers_2014:.0f}; 2025 {us_retail_2025/us_dealers_2025:.0f}")
# --- Dust (LVWR 8-K 22 May 2026)
dust_firm = 0.375 + 0.5 + 3*0.875
print(f"Dust firm consideration = ${dust_firm:.3f}M; max incl. earn-out = ${dust_firm+11.25:.3f}M; cash portion = $0.375M")
# --- Alta footprint (H-D Q3 2018 10-Q R2; Q4 2018 release)
inv_income = {"Q3 2017": 1.083, "Q3 2018": -1.106, "Q4 2018": -1.679, "FY2017": 3.580, "FY2018": 0.951}
print(f"Investment income swing FY2017->FY2018 = {inv_income['FY2018']-inv_income['FY2017']:.2f}M (not attributed in any filing)")
# --- Hero X440 price (Hero release 3 Jul 2023): INR 2,29,000 at ~83 INR/USD (Jul 2023)
print(f"X440 Denim at 83 INR/USD = ${229000/83:,.0f}")
# --- Buell (Q4 2009 release)
print(f"Buell revenue per unit 2008 = ${123.1e6/13119:,.0f}; 2009 = ${46.5e6/9572:,.0f}")
